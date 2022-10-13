=======================
Command line User Guide
=======================

Overview
--------

``oxford_asl`` is an automated command line utility that can process ASL
data to produce a calibrated map of resting state tissue perfusion. It
also includes a range of other useful analysis methods inlcuding
amongst others:

- motion correction
- registration to a structural image (and thereby a template space)
- partial volume correction
- distorition correction
- ROI analysis

If you have ASL data to analyse, ``oxford_asl`` is most likely the tool
you will want to use, unless you want a graphical user interface. In
practice, the GUI in BASIL is largely a means to construct the right
call to ``oxford_asl``.

What you will need
-------------------------
As a minimum to use ``oxford_asl`` all you need are some ASL data (label
and control pairs or already subtracted). In practice you will also most 
probably want:

- *a calibration image*: normally a proton-density-weighted image (or
  a close match) acquired with the same readout parameters as the main
  ASL data. Only once you have a calibration image can you get
  perfusion in absolute units.
- *a structural image*: it is helpful to have a structral image to pass
  to ``oxford_asl`` and if your data incldues this we strongly suggest
  you do use it with ``oxford_asl``. By preference, we strongly
  suggest you process your structural image with ``fsl_anat`` before
  passing those results to ``oxford_asl``. This is a good way to get
  all of the useful information that ``oxford_asl`` can use, and you
  can scrutinise this analysis first to check you are happy with it
  before starting your ASL analysis.
- *multi-delay ASL*: the methods in ``oxford_asl`` are perfectly
  applicable to the widely used single delay/PLD ASL acquisition. But,
  they offer particular advantages if you have multi-delay/PLD data.

Things to note
-------------------------
To produce the most robust analysis possible ``oxford_asl`` includes a
number of things in the overall analysis pipeline that you might want
to be aware of:

- *spatial regularisation*: this feature is now enabled by default for
  all analyses and applies to the estimated perfusion image. We do not
  recommend smoothing your data prior to passing to ``oxford_asl``. If
  you really want to, only do 'sub-voxel' level of smoothing.
- *masking*: ``oxford_asl`` will attempt to produce a brain mask in
  which perfusion quantification will be performed. This is normally
  derived from any structural images with which it is provided (highly
  recommened), via registration. Therefore, if the registration is
  poor there will be an impact on the quality of the mask. Where no
  structural information is provided, the mask will be derived from
  the ASL data via brain extraction, this can be somewhat variable
  depending upon your data. It is thus **always** worth examining the
  mask created. ``oxford_asl`` provides the option to input your own
  mask where you are not satisfied with the one automatically
  generated or you need a specific mask for your study.
- *registration*: ``oxford_asl`` performs the final registration
  using the perfusion image and the BBR cost function. We have found
  this to be reliable, as long as the perfusion image is of
  sufficient quality. In practice, an initial registration is done
  earlier in the pipeline using the raw ASL images and this is used
  in the mask generation step. You should **always** inspect the
  quality of the final registered images.
- *multiple repeats*: ASL data typically contains many repeats of the
  same measurement to increase the overall signal-to-noise ratio of
  the data. You should provide this data to ``oxford_asl``, and not
  average over all the repeats beforehand (unlike earlier versions of
  the tool). ``oxford_asl`` now inlcudes a pipeline where it intially
  analyses the data having done averaging over the repeats, followed
  by a subsequent analysis with all the data - to achieve both good
  robustness and accuracy. If your data has already had the repeats
  averaged, it is still perfectly reasonable to do analysis with
  ``oxford_asl``, if you have very few measurements in the data to pass
  to ``oxford_asl`` you might want to use the special 'noise prior'
  option, since this sets information needed for spatial regularisation.
- *Avanced analyses*: Partial volume correction, or analysis of the
  data into separate epochs, are avaialbe as advanecd supplementary
  analyses in ``oxford_asl``. If you choose these options
  ``oxford_asl`` will *always* run a conventional analysis first, this
  is used to intialise the subsequent analyses. This also means that
  you can get both conventional and advanced results in a single run
  of ``oxford_asl``.
- *Multi-stage analysis*: By default oxford_asl will analyse the data
  in multiple-stages where appropriate in an attempt to get as accurate and robust a
  result as possible. The main example of this is a preliminary
  analysis with the data having been averaged over multiple-repeats
  (see above). But, this also applies to the registration (see
  above). This does mean that you might find some differences in the
  results than if you did an analysis of the data yourself using a
  combination of other command line tools.

Typical Usage
-------------

Typing ``oxford_asl`` with no options will give the basic usage information, further options are revealed by typing ``oxford_asl --more``.

A typical processing run would usually look something like this:

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

**Calibrated output**

If calibration is enabled, calibrated perfusion outputs are available with the suffix ``_calib``. These contain quantified perfusion in ml/100g/min

**Whole-brain averages**

Within the ``native_space`` subdirectory, several whole-brain average values are defined:

 - ``<output>_gm_mean``: These are averages values in pure GM which by default is defined as voxels with more than 80% GM partial volume. This
 threshold can be modified using the ``--gm-thresh`` option
 - ``<output>_wm_mean``: These are averages values in pure WM which by default is defined as voxels with more than 90% WM partial volume. This
 threshold can be modified using the ``--wm-thresh`` option
 - ``<output>_cortical_gm_mean``: These are average values in cortical GM which is defined as 'pure GM' voxels (see above) that are included in 
 the Harvard-Oxford atlas Left/Right cortical mask (i.e. excluding subcortical GM).
 - ``<output>_cerebral_wm_mean``: These are average values in cerebral WM which is defined as 'pure WM' voxels (see above) that are included in 
 the Harvard-Oxford atlas Left/Right cortical mask (i.e. excluding subcortical WM).

**Normalized output **

In all spaces, normalized output is produced, regardless of whether calibrated output is also being generated. Normalized output is generated
by dividing the relative perfusion values by one of the whole brain averages defined above.

 - ``perfusion_norm`` - This is perfusion normalized by whole brain mean pure GM (perfusion_gm_mean)
 - ``perfusion_wm_norm`` - When partial volume correction is enabled, this is WM perfusion normalized by whole brain mean pure WM (perfusion_wm_mean)

Detailed usage information
--------------------------

This section contains a more in-depth look at some of the options available in oxford_asl

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
--region-analysis  Generate additional regional analysis of the perfusion map by registration of the image to standard space and comparison with regions in
the Hardvard-Oxford standard atlas.

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

**Region analysis**

Region analysis involves the generation of summary statistics for perfusion and arterial
transit time within defined brain regions, either from standard atlases or from ROI images
supplied by the user.

*Basic region analysis with oxford_asl*

If the ``--region-analysis`` option is specified an additional directory ``native_space/region_analysis`` will be created containing three files:

 - ``region_analysis.csv`` - This file contains region analysis statistics for all voxels within the brain mask
 - ``region_analysis_gm.csv`` - This file contains region analysis statistics for grey matter
 - ``region_analysis_wm.csv`` - This file contains region analysis statistics for white matter

Region analysis is performed by using the registration from the structural image to standard space from an ``fsl_anat`` run. Hence ``--fslanat`` must
be used in order to run region analysis.

The output files are in comma-separated format, suitable for loading into most spreadsheet or data processing applications. Within each region the following information is presented:

 - ``Nvoxels`` - The number of voxels identified as being within this region
 - ``Mean``, ``Std``, ``Median``, ``IQR`` - Standard summary statistics for the perfusion values within this region
 - ``Precision-weighted mean`` - The mean perfusion weighted by voxelwise precision (1/std.dev) estimates. This measure takes into account the confidence of the 
   inference in the value returned for each voxel and is a standard measure used in meta-analysis to combine results of varying levels of confidence.
 - ``I2`` - A measure of heterogeneity for the voxels within the region expressed as a percentage. A high value of I2 suggests that there is significant
   variation in perfusion *within* the region that is not attributable to the inferred uncertainty in the estimates. For a definition of I2 and an overview
   of its use in meta-analyses, see https://www.ncbi.nlm.nih.gov/pmc/articles/PMC192859/

*Definition of grey/white matter voxels*

The definition of the included data for GM/WM output files varies according to whether or not you
have included partial volume correction in your oxford_asl run.

If you have **not** used partial volume correction then GM voxels are derived from the structural
segmentation and by default includes voxels with at least 80% GM. This threshold can be modified 
using the ``--gm-thresh`` option. WM voxels are those with at least 90% WM, and again this can be
modified using ``--wm-thresh``. The intention here is to restrict the statistics to those voxels
which are near-enough 'pure' GM/WM.

If you **do** have partial volume correction, then oxford_asl will have generated separate perfusion
maps for GM and WM which (in principle) only contains the perfusion contribution from these components.
We use these single-tissue perfusion maps to generate the GM/WM statistics. However a base threshold
of 10% is used to remove voxels that contain very little of the selected tissue type, e.g. the GM
stats will ignore voxels with less than 10% GM. This is because the GM perfusion estimates in such voxels
will have very high uncertainty and could bias the statistics.

*Standard regions*

By default, statistics are generated for a standard set of regions as follows:

GM and WM segmentation maps are used to define 'pure' GM and WM ROIs thresholded at 80% and 90% respectively.
Note that these regions are included in all data files regardless of whether partial volume correction was
performed, and are independent of the separation of voxels into GM and WM described above.

A second set of GM and WM ROIs are included based on 10%+ thresholding - i.e. regions including *some* of the
corresponding tissue type.

A further set of standard regions are taken from the Harvard-Oxford cortical and subcortical atlases. 
Standard space regions are transformed to native ASL space and voxels with probability fraction > 0.5 
are considered to lie within a region. At least 10 voxels must be found in order for statistics to be 
presented.

*Using user-specified ROIs*

In many cases users will want to provide their own ROIs to generate statistics in. This is supported
via the ``--region-analysis-atlas`` option. This option can contain one or more image files (comma
separated) each of which contains a 3D label image in MNI space. Each voxel contains an integer label
and each unique integer > 1 defines a region in which to generate statistics.

To make the output more readable you can specify the names of the regions for each atlas using the 
``--region-analysis-atlas-labels`` option. Again this should be one or more file names (comma separated)
and each file contains a list of text labels, one per line. The number of labels should be equal to the
number of regions defined in the corresponding atlas image.
