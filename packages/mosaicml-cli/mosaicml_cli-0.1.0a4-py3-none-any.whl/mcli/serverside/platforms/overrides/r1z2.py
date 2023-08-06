# pylint: disable=duplicate-code

""" R1Z2 Platform Definition """

from typing import Dict, List

from mcli.models import MCLIPlatform
from mcli.serverside.job.mcli_k8s_job import MCLIVolume
from mcli.serverside.platforms.instance_type import InstanceList
from mcli.serverside.platforms.overrides.r1z2_instances import R1Z2_INSTANCE_LIST
from mcli.serverside.platforms.platform import GenericK8sPlatform

NUM_MULTI_GPU_TOLERATE = 8
MAX_CPUS = 60

R1Z2_PRIORITY_CLASS_LABELS: Dict[str, str] = {
    'scavenge': 'mosaicml-internal-research-scavenge-priority',
    'standard': 'mosaicml-internal-research-standard-priority',
    'emergency': 'mosaicml-internal-research-emergency-priority'
}


class R1Z2Platform(GenericK8sPlatform):
    """ R1Z2 Platform Overrides """

    allowed_instances: InstanceList = R1Z2_INSTANCE_LIST
    priority_class_labels = R1Z2_PRIORITY_CLASS_LABELS  # type: Dict[str, str]
    default_priority_class: str = 'standard'

    def __init__(self, platform_information: MCLIPlatform) -> None:
        self.interactive = True
        super().__init__(platform_information)

    def get_volumes(self) -> List[MCLIVolume]:
        volumes = super().get_volumes()
        # mcli_config = config.MCLIConfig.load_config()
        # volumes.append(
        #     MCLIVolume(
        #         volume=client.V1Volume(
        #             name='local',
        #             host_path=client.V1HostPathVolumeSource(path='/localdisk', type='Directory'),
        #         ),
        #         volume_mount=client.V1VolumeMount(
        #             name='local',
        #             mount_path='/localdisk',
        #         ),
        #     ))
        return volumes
