"""The interfaces module
Temporary resolution to fix bug with dcm2niix not escaping metacharacters in filename.
"""
import glob
import os
import re
from copy import deepcopy

from nipype.interfaces.base import traits
from nipype.interfaces.dcm2nii import Dcm2niix, Dcm2niixInputSpec


class Dcm2niixInputSpecEnhanced(Dcm2niixInputSpec):
    # Current dcm2niix NiPype interface does not support the merge2d
    merge_imgs = traits.Enum(
        0,
        1,
        2,
        default=2,
        argstr="-m %s",
        desc="merge 2D slices from same series regardless of echo, exposure, etc. "
        "(0=no, 1=yes, 2=auto, default 2)",
    )


class Dcm2niixEnhanced(Dcm2niix):

    input_spec = Dcm2niixInputSpecEnhanced

    def _format_arg(self, opt, spec, val):
        """Same as parent but without merge_imgs"""
        bools = [
            "bids_format",
            "single_file",
            "verbose",
            "crop",
            "has_private",
            "anon_bids",
            "ignore_deriv",
            "philips_float",
            "to_nrrd",
        ]
        if opt in bools:
            spec = deepcopy(spec)
            if val:
                spec.argstr += " y"
            else:
                spec.argstr += " n"
                val = True
        if opt == "source_names":
            return spec.argstr % (os.path.dirname(val[0]) or ".")
        return super(Dcm2niix, self)._format_arg(opt, spec, val)

    def _parse_stdout(self, stdout):
        filenames = []
        for line in stdout.split("\n"):
            # if line.startswith("Convert "):  # output
            if "Convert " in line:  # output
                # dcm2niix stdout has a formatting issue that leads to lines that reads like
                # "Warning: Intensity scale/slope using 0028,1053 and 0028,1052Convert 1 DICOM as /flywheel/v0/work/..."
                # and "scale/slope" gets incorrectly extracted as a filepath
                # PR submitted to dcm2niix https://github.com/rordenlab/dcm2niix/pull/584
                res = re.findall(r"\S+/\S+", line)
                fname = [s for s in res if s != "scale/slope"][0]
                # Temporary fix - MR on nipype to fix this issue https://github.com/nipy/nipype/pull/3417
                fname = glob.escape(fname)
                filenames.append(os.path.abspath(fname))
        return filenames
