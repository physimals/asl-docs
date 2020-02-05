======================================
QUASIL - quantification of QUASAR data
======================================

Overview
========

QUASIL is a special implementation of BASIL specifically designed to exploit the features of QUASAR ASL data. It uses the same two component (tissue plus macro vascular signal) model that is employed by BASIL, but it has been extended to use all the information provided by the various phases for flow suppression provided by the QUASAR sequence. QUASIL uses information from the full QUASAR dataset to produce CBF images in absolute units (using an implementation of ``asl_calib``). QUASIL also provides the option to perform a 'model-free' analysis using a very similar methodology as presented in the original QUASAR paper.

More information on the model used can be found in:

  *Chappell, M. A., Woolrich, M. W., Petersen, E. T., Golay, X., & Payne, S. J. (2012). Comparing model-based and model-free analysis methods for QUASAR arterial spin labeling perfusion quantification. Magnetic resonance in medicine. doi:10.1002/mrm.24372*

More information on the model-free method can be found in the original QUASAR paper:

 *Petersen, E., Lim, T., & Golay, X. (2006). Model-free arterial spin labeling quantification approach for perfusion MRI. Magnetic resonance in medicine , 55(2), 219–232. doi:10.1002/mrm.20784*

User Guide
==========

Usage
-----

Since the acquisition of data using QUASAR is very well defined there are far fewer options to set with QUASIL than a typical BASIL analysis. NOTE that QUASIL expects the data without tag-control subtraction having been performed. A typical command line usage would be::

    quasil -i <asl_data> -o <output_directory>
 
This would carry out a model-based analysis of the ASL data and provide voxelwise estimates of perfusion, arterial transit time and arterial blood volume (aBV). The calibration of the data to the equilibrium magnetization is also carried out as part of the processing so that the perfusion image is provided in absolute units (ml/100ml/min). Additionally, the perfusion image prior to calibration is also provided: ``perfusion_raw``.

Typing quasil with no options will give basic usage information.

Main options
----------------

-i <image>  The QUASAR ASL data in Nifti file format. The data order should 'as acquired', i.e. as blocks of TIs measured in the different phases of flow suppression.
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
