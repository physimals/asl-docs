=========================
Oxford ASL User Guide
=========================

A typical usage would be::

    oxford_asl -i [asl_data] -o [output_dir] <data parameters> <analysis options> \
    -c [M0_calib] <calibration parameters> --fslanat [fsl_anat_output_dir]

This command would analyse the ASL data, including calculation of perfusion in absolute (ml/100g/min) units using the calibration data, and register the results to the strcutural image, as well as producing perfusion maps in MNI152 standard space. In general, the use of an fsl_anat analysis of a structural image with ``oxford_asl`` is recommended, but it is not required: perfusion can be calculated in the native space without the structural information.


Output
------

The outputs from Oxford_ASL are a resting state perfusion image called ``perfusion.nii.gz``, which provides blood flow in relative (scanner) units, and an arrival time image called ``arrival.nii.gz``. If a calibration image has been supplied then a further image ``perfusion_calib.nii.gz`` is also produced, which is a flow map in absolute units (ml/100g/min).

If calibration was performed then in the ``calib`` subdirectory you will find:
- In *reference region* (*single*) mode: a text file called ``M0b.txt`` will be created that saves the estimated M0 value from arterial blood. If a CSF mask was not supplied then the automatically generated one will also be saved in the output directory as ``csf_mask.nii.gz``.
- In *voxelwise* mode (automatic when no structural image is provided): a ``M0.nii.gz`` image will be produced.

Various subdirectories are created:

- ``native_space`` in which perfusion and arrival time images in the native resolution of the ASL data are saved.
- ``struct_space`` provides results in the same space as the structural image (if supplied).
- ``std_space`` provides results in MNI152 standard space (if an ``fsl_anat`` results directory has been provided).

If you find the registration to be unsatisfactory, a new registration can be performed without having to repeat the main analysis using the results in ``native_space``.

Usage
-----

Typing ``oxford_asl`` with no options will give the basic usage information, further options are revleaed by typing ``oxford_asl --more``.

-i <asl_data>  ASL data with the individual ASL images stacked in the time (4th) dimension.
-o <output_directory>  (optional)  places the results in a different directory to the current working directory.

**Main options**

-m <mask>  a brain mask in the native space of the ASL data. This will be generated automatically by ``oxford_asl``, this option is for the cases where you need your own mask.
--spatial  use spatial regularisation. This option is enable by default and is highly recommended. Use ``--spatial=off`` to disable.
--wp  Do analysis in 'White Paper Mode'. This analysis will conform to the assumptions made in the white paper about the underlying kinetic model and T1 values. Note, it still uses the Bayesian kinetic inference method in BASIL (thus spatial regularisation can be applied etc) and not the formula in the 'White Paper'.
--mc  Apply motion correction (using ``mcflirt``). This will also correct for motion between calibration image and main ASL data using an approach that minimises the interpolation applied to the main ASL data.

**Acquisition specific**

There are a number of acquisition sepecific parameters that you should set to describe your data to ``oxford_asl``. Note, it is highly unlikely that the defaults for all of these parameters will be correct for your data - in particular you should pay attention to the follwing options.

--iaf=<diff,tc,ct>  Input ASL format: specifies if the data has already been label-control subtracted (``diff``, default), or is in the form of label(tag)-control pairs (``tc`` or ``ct`` depending upon if label/tag is first).
--ibf=<rpt,tis>  Input block format. Specifically for multi-delay (multi-PLD) ASL data to identify whther the individual delays/PLDs are groups togther or by repeats of the same sequence of PLDs.
--casl  Data were acquired using cASL or pcASL labelling (pASL labeling is assumed by default).
--tis=<csv>  The list of *inflow times* (TIs), a comma separated list of values should be provided (that matches the order in the data).

  Note, the inflow time is the PLD plus bolus duration for pcASL (and cASL), it equals the inversion time for pASL.
  If the data contains multiple repeats of the same set of TIs then it is only necessary to list the unique TIs.

  When using the ``--tis=`` you can specify a full list of all TIs/PLDs in the data (i.e., as many entries as there are label-control pairs). Or, if you have a number of TIs/PLDs repeated multiple times you can just list the unique TIs in order and ``oxford_asl`` will automatically replicate that list to mathc the number of repeated measurements in the data. If you have a variable number of repeats at each TI/PLD then either list all TIs or use the ``--rpts=<csv>`` option (see below).
  
--bolus=<value>  use this to specify the duration of the ASL labeling bolus used in the sequence (in seconds). For pcASL/cASL this will be the value fixed by the sequence, for pASL this will be taken as the inital value for bolus duration estimation (unless the ``--fixbolus``) option is specified.
--bolus=<csv>  alternatively supply a list of bolus duration for each TI/PLD in the data (the length of the list should match that provided to ``--tis=``).
--slicedt=<value>  For multi-slice (2D) acquisitions where superior slices are acquired later than those below, this option does not apply to 3D readouts. This provides the increase in time (in seconds) after labeling for a superior slice relative to the one directly below. It is assumed that the TIs provided refer to the lowest slice in the dataset.

There are further acquisition specific parameters that you might need to invoke depending upon your data, although the defaults here are more likely to apply.

--bat=<value>  A value for Arterial Transit Time (ATT), here called Bolus Arrival Time (BAT). For single delay/PLD ASL this is the value used in the perfusion calculation (and it is set to 0 in 'White Paper Mode'). For multi-delay/PLD ASL this value will be used to initialise the estimation of ATT from the data. Typically, the ATT is longer in pcASL compared to pASL. The defaults are 0.7 s for pASL and 1.3 s for pcASL based on typical experience.
--t1=<value>  The T1 value of tissue, 1.3 s by default (assuming acquisition at 3T).
--t1b=<value>  The T1 value of arterial blood, 1.65 s by default (assuming acquisition at 3T).
--sliceband=<number>  Number of slices per band in a multi-band acquisition.
--rpts=<csv>  Number of repeated measurements for each TI/PLD in the TIs list (``--tis=<csv>``), for use where the number of repeated measurements varies at each TI.

**Structural image**

The inclusion of a structural image is optional but highly recommended, as various useful pieces of information can be extracted when this image is used as part of ``oxford_asl``, and partial volume correction can be done. Generally, we recommend the use of ``fsl_anat`` to process the structural image prior to use with ``oxford_asl``.

--fslanat=<directory>  An ``fsl_anat`` results directory from the structural image (Note that ideally brain extraction and segmentation will have been performed, ``oxford_asl`` will also use the bias field correction if present).
-s <image>  High resolution structural image (assumed to be T1 weighted or similar). An alternative to ``--fslanat``, if neither is not provided then results will be provided in native space only. Also requires the provision of a brain extracted version of the image with ``--sbrain``.
--sbrain=<image>  Brain extracted (e.g., using ``bet``) version of the structural image.
--fastsrc=<image_stub>  The results of a ``fast`` segmentation of the structural image. This option is an alternative to ``--fslanat`` for entering partial volume estimates (and bias field), in the same space as the structural image, into ``oxford_asl``. It presumes the images will be presented with the same naming syntax as a ``fast`` output, but any alternative source of partial volume estimates could be used.
--senscorr  Instruct ``oxford_asl`` to use the bias field map from ``fsl_anat`` or ``fast`` for coil sensitivity correction where this hasn't been done on the scanner or there isn't a separate correction available.

**Calibration**

Most commonly you will have a calibration image that is some form of (approximately) proton-density-weighted image and thus will use the ``-c`` option.

-c <M0_calib_image>  specifies the M0 calibration image that is used to get flow values in absolute units. This should be an image with any repeated measurements stacked in the 4th (time) dimension.
--tr=<value>  the repetition time for the calibration image.
--alpha=<value>  the inversion efficiency of the labeling process, the defaults are likely to apply for most ASL data: 0.98 (pASL) or 0.85 (pcASL/cASL)
--cmethod=<single,voxel>  Specifies whether the calibration is done via a single M0 value calculated from the CSF in the ventricles (``single``) or using a voxelwise approach where M0 is calcuated in every voxel (``voxel``).

  The voxelwise method is the simplest and follows the procedure in the 'White Paper', adding a correction for partial volume effects around the edge of the brain. This is is used whenever a structural image is not supplied.
  The single method, using CSF for calibration, automatically generates a ventricle mask in ASL space from the segmentation of the structural image. You should inspect this mask to ensure it has been sucessful (in the ``calib`` subdirectory of the results). This procedure can sometimes fail, in which case you can supply your own mask using the ``--csf`` option.
  More advanced calibration can be performed using ``asl_calib``.

--M0=<value>  A single precomputed value for the value of equilbirum magnetization in arterial blood. Useful when you have already performed calibration, e.g. using ``asl_calib``.

There are further advanced/extended options for calibraiton:

--csf=<image>  Image in the same space as the structural that is a mask of voxels containing CSF to be used in calibration. This is a further option of the calibration step and allows the CSF mask to be manually specified if the automated procedure fails.
--cgain=<value>  If the calibration image has been acquired with a different gain to the ASL data this can be specified here. For example, when using background suppression the raw ASL signal will be much smaller than the (non background suppressed) calibration image so a higher gain might be employed in the acquisition.
--t1csf=<value>  Supply a value for the T1 of CSF to be used in the calibration process. Default values are used by asl_calib based on a 3T field strength (these can be checked by calling ``asl_calib`` at the command line).
--te=<value>  Set the echo time (in milliseconds) for the readout so that T2 (or T2*) effects are taken into account in the calibration. If this is not supplied then TE = 0 ms is assumed, i.e. T2/T2* effects are negligible. Default values are assumed by asl_calib for T2/T2* values, you might wish to treat these with caution as these are estimates based on the literature.
--t2star  Tells oxford_asl to correct for T2* rather than T2 effects. This simply tells ``asl_calib`` to use the default values for T2* in place of T2 in the calculations.
--t2csf=<value>  Supply a value for the T2 (in milliseconds) of CSF to be used in the calibration process, only relevant if you supply the TE value. Default values are used by ``asl_calib`` based on a 3T field strength (these can be checked by calling ``asl_calib`` at the command line).
--t2bl=<value>  Supply a value for the T2 of blood to be used in the calibration process, only relevant if you supply the TE value. Default values are used by ``asl_calib`` based on a 3T field strength (these can be checked by calling ``asl_calib`` at the command line).

**Registration**

There are some extended options (to be used alongside a structural image) for the purposes of registration.

--asl2struc=<mat>  an existing ASL to structural image transformation matix, skips the registration process.
-r <image>  low resolution structural image used as an extra step in the registration to improve resulting transformation.
--regfrom=<image>  An alternative image to use as the basis of registration. This should be the same resolution as the ASL data and aligned to it. 

**Kinetic Analysis**

--artoff  Turn off correction for signal arising from ASL signal still within the (macro) vasculature, this might be appropriate if the acquisition employed flow suppression. This is enabled by default for single-delay/PLD ASL.
--fixbolus  Turn off the automatic estimation of bolus duration, this might be appropriate if the bolus duration is well defined by the acquisition sequence and is on by default for cASL and pcASL. It might be appropriate to use this with pASL where the bolus duration has been fixed using QUIPSSII or Q2TIPS.
--fixbat  Force basil not to infer the ATT (BAT), this is on by default for single-delay/PLD ASL.
--batsd  The standard deviation for the ATT (BAT) prior distribution (default 0.316 seconds for single-PLD, 1.0 second for multi-PLD). See BASIL command line user guide for more information.
--infert1  Incorporate uncertainty in the T1 values into the analysis. Strictly this inlcudes the T1 values in the inference process, but dont expect accurate T1 maps from ASL data.
--noiseprior  Use the in-built informative prior for noise estimation. This is particuarly useful where you only have a small number of repeats/volumes in the main ASL data (e.g., if your data has already been averaged before you get it). This provides information to ``basil`` about the typical noise present in ASL data and helps with the application of appropriate spatial regularisation.
--noisesd  The standard deviation of the noise as described by the noise prior, overrides the values set internally and needs to be of the form of the standard deviation of the noise relative to the magnitude of the ASL data (only for very advanced use).


**Distortion Correction**

Distortion correction for (EPI) ASL images follows the methodology used in BOLD EPI distortion correction.

Using a separately acquired fieldmap (structural image is required), this can in principle be in any image space (not necessarily already alinged with the ASL or structural image), the syntax follows ``epi_reg``:

--fmap=<image>  fieldmap image (in rad/s)
--fmapmag=<image>  fieldmap magnitude image - wholehead extracted
--fmapmagbrain=<image>  fieldmap magnitude image - brain extracted
--echospacing=<value>  effective EPI echo spacing (sometimes called dwell time) - in seconds
--pedir=<dir>  phase encoding direction, dir = x/y/z/-x/-y/-z
--nofmapreg  do not perform registration of fmap to T1 (use if fmap already in T1-space)

Further information on fieldmaps can be found under the ``fsl_prepare_fieldmap`` documentation on the FSL webpages.
 
Using phase-encode-reversed calibration image (a la ``topup``):
 
--cblip  phase-encode-reversed (blipped) calibration image
--echospacing=<value>  Effective EPI echo spacing (sometimes called dwell time) - in seconds
--pedir=<dir>  phase encoding direction, dir = x/y/z/-x/-y/-z

For ``topup`` the effective EPI echo spacing is converted to total readout time by multiplication by the number of slices (minus one) in the encode direction. Earlier versions of oxford_asl (pre v3.9.22) interpreted the ``--echospacing`` parameter as total readout time when supplied with a phase-encode-reversed calibration image.

**Partial volume correction**

Correction for the effect of partial voluming of grey and white matter, and CSF can be performed using ``oxford_asl`` to get maps of 'pure' grey (and white) matter perfusion. When partial volume correction is performed a separate subdirectory (``pvcorr``) within the main results subdirectories will appear with the corrected perfusion images in: in this directory the ``perfusion.nii.gz`` image is for grey matter, ``perfusion_wm.nii.gz`` contains white matter estimates. Note that, the non-corrected analysis is always run prior to partial volume correction and thus you will also get a conventional perfusion image.

 --pvcorr    : Do partial volume correction
 
  PV estimates will be taken from:
  
  - fsl_anat dir (``--fslanat``), if supplied
  - exising fast segmentation (``--fastsrc``), if supplied
  - FAST segmenation of structural (if using `-s` and `--sbet`)
  - User supplied PV estimates (--pvgm, --pvwm)
   
   --pvgm    : Partial volume estimates for GM
   --pvwm    : Partial volume estimates for WM

**Epoch analysis**

The data can also be analysed as separate epochs based on the different measurements (volumes) within the ASL data. This can be a useful way of examining changes in perfusion over the duration of the acquisition, although shorter epochs will contain fewer measurements and thus be more noisy. Epoch analysis is always preceeded by a conventional analysis of the full data and thus the conventional perfusion image will also be generated from the full dataset.

--elen  Length of each epoch in TIs.
--eol   Overlap of each epoch in TIs (default is 0).
