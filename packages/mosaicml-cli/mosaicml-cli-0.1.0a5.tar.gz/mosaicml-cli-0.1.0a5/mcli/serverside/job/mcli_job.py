""" Kubernetes Intermediate Job Abstraction """

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, cast

import yaml
from kubernetes import client

from mcli import config, version
from mcli.models import MCLIEnvVar, MCLIIntegration, MCLIPlatform, RunInput
from mcli.serverside.job.mcli_k8s_job import MCLIConfigMap, MCLIK8sJob, MCLIVolume
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.utils.utils_kube_labels import label

if TYPE_CHECKING:
    from mcli.models import MCLISecret

logger = logging.getLogger(__name__)


@dataclass
class MCLIJob():
    """ Kubernetes Intermediate Job Abstraction """

    run_id: str
    run_name: str
    instance_type: InstanceType
    platform: MCLIPlatform
    num_nodes: int
    image: str
    integrations: List[MCLIIntegration]
    secrets: List[MCLISecret]
    env_variables: List[MCLIEnvVar]

    command: str
    parameters: Dict[str, Any]

    @property
    def unique_name(self) -> str:
        """Gets a unique name from user set name and run_id"""
        return self.run_name + '-' + self.run_id

    @classmethod
    def from_run_input(cls, run_input: RunInput) -> MCLIJob:
        mcli_config: config.MCLIConfig = config.MCLIConfig.load_config()

        secrets: List[MCLISecret] = []
        secrets += mcli_config.secrets
        secrets += [MCLISecret.from_dict(x) for x in run_input.secrets]

        env_variables: List[MCLIEnvVar] = []
        env_variables += mcli_config.environment_variables
        env_variables += [MCLIEnvVar.from_dict(x) for x in run_input.env_variables]

        integrations: List[MCLIIntegration] = []
        for integration_data in run_input.integrations:
            integrations.append(MCLIIntegration.from_dict(integration_data))

        # Convert instance_type and platform into objects
        # TODO(HEK-323): Refactor so this hack isn't necessary to get the platform

        # pylint: disable-next=import-outside-toplevel
        from mcli.serverside.platforms.registry import PlatformRegistry
        registry = PlatformRegistry()
        platform, instance_type = registry.get_mcli_platform_and_instance_type(instance_str=run_input.instance_type,)
        # END TODO(HEK-323):

        data = {
            'run_id': run_input.run_id,
            'run_name': run_input.run_name,
            'instance_type': instance_type,
            'platform': platform,
            'num_nodes': run_input.num_nodes,
            'image': run_input.image,
            'integrations': integrations,
            'secrets': secrets,
            'env_variables': env_variables,
            'command': run_input.command,
            'parameters': run_input.parameters
        }

        return MCLIJob(**data)

    def get_kubernetes_job(self) -> MCLIK8sJob:
        kubernetes_job = cast(MCLIK8sJob, MCLIK8sJob.empty(name=self.unique_name))
        assert isinstance(kubernetes_job, MCLIK8sJob)
        kubernetes_job.container.image = self.image
        kubernetes_job.container.command = ['/bin/bash', '-c']
        kubernetes_job.container.command_string = self.command
        kubernetes_job.metadata = client.V1ObjectMeta(name=self.unique_name)
        kubernetes_job.spec.ttl_seconds_after_finished = config.JOB_TTL

        for env_item in self.env_variables:
            kubernetes_job.add_env_var(client.V1EnvVar(
                name=env_item.env_key,
                value=env_item.env_value,
            ))

        for secret in self.secrets:
            success = secret.add_to_job(kubernetes_job=kubernetes_job)
            if not success:
                logger.warning(f'Unable to add secret: \n{secret}')

        for integration in self.integrations:
            success = integration.add_to_job(kubernetes_job=kubernetes_job)
            if not success:
                logger.warning(f'Unable to add integration: \n{integration}')

        # Configure for instance
        kubernetes_job.container.resources = self.instance_type.resource_requirements
        if isinstance(kubernetes_job.container.resources.limits, dict) and \
            kubernetes_job.container.resources.limits.get(label.nvidia.GPU, 0) == 0:
            # If no GPUs requested, limit the container visibility with this envvar.
            # see: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html#gpu-enumeration
            kubernetes_job.add_env_var(client.V1EnvVar(
                name='NVIDIA_VISIBLE_DEVICES',
                value='void',
            ))

        return kubernetes_job

    def get_config_map(self) -> MCLIConfigMap:
        data = yaml.dump({k: v for k, v in self.parameters.items() if not k.startswith('_')})
        cm = client.V1ConfigMap(
            api_version='v1',
            kind='ConfigMap',
            data={'parameters.yaml': data},
        )
        cm.metadata = client.V1ObjectMeta(name=self.unique_name)
        cm_volume = client.V1Volume(
            name='config',
            config_map=client.V1ConfigMapVolumeSource(name=self.unique_name),
        )
        cm_mount = client.V1VolumeMount(
            name='config',
            mount_path='/mnt/config',
        )

        return MCLIConfigMap(
            config_map=cm,
            config_volume=MCLIVolume(
                volume=cm_volume,
                volume_mount=cm_mount,
            ),
        )

    def get_shared_metadata(self) -> client.V1ObjectMeta:
        labels = {
            label.mosaic.JOB: self.unique_name,
            'type': 'mcli',
            label.mosaic.LAUNCHER_TYPE: 'mcli',
            label.mosaic.MCLI_VERSION: str(version.__version__),
            label.mosaic.MCLI_VERSION_MAJOR: str(version.__version_major__),
            label.mosaic.MCLI_VERSION_MINOR: str(version.__version_minor__),
            label.mosaic.MCLI_VERSION_PATCH: str(version.__version_patch__),
        }
        shared_metadata = client.V1ObjectMeta(labels=labels)
        return shared_metadata
