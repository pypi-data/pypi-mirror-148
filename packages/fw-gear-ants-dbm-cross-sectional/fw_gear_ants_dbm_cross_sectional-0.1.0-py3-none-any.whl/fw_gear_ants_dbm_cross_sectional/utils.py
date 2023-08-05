import logging
import os
import typing as t
import zipfile
from pathlib import Path

import fw_utils

TEMPLATE_DIR_BASE = {
    "Priors2": "",
    "brain_extraction_probability_mask": "",
    "brain_segmentation_template": "",
    "extraction_registration_mask": "",
    "t1_registration_template": "",
}

logger = logging.getLogger(__name__)


def generate_template_file_mapping(template_dir: t.Union[Path, str]) -> t.Dict:
    """Generate mapping for antsCorticalThickness template/mask input

    Args:
        template_dir: Path to template directory

    Returns:
        dict: Dictionary with template name as key and template file name as value
    """
    template_file_mapping = TEMPLATE_DIR_BASE.copy()

    priors_list = list()

    for file_ in fw_utils.fileglob(template_dir, pattern="*.nii.gz", recurse=True):
        # Validate parent dir name
        if file_.parent.name in TEMPLATE_DIR_BASE.keys():
            if file_.parent.name == "Priors2":
                priors_list.append(file_.as_posix())
            else:
                template_file_mapping[file_.parent.name] = file_.as_posix()
        else:
            logger.info(
                f"{file_.parent.name} not found in predefined directory name. Skipping..."
            )
            logger.debug(
                f"Details: Directory name must be matching one of the following: {*TEMPLATE_DIR_BASE.keys(),}"
            )
            logger.debug("Please refer to README.md for more details")
    template_file_mapping["Priors2"] = priors_list if priors_list else ""

    if all(template_file_mapping.values()):
        return template_file_mapping
    else:
        empty_pair = [k for k, v in template_file_mapping.items() if not v]
        raise ValueError(
            f"Missing template file for the following mask: {*empty_pair,} \n"
            f"Please refer to README.md for more details."
        )


def zip_outputs_files(directory: t.Union[Path, str], zip_filename: t.Union[Path, str]):
    """Zip files in target directory to destination zip file path"""
    if os.path.exists(directory):

        outZipFile = zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED)

        rootdir = os.path.basename(directory)

        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                parentpath = os.path.relpath(filepath, directory)
                arcname = os.path.join(rootdir, parentpath)

                outZipFile.write(filepath, arcname)

        outZipFile.close()

    else:
        raise FileNotFoundError(f"The directory, {directory}, does not exist.")
