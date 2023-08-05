"""The interface module

Redefining CorticalThickness interface to align with FW usage.

"""
import logging as log
import os
import re

import fw_utils
from nipype.interfaces.ants.segmentation import (
    ANTSCommand,
    CorticalThickness,
    CorticalThicknessInputSpec,
)
from nipype.interfaces.base import traits
from nipype.utils.filemanip import split_filename

logger = log.getLogger(__name__)


class CorticalThicknessEnhancedInputSpec(CorticalThicknessInputSpec):
    denoise_anatomical_images = traits.Int(
        desc=("Denoise anatomical images (default = 0)."),
        argstr="-g %d",
        usedefault=True,
        mandatory=True,
        default_value=1,
    )
    max_iterations = traits.Str(
        argstr="-i %s",
        desc=("ANTS registration max iterations (default = 100x100x70x20)"),
    )
    atropos_iteration = traits.Int(
        argstr="-x %d",
        desc=("Number of iterations within Atropos (default 5)."),
        default_value=5,
        mandatory=True,
    )
    use_floatingpoint_precision = traits.Bool(
        argstr="-j",
        desc=("Use floating point precision in registrations (default = 0)"),
    )


class CorticalThicknessEnhanced(CorticalThickness):
    input_spec = CorticalThicknessEnhancedInputSpec
    _cmd = "antsCorticalThickness.sh"

    def _format_arg(self, opt, spec, val):
        if opt == "use_floatingpoint_precision":
            if val:
                value = 0
            else:
                value = 1
            retval = f"-j {value}"
            return retval
        if opt == "b_spline_smoothing":
            if val:
                value = 0
            else:
                value = 1
            retval = f"-v {value}"
            return retval
        if opt == "anatomical_image":
            retval = "-a %s" % val
            return retval
        if opt == "brain_template":
            retval = "-e %s" % val
            return retval
        if opt == "brain_probability_mask":
            retval = "-m %s" % val
            return retval
        if opt == "out_prefix":
            retval = "-o %s" % val
            return retval
        if opt == "t1_registration_template":
            retval = "-t %s" % val
            return retval
        if opt == "segmentation_priors":
            # Generate customized file
            priors_count = len(self.inputs.segmentation_priors)
            leading_zero = (
                True if self.inputs.segmentation_priors[0].startswith("0") else False
            )
            if priors_count < 10:
                wildcard_format = "%01d" if leading_zero else "%1d"
            else:
                wildcard_format = "%02d" if leading_zero else "%2d"

            dirname, filename, ext = split_filename(self.inputs.segmentation_priors[0])
            priors_filename = re.sub("\d", wildcard_format, filename)
            retval = f"-p {dirname}/{priors_filename}" + ext
            return retval
        return super(ANTSCommand, self)._format_arg(opt, spec, val)

    def _run_interface(self, runtime, correct_return_codes=None):

        if correct_return_codes is None:
            correct_return_codes = [0]
        # inherit from ANTSCommand instead of CorticalThickness to avoid running _run_interface from CorticalThickness
        runtime = super(ANTSCommand, self)._run_interface(
            runtime, correct_return_codes=correct_return_codes
        )
        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs["BrainExtractionMask"] = os.path.join(
            os.getcwd(),
            self.inputs.out_prefix + "BrainExtractionMask." + self.inputs.image_suffix,
        )
        outputs["ExtractedBrainN4"] = os.path.join(
            os.getcwd(),
            self.inputs.out_prefix + "ExtractedBrain0N4." + self.inputs.image_suffix,
        )
        outputs["BrainSegmentation"] = os.path.join(
            os.getcwd(),
            self.inputs.out_prefix + "BrainSegmentation." + self.inputs.image_suffix,
        )
        outputs["BrainSegmentationN4"] = os.path.join(
            os.getcwd(),
            self.inputs.out_prefix + "BrainSegmentation0N4." + self.inputs.image_suffix,
        )
        posteriors = []
        posteriors_file_pattern = f"{self.inputs.out_prefix}BrainSegmentationPosteriors*.{self.inputs.image_suffix}"
        for file_ in fw_utils.fileglob(
            os.getcwd(), pattern=posteriors_file_pattern, recurse=False
        ):
            posteriors.append(file_)
        outputs["BrainSegmentationPosteriors"] = posteriors
        outputs["CorticalThickness"] = os.path.join(
            os.getcwd(),
            self.inputs.out_prefix + "CorticalThickness." + self.inputs.image_suffix,
        )
        outputs["TemplateToSubject1GenericAffine"] = os.path.join(
            os.getcwd(), self.inputs.out_prefix + "TemplateToSubject1GenericAffine.mat"
        )
        outputs["TemplateToSubject0Warp"] = os.path.join(
            os.getcwd(),
            self.inputs.out_prefix
            + "TemplateToSubject0Warp."
            + self.inputs.image_suffix,
        )
        outputs["SubjectToTemplate1Warp"] = os.path.join(
            os.getcwd(),
            self.inputs.out_prefix
            + "SubjectToTemplate1Warp."
            + self.inputs.image_suffix,
        )
        outputs["SubjectToTemplate0GenericAffine"] = os.path.join(
            os.getcwd(), self.inputs.out_prefix + "SubjectToTemplate0GenericAffine.mat"
        )
        outputs["SubjectToTemplateLogJacobian"] = os.path.join(
            os.getcwd(),
            self.inputs.out_prefix
            + "SubjectToTemplateLogJacobian."
            + self.inputs.image_suffix,
        )
        outputs["CorticalThicknessNormedToTemplate"] = os.path.join(
            os.getcwd(),
            self.inputs.out_prefix
            + "CorticalThicknessNormalizedToTemplate."
            + self.inputs.image_suffix,
        )
        outputs["BrainVolumes"] = os.path.join(
            os.getcwd(), self.inputs.out_prefix + "brainvols.csv"
        )
        return outputs
