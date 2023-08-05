import os
import re
from pathlib import Path

from nipype.interfaces.ants.base import ANTSCommand, ANTSCommandInputSpec
from nipype.interfaces.base import (
    BaseInterface,
    BaseInterfaceInputSpec,
    TraitedSpec,
    traits,
)
from nipype.interfaces.base.traits_extension import Directory, File, InputMultiPath
from nipype.utils.filemanip import split_filename

from fw_gear_ants_dbm_longitudinal.utils import parse_and_zip_directory


class DBMLongitudinalCorticalThicknessInputSpec(ANTSCommandInputSpec):
    dimension = traits.Enum(
        3,
        2,
        argstr="-d %d",
        usedefault=True,
        desc="2 or 3 (for 2- or 3-dimensional image)",
    )
    anatomical_image = InputMultiPath(
        File(exists=True),
        mandatory=True,
        argstr="%s",
        desc=(
            "Set of multimodal input data assumed to be specified ordered as follows: "
            "\${time1_modality1} \${time1_modality2} ... \${time1_modalityN} \ "
            "\${time2_modality1} \${time2_modality2} ..."
            "."
            "."
            "."
            "\${timeN_modality1} ..."
            "A single modality is expected by default, in which case the input images are simply ordered by time:"
            "\${time1_modality1} \${time2_modality1} ... \${timeN_modality1}"
            "If there are multiple modalities, use the -k option to specify how many."
        ),
        position=-1,
    )
    brain_segmentation_template = File(
        exists=True,
        argstr="-e %s",
        desc=(
            "Anatomical *intensity* template. This template is *not* skull-stripped."
            "The following images must be in the same space as this template:"
            "   * Brain probability mask (-m)"
            "   * Segmentation priors (-p)."
            "If used, the following optional images must also be in the same space as"
            "this template:"
            "* Registration metric mask (-f)."
        ),
        mandatory=True,
    )
    brain_extraction_probability_mask = File(
        exists=True,
        argstr="-m %s",
        desc=(
            "Brain *probability* mask in the segmentation template space. A binary mask"
            " is an acceptable probability image."
        ),
        copyfile=False,
        mandatory=True,
    )
    brain_segmentation_priors = InputMultiPath(
        File(exists=True),
        argstr="-p %s",
        mandatory=True,
        desc=(
            "Tissue *probability* priors corresponding to the image specified"
            "with the -e option.  Specified using c-style formatting, e.g."
            "-p labelsPriors%02d.nii.gz.  We assumpriors_template_dire that the first four priors"
            "are ordered as follows"
            "  1:  csf"
            "  2:  cortical gm"
            "  3:  wm"
            "  4:  deep gm."
        ),
    )
    out_prefix = traits.Str(
        "antsL_",
        argstr="-o %s",
        desc=(
            "The following subdirectory and images are created for the single"
            "subject template"
            "* \${OUTPUT_PREFIX}SingleSubjectTemplate/"
            "* \${OUTPUT_PREFIX}SingleSubjectTemplate/T_template*.nii.gz"
            "A subdirectory is created for each anatomical image."
        ),
        mandatory=True,
    )
    # Optional args

    image_suffix = traits.Str(
        "nii.gz",
        desc=("any of standard ITK formats," " nii.gz is default"),
        usedefault=True,
    )
    control_type = traits.Int(
        default_value=2,
        desc=(
            "Control for parallel computation (default 0):"
            "0 = run serially"
            " 1 = SGE qsub"
            "2 = use PEXEC (localhost)"
            "3 = Apple XGrid"
            "4 = PBS qsub"
            "5 = SLURM."
        ),
        argstr="-c %d",
        usedefault=True,
        mandatory=True,
    )

    t1_registration_template = File(
        exists=True,
        desc=(
            "Anatomical *intensity* template"
            "This template *must* be skull-stripped."
            "This template is used to produce a final, high-quality registration between"
            "the skull-stripped single-subject template and this template."
        ),
        argstr="-t %s",
        mandatory=False,
    )

    atlases = traits.Str(
        desc=(
            "Atlases (assumed to be skull-stripped) used to cook template priors. If atlases aren't used then "
            "we simply smooth the single-subject template posteriors after"
            "passing through antsCorticalThickness.sh. Example: "
            "-a atlas1.nii.gz -a atlas2.nii.gz ... -a atlasN.nii.gz"
        ),
        argstr="-a %s",
        mandatory=False,
    )

    atlases_label = traits.Str(
        desc=(
            "Labels associated with each atlas, in the same order as they are specified"
            "with the -a option. The number of labels in each image is assumed to be equal"
            "to the number of priors."
        ),
        argstr="-l %s",
        mandatory=False,
    )

    extraction_registration_mask = File(
        exists=True,
        argstr="-f %s",
        desc=(
            "Binary metric mask defined in the segmentation template space (-e). During the"
            "registration for brain extraction, the similarity metric is only computed within"
            "this mask."
        ),
        mandatory=True,
    )
    denoise_anatomical_images = traits.Int(
        desc=("Denoise anatomical images (default = 0)."),
        argstr="-g %d",
        usedefault=True,
        mandatory=True,
        default_value=1,
    )
    num_cores = traits.Int(
        argstr="-j %d",
        desc=(
            "Number of cpu cores to use locally for pexec option (default 2; requires '-j 2')."
        ),
        usedefault=True,
        default_value=2,
        mandatory=False,
    )
    num_modalities = traits.Int(
        argstr="-k %d",
        default_value=1,
        desc=(
            "Number of modalities used to construct the template (default 1)"
            "For example, if one wanted to use multiple modalities consisting of T1, T2, and FA components ('-k 3')."
        ),
        usedefault=True,
        mandatory=True,
    )
    sst_cortical_thickness_prior = traits.Enum(
        0,
        1,
        argstr="-n %d",
        desc=(
            "If set to '1', the cortical thickness map from the single-subject template is used"
            "as a prior constraint for each of the individual calls to antsCorticalThickness.sh"
            "(default = 0)"
        ),
        mandatory=False,
    )
    float_precision = traits.Enum(
        0,
        1,
        argstr="-u %d",
        desc=("If 1, use single float precision in registrations (default = 0)."),
        mandatory=False,
    )
    atropos_seg_weight_sst = traits.Float(
        argstr="-v %d",
        desc=(
            "Atropos spatial prior *probability* weight for the segmentation of the"
            "single-subject template (default = 0.25)."
        ),
        default_value=0.25,
        mandatory=False,
    )

    atropos_seg_weight_indiv = traits.Float(
        argstr="-w %d",
        desc=(
            "Atropos spatial prior *probability* weight for the segmentation of the individual"
            "time points (default = 0.5)."
        ),
        default_value=0.5,
        mandatory=False,
    )
    atropos_iteration = traits.Int(
        argstr="-x %d",
        desc=("Number of iterations within Atropos (default 5)."),
        default_value=5,
        mandatory=True,
    )
    quick_registration = traits.Int(
        argstr="-q %d",
        desc=(
            "Use antsRegistrationSyNQuick.sh for some or all of the registrations."
            "The higher the number, the more registrations are performed quickly. The options are"
            "as follows:"
            "-q 0 = antsRegistrationSyN.sh for everything (default)"
            "-q 1 = Quick registration of time points to the SST"
            "-q 2 = Adds quick registrations for prior cooking"
            "-q 3 = Quick registrations throughout."
        ),
        default_value=0,
        mandatory=False,
    )
    rigid_alignment = traits.Enum(
        0,
        1,
        argstr="-r %d",
        mandatory=True,
        use_default=True,
        desc=(
            "If 1, register anatomical images to the single-subject template before processing"
            "with antsCorticalThickness. This potentially reduces bias caused by variable"
            "orientation and voxel spacing (default = 0)."
        ),
    )
    keep_temporary_files = traits.Int(
        argstr="-b %d",
        desc="Keep brain extraction/segmentation warps, etc (default = 0).",
        default_value=0,
        mandatory=False,
        use_default=True,
    )

    rigid_template_update_component = traits.Enum(
        0,
        1,
        desc=(
            "Update the single-subject template with the full affine transform (default 0)."
            "If 1, the rigid component of the affine transform will be used to update the"
            "template. Using the rigid component is desireable to reduce bias, but variations"
            "in the origin or head position across time points can cause the template head to"
            "drift out of the field of view."
        ),
        argstr="-y %d",
        use_default=True,
        mandatory=True,
    )


class DBMLongitudinalCorticalThicknessOutputSpec(TraitedSpec):
    SingleSubjectTemplateDir = Directory(
        exists=True,
        desc="Directory that contains SingleSubjectTemplate files",
        resolve=False,
    )
    TimePointDir = Directory(
        exists=True,
        desc="Directory that contains templates from various timepoint",
        resolve=False,
    )


class DBMLongitudinalCorticalThickness(ANTSCommand):
    """Wrapper for antsLongitudinalCorticalThickness.sh executable script."""

    input_spec = DBMLongitudinalCorticalThicknessInputSpec
    output_spec = DBMLongitudinalCorticalThicknessOutputSpec
    _cmd = "antsLongitudinalCorticalThickness.sh"

    def _format_arg(self, opt, spec, val):
        if opt == "anatomical_image":
            dir_name, _, ext = split_filename(self.inputs.anatomical_image[0])
            retval = f" {dir_name}/*" + ext
            return retval
        if opt == "brain_template":
            retval = "-e %s" % val
            return retval
        if opt == "brain_extraction_probability_mask":
            retval = "-m %s" % val
            return retval
        if opt == "out_prefix":
            retval = "-o %s" % val
            return retval
        if opt == "t1_registration_template":
            retval = "-t %s" % val
            return retval
        if opt == "brain_segmentation_priors":
            # Generate customized file
            priors_count = len(self.inputs.brain_segmentation_priors)
            leading_zero = (
                True
                if self.inputs.brain_segmentation_priors[0].startswith("0")
                else False
            )
            if priors_count < 10:
                wildcard_format = "%0d" if leading_zero else "%d"
            else:
                wildcard_format = "%02d" if leading_zero else "%2d"

            dirname, filename, ext = split_filename(
                self.inputs.brain_segmentation_priors[0]
            )
            priors_filename = re.sub("\d", wildcard_format, filename)
            retval = f"-p {dirname}/{priors_filename}" + ext
            return retval
        return super(DBMLongitudinalCorticalThickness, self)._format_arg(opt, spec, val)

    def _run_interface(self, runtime, correct_return_codes=None):

        if correct_return_codes is None:
            correct_return_codes = [0]
        runtime = super(DBMLongitudinalCorticalThickness, self)._run_interface(runtime)
        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        out_prefix = self.inputs.out_prefix
        outputs["SingleSubjectTemplateDir"] = os.path.join(
            os.getcwd(), out_prefix + "SingleSubjectTemplate"
        )
        outputs["TimePointDir"] = os.path.join(os.getcwd(), out_prefix)

        return outputs


class antsLResultsGeneratorInputSpec(BaseInterfaceInputSpec):
    SSTemplateDir = Directory(
        exists=True,
        desc="Directory that contains SingleSubjectTemplate files",
        resolve=False,
    )
    TPDir = Directory(
        exists=True,
        desc="Directory that contains templates from various timepoint",
        resolve=False,
    )


class antsLResultsGeneratorOutputSpec(TraitedSpec):
    SingleSubjectTemplateArchive = File(exists=True, resolve=False)
    TimePointTemplateArchive = File(exists=True, resolve=False)
    OutputFilesInfo = File(exists=True, resolve=False)


class antsLResultsGenerator(BaseInterface):
    """
    Interface to process antsLongitudinalCorticalThickness.sh executable output files.
    This interface will parse through the template directory and generate a zip archive with desired output files.
    A text file of a detailed information of the output files will be produced in this interface as well.
    """

    input_spec = antsLResultsGeneratorInputSpec
    output_spec = antsLResultsGeneratorOutputSpec

    def _run_interface(self, runtime):

        parse_and_zip_directory(
            self.inputs.SSTemplateDir, summary_file="antsL_output_files_info.txt"
        )
        parse_and_zip_directory(
            self.inputs.TPDir, summary_file="antsL_output_files_info.txt"
        )

        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()

        sst_dir = Path(self.inputs.SSTemplateDir)
        tp_dir = Path(self.inputs.TPDir)
        outputs["SingleSubjectTemplateArchive"] = os.path.join(
            os.getcwd(), sst_dir.name + ".zip"
        )
        outputs["TimePointTemplateArchive"] = os.path.join(
            os.getcwd(), tp_dir.name + ".zip"
        )
        outputs["OutputFilesInfo"] = os.path.join(
            os.getcwd(), "antsL_output_files_info.txt"
        )

        return outputs
