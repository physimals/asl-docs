=====================
TOAST User Guide
=====================

Usage
-----

TOAST expects the input data without label-control subtraction being performed. A typical command line usage would be::

    toast -i <asl_data> -o <output_directory>  --infert1
 
This would carry out a model-based analysis of Turbo-QUASAR data and provide voxelwise quantification of perfusion and arterial transit time. Note: the current implementation of TOAST does NOT support dispersion correction, model-free analysis, or partial volume correction.

Output files
----------------

The main output files are (some of them are only available when using certain options)

<ABV_absolute>  Arterial blood volume in decimals after calibration

-i <ABV_absolute>  The QUASAR ASL data in Nifti file format. The data order should 'as acquired', i.e. as blocks of TIs measured in the different phases of flow suppression.
-o <directory>  Use this to place the result in a different directory to the current working directory.
-m <image>  Use this to provide a brain mask in which data analysis should take place. If this is not set, a mask will be generated automatically from the data.

Calibration
-----------

The calibration is carried out by ``asl_calib`` and uses the saturation recovery of the control images. M0 of the tissue is estimated voxelwise from fitting a saturation recovery model and from this a voxelwise estimate of M0 of the blood is derived and applied to the estimated perfusion images. More details are given in the references. An alternative is to calculate the M0 of CSF within a CSF mask and from this estimate a single value of M0 of arterial blood, as is done by ``oxford_asl`` by default. This can be achieved using ``asl_calib`` and the resulting M0 value applied to the ``perfusion_raw`` image.

Sequence parameters
---------------------------

For the most part the QUASAR sequence is pretty much defined by the roignal pubplication and thus you are likely to use a version where all the parameters match the default assumed by ``quasil``. However, there is the option to input values if your sequence is different from the standard one.

--slicedt  Increase in inversion time with slice (default is 0.035 s)
--fa  Flip anlge used in the look-locker readout (default is 35 degrees)
--lfa  Flip anlge used for the 'low flip anlge' phase (default 11.7 degrees)
--tis  Comma separated list of inversion time values (default: 0.04,0.34,0.64,0.94,1.24,1.54,1.84,2.14,2.44,2.74,3.04,3.34,3.64)

Extended options
------------------------

--t1b  use this to set the value of T1 of arterial blood (1.65 s by default).
--disp  Includes the effects of label dispersion in the model (using a gamma vascular transport function)
--infertau  Also estiamte the label duration from the data (rather than assuming it be be fixed by the sequence).
--corrcal  Inlcude correction for partial volume effects present around the edges of the calibration image.
--mfree  Do a 'model-free' rather than model based analysis of the data.

Partial Volume Correction
--------------------------

It is posisble to perform model-based partial volume correction with QUASAR ASL using the same methodology available in BASIL for other ASL variants.

--pvcorr  Do partial voluem correction, requires structural image and its segmentation results.
--fslanat  An ``fsl_anat`` results directory to supply ``quasil`` with a structural image and the results of segmentation.
--t1wm  The value of T1 to be used fro white matter (default 1.1 seconds)
