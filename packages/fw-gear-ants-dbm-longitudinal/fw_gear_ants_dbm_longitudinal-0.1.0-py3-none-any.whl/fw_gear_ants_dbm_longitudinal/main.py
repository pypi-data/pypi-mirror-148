"""Main module."""

import logging
import sys

from flywheel_gear_toolkit.utils.decorators import report_usage_stats

from fw_gear_ants_dbm_longitudinal.utils import setup_logger
from fw_gear_ants_dbm_longitudinal.workflow import (
    config_antsL_workflow,
    setup_dbm_nodes,
)

logger = logging.getLogger(__name__)


@report_usage_stats(save_output=True, output_format="png")
def usage_stats_run(antsL_workflow):
    try:
        logger.debug("Starting usage stats report....")
        antsL_workflow.run()

    except Exception:
        logger.exception("antsLongitudinalCorticalThickness workflow failed...")
        logger.info("Exiting....")
        sys.exit(1)
    else:
        logger.info(
            "antsLongitudinalCorticalThickness workflow has been successfully completed..."
        )


def run(
    config_dict,
    workflow_dir,
    anatomical_input_mapping,
    atlases_template_dir,
    subj_label,
    output_dir,
):
    """
    Args:
        config_dict (dict):
        workflow_dir (pathlib.Path):
        anatomical_input_mapping (list):
        atlases_template_dir (pathlib.Path):
        subj_label (str):
        output_dir (pathlib.Path):

    Returns:

    """
    try:

        dbm_longitudinal_node = setup_dbm_nodes(
            config_dict, anatomical_input_mapping, atlases_template_dir, subj_label
        )

        antsL_nipype_workflow = config_antsL_workflow(
            workflow_dir, output_dir.parent.absolute(), dbm_longitudinal_node
        )
        logger.debug("Running workflow....")

        if logger.isEnabledFor(logging.DEBUG):
            usage_stats_run(antsL_nipype_workflow)
        else:
            antsL_nipype_workflow.run()

    except Exception:
        logger.exception("antsLongitudinalCorticalThickness workflow failed...")
        logger.info("Exiting....")
        sys.exit(1)
    else:
        # Append antsLongitudinalCorticalThickness.sh command line args to output file
        cortical_node = antsL_nipype_workflow.get_node("dbm_cortical")

        output_logger = setup_logger(
            "antsLongitudinalCorticalThickness",
            output_dir / "antsL_output_files_info.txt",
        )
        output_logger.info("    ")
        output_logger.info(
            "---------- antsLongitudinalCorticalThickness.sh commandline ----------"
        )
        output_logger.info(cortical_node._interface.cmdline)
        output_logger.info("---------- End of File ----------")
        logger.info(
            "antsLongitudinalCorticalThickness workflow has been successfully completed..."
        )
