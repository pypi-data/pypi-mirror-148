"""Parse and validate config.json"""
import logging
import typing as t

import fw_utils
from flywheel_gear_toolkit import GearToolkitContext
from flywheel_gear_toolkit.utils import zip_tools

from fw_gear_ants_dbm_cross_sectional import TEMPLATES_DIR

from .utils import generate_template_file_mapping

logger = logging.getLogger(__name__)


def parse_config(
    gear_context: GearToolkitContext, out_file_prefix: str
) -> t.Tuple[t.Dict, t.Dict]:
    """Parse antsCorticalThickness config values and gear inputs
    Args:
        gear_context:
        out_file_prefix:

    Returns:
        tuple:
            dict: Mapping of template files
            dict: Config values for antsCorticalThickness

    """
    gear_config = gear_context.config_json["config"]

    # Gear specific config
    atlases_template = gear_config.pop("atlases_template")
    debug = gear_config.pop("debug")

    selected_template_dir = ""
    template_name = ""
    if gear_context.get_input_path("registered_predefined_template"):
        selected_template_dir = fw_utils.TempDir().name
        template_name = gear_context.get_input_path("registered_predefined_template")
        logger.info(f"Found {template_name}...")
        logger.info("Unzipping the template archive...")
        zip_tools.unzip_archive(
            gear_context.get_input_path("registered_predefined_template"),
            selected_template_dir,
        )
    else:
        template_name = atlases_template
        logger.info(f"No template was provided...Using {template_name}...")
        selected_template_dir = TEMPLATES_DIR / template_name
    logger.info(f"Using template {template_name} for the gear...")
    atlases_template_file_mapping = generate_template_file_mapping(
        selected_template_dir
    )

    gear_config["out_prefix"] = out_file_prefix

    return atlases_template_file_mapping, gear_config
