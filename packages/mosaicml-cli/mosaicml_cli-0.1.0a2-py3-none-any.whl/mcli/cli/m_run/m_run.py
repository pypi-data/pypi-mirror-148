""" mcli run Entrypoint """
import argparse
import logging
import textwrap
from typing import List, Optional

from mcli import config
from mcli.api.model.run_model import RunModel
from mcli.models import PartialRunInput, RunInput
from mcli.serverside.job.mcli_job import MCLIJob
from mcli.serverside.platforms.experimental import ExperimentalFlag
from mcli.serverside.runners.runner import Runner

logger = logging.getLogger(__name__)


def run(
    file: str,
    experimental: Optional[List[ExperimentalFlag]] = None,
    **kwargs,
) -> int:
    del kwargs
    # TODO: Reintroduce experimental
    del experimental
    logger.info(
        textwrap.dedent("""
    ------------------------------------------------------
    Let's run this run
    ------------------------------------------------------
    """))

    partial_run_input = PartialRunInput.from_file(path=file)
    run_input = RunInput.from_partial_run_input(partial_run_input)

    if config.feature_enabled(config.FeatureFlag.USE_FEATUREDB):
        run_model = RunModel.from_run_input(run_input=run_input)
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.runs.create_run import create_run
        if not create_run(run_model):
            print('Failed to persist run')

    # Populates the full MCLI Job including user defaults
    mcli_job = MCLIJob.from_run_input(run_input=run_input)

    runner = Runner()
    runner.submit(job=mcli_job,)

    print('Submitted job')
    return 0


def add_run_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser: argparse.ArgumentParser = subparser.add_parser(
        'run',
        aliases=['r'],
        help='Run stuff',
    )
    run_parser.set_defaults(func=run)
    _configure_parser(run_parser)


def _configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        '-f',
        '--file',
        dest='file',
        help='File from which to load arguments.',
    )

    parser.add_argument(
        '--experimental',
        choices=ExperimentalFlag.permitted(),
        type=ExperimentalFlag,
        nargs='+',
        default=None,
        metavar='FLAG',
        help=
        'Enable one or more experimental flags. These flags are designed to take advantage of a specific feature that '
        'may still be too experimental for long-term inclusion in mcli.')
