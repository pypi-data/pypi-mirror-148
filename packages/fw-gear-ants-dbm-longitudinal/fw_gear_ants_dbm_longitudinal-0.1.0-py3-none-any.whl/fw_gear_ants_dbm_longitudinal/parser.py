"""Parser module to parse gear config.json."""
import logging
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from flywheel_gear_toolkit.utils import zip_tools

from fw_gear_ants_dbm_longitudinal import TEMPLATES_DIR

logger = logging.getLogger(__name__)


def generate_template_file_mapping(template_dir):
    """

    Args:
        template_dir (Path): Path to template directory.

    Returns:
        dict: Dictionary with template name as key and template file name as value.
    """
    template_file_mapping = dict()

    if not isinstance(template_dir, Path):
        template_dir = Path(template_dir)

    for p in template_dir.iterdir():
        if p.is_dir():
            file_list = [x.as_posix() for x in p.glob("*.nii.gz")]
            # Check number of files in each directory except priors template
            if "priors" not in p.name.lower() and len(file_list) != 1:
                logger.error(
                    f"Expecting one file for the {p.name} template directory. Found {len(file_list)} instead."
                )
                sys.exit(1)

            template_file_mapping[p.name] = file_list

    return template_file_mapping


def parse_config(context):
    """Parse geartoolkit context to get/download gear inputs.

    Args:
        context (GearToolkitContext): flywheel Gear Toolkit Context

    Returns:
        (tuple): Tuple containing
            - Regular Expression (regex) of input files
            - Input Files tags
            - Mapping of atlases template directory
    """
    input_regex = context.config.get("input_regex")
    input_tags = context.config.get("input_tags")

    if not input_regex and not input_tags:
        logger.error("Input Regex or Input Tags must be defined. None found.")
        sys.exit(1)
    # Parse the input
    selected_template_dir = ""
    if context.get_input_path("registered_predefined_atlases"):
        temp_template_dir = Path(TemporaryDirectory().name)
        zip_tools.unzip_archive(
            context.get_input_path("registered_predefined_atlases"),
            temp_template_dir,
        )
        dir_list = list(temp_template_dir.iterdir())
        if len(dir_list) == 1:
            template_name = dir_list[0].name
            selected_template_dir = temp_template_dir / template_name
        else:
            logger.debug(f"Here is the template folder list - {dir_list}")
            raise TypeError(
                f"Expecting one template folder but found {len(dir_list)} instead."
            )

    else:
        template_name = context.config.get("atlases_template")
        selected_template_dir = TEMPLATES_DIR / template_name

    if not selected_template_dir.exists():
        raise ValueError(f"Template not found: {template_name}")
    else:
        atlases_template_dir_mapping = generate_template_file_mapping(
            selected_template_dir
        )

    if input_tags:
        input_tags = [tag.strip() for tag in input_tags.split(",")]

    return input_regex, input_tags, atlases_template_dir_mapping
