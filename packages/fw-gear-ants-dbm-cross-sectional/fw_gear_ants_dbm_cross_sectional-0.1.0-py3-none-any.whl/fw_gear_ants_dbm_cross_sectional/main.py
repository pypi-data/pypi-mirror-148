"""Main module."""

import logging
import sys
from pathlib import Path

from .utils import zip_outputs_files
from .workflow import config_segmentation_workflow, setup_cortical_thickness

logger = logging.getLogger(__name__)


def run(
    interface_config, work_dir, anatomical_image, template_file_mapping, output_dir
):
    sinker_out_dir = Path(work_dir) / "sinker"
    sinker_out_dir.mkdir(exist_ok=True, parents=True)
    try:
        cortical_thickness_node = setup_cortical_thickness(
            anatomical_image, template_file_mapping, interface_config
        )
        seg_wf = config_segmentation_workflow(
            work_dir, cortical_thickness_node, sinker_out_dir
        )
        logger.debug("Running antsCorticalThickness workflow...")
        seg_wf.run()

    except Exception:
        logger.exception("antsCorticalThickness workflow failed...")
        logger.info("Exiting....")
        sys.exit(1)
    else:
        logger.info("antsCorticalThickness workflow has been successfully completed...")

    archive_file_name = f"{interface_config['out_prefix']}_outputs.zip"

    zip_outputs_files(sinker_out_dir / "outputs", output_dir / archive_file_name)
    logger.info(f"Generated output archive file as {archive_file_name}...")
