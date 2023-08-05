import logging as log
import os
from pathlib import Path

from nipype import config, logging

cfg = dict(
    execution={
        "stop_on_first_crash": True,
        "hash_method": "content",
        "remove_unnecessary_outputs": False,
        "crashfile_format": "txt",
        "crashdump_dir": os.path.abspath("./output"),
    },
)

config.update_config(cfg)
logging.update_logging(config)

import nipype.pipeline.engine as pe
from nipype.interfaces.io import DataSink

logger = log.getLogger(__name__)

from fw_gear_ants_dbm_longitudinal.interfaces import (
    DBMLongitudinalCorticalThickness,
    antsLResultsGenerator,
)


def config_antsL_workflow(workflow_dir, output_dir_parent, dbm_node):
    """Configure Nipype Workflow to run DBM executable and generate proper zip archive in designated output directory.

    Args:
        workflow_dir (pathlib.Path): Path to store nipype workflow files
        output_dir_parent (pathlib.Path): Path to store all the output files
        dbm_node (nipype.pe.Node): DBM nipype node

    Returns:
        nipype.pe.Workflow: Ants Longitudinal DBM Workflow
    """
    logger.info(f"Creating ANTSL workflow...")
    logger.debug(f"Setting dbm_longitudinal_workflow base dir to {workflow_dir} ")

    workflow_dir = Path(workflow_dir)
    workflow_dir.mkdir(exist_ok=True, parents=True)
    dbm_longitudinal_wf = pe.Workflow(
        name="dbm_longitudinal_workflow", base_dir=workflow_dir
    )

    logger.info("Creating Nodes for the workflow...")
    outputs_generator_node = pe.Node(antsLResultsGenerator(), name="parse_outputs")
    # Set up sinker nodes here
    logger.debug(f"Setting up Datasink")
    sinker_node = pe.Node(DataSink(), name="sinker")
    logger.debug(f"Setting sinker directory to {output_dir_parent}")
    sinker_node.inputs.base_directory = str(output_dir_parent)

    logger.debug("Connecting nodes...")

    try:

        dbm_longitudinal_wf.connect(
            [
                (
                    dbm_node,
                    outputs_generator_node,
                    [
                        ("SingleSubjectTemplateDir", "SSTemplateDir"),
                        ("TimePointDir", "TPDir"),
                    ],
                ),
                (
                    outputs_generator_node,
                    sinker_node,
                    [
                        ("SingleSubjectTemplateArchive", "output.@SSTemplateArchive"),
                        ("TimePointTemplateArchive", "output.@TPTemplateArchive"),
                        ("OutputFilesInfo", "output.@OutputFilesInfo"),
                    ],
                ),
            ]
        )
    except Exception:

        logger.exception(
            "Error occurred while setting up DBM Longitudinal Workflow nodes"
        )

        raise

    else:

        return dbm_longitudinal_wf


def setup_dbm_nodes(config_dict, file_mapping_list, template_dir_mapping, subj_label):
    """Setting up inputs for DBM nipype Nodes.

    Args:
        config_dict (dict): Configuration for antsLongitudinalCorticalThickness.sh
        file_mapping_list (list): List of anatomical files
        template_dir_mapping (dict): Dictionary of template file path
        subj_label (str): Current subject label

    Returns:
        nipype.Nodes: Nodes for DBMLongitudinalCorticalThickness interface
    """

    dbm_node = pe.Node(DBMLongitudinalCorticalThickness(), name="dbm_cortical")
    # -d
    dbm_node.inputs.dimension = config_dict.get("image_dimension")
    # anatomical image inputs
    dbm_node.inputs.anatomical_image = file_mapping_list

    for key, val in template_dir_mapping.items():
        if key == "Priors2":
            priors_file_list = val
            priors_file_list.sort()
            setattr(dbm_node.inputs, "brain_segmentation_priors", priors_file_list)
        else:
            setattr(dbm_node.inputs, key, val[0])

    # -o
    dbm_node.inputs.out_prefix = subj_label + "_antsL"
    # -c
    dbm_node.inputs.control_type = 2

    # -g
    dbm_node.inputs.denoise_anatomical_images = config_dict.get(
        "denoise_anatomical_image"
    )

    # -j
    logger.debug(f"Setting number of cores to {os.cpu_count() - 1}")
    dbm_node.inputs.num_cores = os.cpu_count() - 1
    # -k
    dbm_node.inputs.num_modalities = config_dict.get("number_of_modalities")
    # -x
    dbm_node.inputs.atropos_iteration = config_dict.get("atropos_iteration")
    # -r
    dbm_node.inputs.rigid_alignment = config_dict.get("rigid_alignment_to_SST")

    # -y
    dbm_node.inputs.rigid_template_update_component = config_dict.get(
        "rigid_template_update_component"
    )

    return dbm_node
