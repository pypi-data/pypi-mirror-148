""" mcli interactive Entrypoint """
import argparse
from typing import Optional

from mcli.serverside.platforms.registry import PlatformRegistry


def interactive_entrypoint(
    num_gpus: Optional[int] = None,
    **kwargs,
) -> int:
    del kwargs
    if num_gpus is None:
        print('A number of gpus must be selected\n'
              'mcli interactive <num_gpus>')
        return 1

    registry = PlatformRegistry()
    k8s_platforms = [registry.get_k8s_platform(x) for x in registry.platforms]
    interactive_platforms = [x for x in k8s_platforms if x.interactive]
    if len(interactive_platforms) == 0:
        print('No interactive platforms registered.\n'
              'Make sure to register your interactive platform with mcli create platform first')
        return 1
    for interactive_platform in interactive_platforms:
        if num_gpus in interactive_platform.get_allowed_interactive_gpu_nums():
            _ = interactive_platform.get_interactive_instance_from_gpus(num_gpus=num_gpus)
            # TODO(averylamp): Launch interactive job with new platform refactor

    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:

    parser.add_argument('num_gpus', default=None, type=int, help='Number of GPUs to run interactively')
    parser.set_defaults(func=interactive_entrypoint)
    return parser


def add_interactive_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """

    interactive_parser: argparse.ArgumentParser = subparser.add_parser(
        'interactive',
        aliases=['int'],
        help='Get an interactive instance',
    )
    get_parser = configure_argparser(parser=interactive_parser)
    return get_parser
