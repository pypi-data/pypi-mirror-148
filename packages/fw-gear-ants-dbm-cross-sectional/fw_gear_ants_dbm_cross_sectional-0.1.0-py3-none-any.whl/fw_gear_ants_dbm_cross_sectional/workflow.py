"""Handle ants cross sectional nipype workflow."""
import logging as log
import typing as t
from pathlib import Path

from nipype import config, logging

cfg = dict(  # pragma: no cover
    execution={
        "stop_on_first_crash": True,
        "hash_method": "content",
        "remove_unnecessary_outputs": False,
        "crashfile_format": "txt",
        "crashdump_dir": "/flywheel/v0/output",
    },
)

config.update_config(cfg)
logging.update_logging(config)

import nipype.pipeline.engine as pe
from nipype.interfaces.io import DataSink

from .interfaces import CorticalThicknessEnhanced

logger = log.getLogger(__name__)


def config_segmentation_workflow(
    workflow_dir: t.Union[Path, str], ct_node: pe.Node, sinker_dir: t.Union[Path, str]
) -> pe.Workflow:
    logger.info("Setting up segmentation workflow")
    logger.debug(f"Setting up workflow base fir as {workflow_dir}")

    workflow_dir = Path(workflow_dir)
    workflow_dir.mkdir(exist_ok=True, parents=True)

    seg_wf = pe.Workflow(
        name="ants_dbm_cross_sectional_workflow", base_dir=workflow_dir
    )

    logger.debug(f"Setting up Datasink")
    sinker_node = pe.Node(DataSink(), name="sinker")
    logger.debug(f"Setting sinker directory to {sinker_dir}")
    sinker_node.inputs.base_directory = str(sinker_dir)

    logger.debug("Connecting nodes...")

    try:
        seg_wf.connect(
            [
                (
                    ct_node,
                    sinker_node,
                    [
                        ("BrainExtractionMask", "outputs.@brain_extraction_mask"),
                        ("ExtractedBrainN4", "outputs.@ExtractedBrainN4"),
                        ("BrainSegmentation", "outputs.@BrainSegmentation"),
                        ("BrainSegmentationN4", "outputs.@BrainSegmentationN4"),
                        (
                            "BrainSegmentationPosteriors",
                            "outputs.@BrainSegmentationPosteriors",
                        ),
                        ("CorticalThickness", "outputs.@CorticalThickness"),
                        (
                            "TemplateToSubject1GenericAffine",
                            "outputs.@TemplateToSubject1GenericAffine",
                        ),
                        ("TemplateToSubject0Warp", "outputs.@TemplateToSubject0Warp"),
                        ("SubjectToTemplate1Warp", "outputs.@SubjectToTemplate1Warp"),
                        (
                            "SubjectToTemplate0GenericAffine",
                            "outputs.@SubjectToTemplate0GenericAffine",
                        ),
                        (
                            "SubjectToTemplateLogJacobian",
                            "outputs.@SubjectToTemplateLogJacobian",
                        ),
                        (
                            "CorticalThicknessNormedToTemplate",
                            "outputs.@CorticalThicknessNormedToTemplate",
                        ),
                        ("BrainVolumes", "outputs.@BrainVolumes"),
                    ],
                )
            ]
        )
    except Exception as exc:
        logger.error("Unhandled exception", exc_info=True)
        raise RuntimeError(*exc.args) from exc

    return seg_wf


def setup_cortical_thickness(
    anatomical_image: t.Union[Path, str], template_image_mapping: t.Dict, config: t.Dict
) -> pe.Node:
    """Setup antsCorticalThickness node.

    Args:
        anatomical_image:  Anatomical image for antsCorticalThickness
        template_image_mapping: Dictionary of template file path
        config: Configuration for antsCorticalThicness

    Returns:
        nipype.Nodes: Nodes for antsCorticalThickness workflow
    """
    cross_thickness_node = pe.Node(
        CorticalThicknessEnhanced(), name="antsCorticalThickness"
    )
    # Mandotory inputs
    # -a
    cross_thickness_node.inputs.anatomical_image = anatomical_image
    # -m
    cross_thickness_node.inputs.brain_probability_mask = template_image_mapping[
        "brain_extraction_probability_mask"
    ]
    # -e
    cross_thickness_node.inputs.brain_template = template_image_mapping[
        "brain_segmentation_template"
    ]
    # -p
    cross_thickness_node.inputs.segmentation_priors = template_image_mapping["Priors2"]
    # -t
    cross_thickness_node.inputs.t1_registration_template = template_image_mapping[
        "t1_registration_template"
    ]

    # -f
    cross_thickness_node.inputs.extraction_registration_mask = template_image_mapping[
        "extraction_registration_mask"
    ]

    for key, val in config.items():
        setattr(cross_thickness_node.inputs, key, val)

    return cross_thickness_node
