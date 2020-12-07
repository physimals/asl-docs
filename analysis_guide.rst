=============================
ASL Analysis Guide
=============================

Preparatory materials
=====================

If you are new to Neuroimaging or to FSL tools you might find the
following resources helpful before looking at the material on ASL.

If you are not particularly familar with MRI you might like to
read a `Short Introduction to MRI Physics for Neuroimaging <http://www.neuroimagingprimers.org/online-appendices/>`_ 
available via the neuroimagingprimers.org website.

If you are new to FSL we recommend these three short introductory FSL 
practicals on:

  - `FSLeyes <https://www.youtube.com/watch?v=80d9FoqvuGo&list=PLvgasosJnUVku_GE64BfFuftEvh3Y8lHC&index=1>`_
  - `BET <https://www.youtube.com/watch?v=CcjBoqpgACc&index=1&list=PLvgasosJnUVku_GE64BfFuftEvh3Y8lHC>`_
  - `FSL Utils <https://www.youtube.com/watch?v=7Ud6uBuxqXY&list=PLvgasosJnUVku_GE64BfFuftEvh3Y8lHC&index=2>`_

The `FSL course <http://fsl.fmrib.ox.ac.uk/fslcourse/online_materials.html>`_
provides a wide range of videos and practical
exercises. Whilst you do not need to have looked at any of this before
the BASIL course, you might find some of it helpful background for
topics that will be covered (especially for the group analysis
section).

We would recommend familarity with:

 - Section 1: Image Registration and Distorition Correction (videos 1-5
   are all helpful)
 - Section 2: Segmentation and Structural Analysis (video 7 on FAST)
 - Section 4: Statistics & Task fMRI: Inference and Group Analysis (videos
   15-20 provide useful background on group analysis)

Bayesian Inference for Arterial Spin Labelling MRI
==================================================

.. image:: images/basil_perfusion.jpg
   :scale: 100 %
   :alt: BASIL perfusion image
   :align: right

Arterial Spin Labeling (ASL) MRI is a non-invasive method for the quantification 
of perfusion. Analysis of ASL data typically requires the inversion of a kinetic 
model of labeled blood-water inflow along with a separate calculation of the equilibrium 
magnetization of arterial blood. The BASIL toolbox provides the tools to do this 
based on Bayeisan inference principles. The toolbox was orginally developed for 
multi delay (inversion time) data where it can be used to greatest effect, but 
is also sufficiently fleixble to deal with the widely used single delay form 
of acquisition.

If you want to 
perform analysis of a functional experiment with ASL data, i.e. one where 
you want to use a GLM, then you should consult the perfusion section of 
`FEAT <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FEAT/UserGuide>`_, 
or if you have dual-echo (combined BOLD and ASL) data then consult 
`FABBER <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FABBER>`_.

For single delay ASL data kinetic model inversion is relatively trivial and 
solutions to the standard model have been described in the literature. However,
there are various advantages to aquiring ASL data at multiple times 
post-inversion and fitting the resultant data to a kinetic model. This 
permits problems in perfusion estimation associated with variable bolus arrival 
time to be avoided, since this becomes a parameter of the model whose value is 
determined from the data. Commonly the model fitting will be performed with a 
least squares technique providing parameter estimates, e.g. perfusion and bolus 
arrival time. In contrast to this BASIL uses a (fast) Bayesian inference method 
for the model inversion, this provides a number of advantages:

 - Voxel-wise estimation of perfusion and bolus arrival time along with parameter 
   variance (allowing confidence intervals to be calculated).

 - Incorporation of natural varaibility of other model parameters, e.g. values of T1,
   T1b and labeling/bolus duration.

 - Spatial regularization of the estimated perfusion image.

 - Correction for partial volume effects (where the appropriate segmentation 
   information is available).

While the first two apply specfically to the case of mulitple delay data, the latter 
are also applicable to single delay ASL and are only available using the Bayesian 
technique employed by BASIL.

ASL analysis principles
=========================

The generation of a perfusion-weighted image from ASL data is relatively simple, requiring the pair-wise subtraction of label and control images to leave the contribution of labelled blood-water delivered by the vasculature. Since the magnitude of the signal directly relates to the delivery of blood, the image created is itself perfusion-weighted. To go beyond the perfusion weighted image, and generate quantitative voxelwise measures of perfusion with values in the typical units of ml/100 g/min, we need an analysis scheme that would look like the following:

* Subtraction.
* Kinetic Modelling.
* Calibration.

Subtraction
-------------------------------

Central to ASL analysis is the subtraction of label and control images. Both label and control images will contain some signal from brain tissue - called the static tissue signal (this is true even if background suppression has been used to reduce this contribution). Subtraction of the label-control pair reveals the contribution from labelled blood-water. This image is often referred to as the difference image and is perfusion-weighted, which means it reflects the perfusion in each voxel, but the intensity value in each voxel does not alone provide an absolute measure of perfusion.

Kinetic Modelling
--------------------------------
The voxel intensity in an ASL difference image is directly related to the labelled blood-water. More accurately, it relates to the amount of labelled blood-water that has accumulated in the voxel in the time between creation of the label and the collection of a brain image. This means that it is a measure of delivery and thus perfusion, rather than blood volume or blood flow rate. To be able to say how much labelled blood has been delivered, and thus what the perfusion is, it is necessary to describe the delivery process, as well as what happens to the labelled blood once it has been delivered. This is achieved by means of a kinetic model.

At its very simplest the kinetic model for labelled blood-water in an ASL study needs to account for the delivery of a finite duration (the label duration) of labelled blood-water into the voxel where it accumulates. At the same time as it is being delivered, the label is also decaying away. THe tracer decays at a rate defined by the T1 time constant, which is of the order of a second in the brain at typical MRI field strengths. The kinetic model allows the relationship between the signal and perfusion to be expressed as an equation and this can be rearranged to give an equation that takes signal magnitude and returns perfusion, or fit to the data using optimisation techniques.

Calibration
--------------------------------
The ASL calculation relies on knowledge of the tracer concentration, strictly the quantity called the equilibrium magnetization of arterial blood, which will vary between individuals and other MRI-related factors (e.g. the main magnetic field strength). The simplest approach for estimating this parameter is by the acquisition of a separate proton-density-weighted image. This can be converted to a measure of arterial magnetization by accounting for the relative density of hydrogen nuclei in tissue and blood (the partition coefficient). Various corrections can be performed where the calibration image is not a pure proton-density weighted image, e.g., where it has a (realtively) short repetition time.

Key ASL data parameters
============================

There are various parameters associated with an ASL acquisition. Some of which are important for the quantification/analysis process. Whilst you do not necessarily need to know all of the details of an ASL acquisition to be able to extract a perfusion image, you should at least find out the following information before attempting analysis.

pcASL or pASL
-----------------------------------

The labelling may either have been pseudo-continuous ASL (pcASL, most common) or pulsed ASL (pASL). There are important differences between these two forms of ASL that affect the kinetic model used and thus you need to tell BASIL which one you have.

Post-label delay(s)
------------------------------------

After labeling a delay is left for the labeled blood-water to travel into the brain. For pcASL this is called the Post-Label Delay (PLD) and is the time from the *end* of the label duration (see `Label duration`_) until imaging. For pASL the labeling process is instantaneous and it is more common to refer to the inversion time (TI). For the BASIl GUI you are asked for PLD value(s) for pcASL and TI for pASL. However, the command line tools primiarly use the common delay measure: the inflow time (also TI), the time from the *start* of labeling. This is identical to the inversion time for pASL, but for pcASL is the sum of the label duration and PLD:

cASL or pcASL: TI = PLD + Label duration

It is quite common to meet ASL data with multiple repeats/measurements (and thus volumes in the resulting images) that all have the same PLD (or TI) - single delay ASL. It is, however, possible to use a range of different PLD in an acquisition in an attempt to extract more information, or achieve a better SNR - multi-delay (multi-PLD) ASL. BASIL can process both forms of ASL and the various tools have been designed so that you can specify either the numer ofs TIs in the data (``asl_file``) or a list of values (e.g., ``oxford_asl``). When you have multi-delay ASL you will also obtain an estimate of the arterial transit time (ATT), which will be provided as an extra output from BASIL and ``oxford_asl``.

Label duration
-------------------------------------

The label (or bolus) duration is an important measure of how much labeled-blood water has been delivered to the tissue and is thus important for quantification. For pcASL the value is set by the sequence and thus is something you need to know. It is quite common to use a 1.8 second (or longer) label duration with pcASL.

In principle in pASL the label duration is unknown (a spatial region is labeled instead of a known duration of flowing blood). You may find that your pASL acquisition is using Q2TIPS or QUIPSSII, in which case the label duration has been set using extra pulses. Quite often the value of label duration can then be determined from the associated parameter, often called TI2 - a value of 0.7 or 0.8 seconds would be quite normal. Where the label duration is genuinely unknown (e.g. a FAIR pASL acquisition), BASIL can attempt to estimate it as long as the data is multi-TI. In practice, BASIL automatically estimates the label duration for all multi-TI pASL data, since it is possible with Q2TIPS/QUIPSSII that the duration will be shorter than expected due to high flow in the labelling region.

ASL variants
=======================

Hadamard/Time-encoded ASL
--------------------------------------
This is a form of pcASL where the label ling performed via a series of sub-labels with shorter duration. Individual volumes in the ASL acquisition will vary whether for given periods during the label duration labeling is actually taking palce or not. This is normally done accoridng to a specific sceme that means that adter decoding it is posisble to recover multi-PLD data that appears as if it has been collected with a PLD equal to the sub-label duration. Even more advanced versions vary the sub-label durations.

It is posisble to directly analyse some forms of TE-ASL directly using BASIL (the command line tool). Otherwise, to analyse this data in BASIL you can first perform the decoding step to reveal the multi-PLD data. Thereafter this can be used in BASIL (and associated tools) treating the data as label-control subtracted and specufying the relevant (sub-) label duration and PLDs. Variable label durations are supported in BASIL if needed.

QUASAR
--------------------------------------
This is a special version of pASL which combines data with and without vascular signal suppression. QUASAR can be used to separate signal from tissue and macrovasular contamination. It is possible using QUASAR to isolate the macrovascular signal and thus estimate an arterial input function, which enables 'model-free' deconvolution. QUASAR uses a Look-Locker readout to achieve sampling of different TIs.

Analysis using both 'model-based' and 'model-free' methods are provided in the QUASIL tool, a version of BASIL optimised for QUASAR data. 

Turbo-QUASAR
--------------------------------------
This is a form of pASL where multiple sub-boluses are created using a series of labelling pulses. It is a variant on QUASAR ASL. The total effective bolus duration is the summation of the duration each sub-bolus, which is equal to the time between each inversion time (TI) of the Look-Locker readout under normal circumstances where the flow velocity of the arterial blood is about 25cm/s. In conditions where the flow velocity is significantly different from this value, an estimation of the flow velocity is needed from a separate phase contrast MR data. Subsequently, the effective bolus duration can be estimated from the flow velocity information.

To analyse Turbo-QUASAR in BASIL, you can the TOAST command line tool.

Other ASL quantification/analysis issues
==========================================

There are a number of other analysis steps and processes that are specific to ASL, or specifically availabel for ASL through BASIL. Some important ones are noted here.

Spatial regularization
----------------------

BASIL can apply a spatial regularisation to the estimated perfusion image and this is highly *recommended*. This exploits the fact that neighboring voxels are likely to have similar perfusion values, i.e. perfusion variation in the brain is relatively smooth. It brings the advantages associated with the more common pre-processing step of spatially smoothing the data. However, unlike smoothing the data it correctly preserves the non-linear kinetics exploited by the perfusion estimation. It is also adaptive, so that in regions where the data does not support the use of smoothing the perfusion image will not be smoothed.

Registration
------------

Registration of ASL data to the structural image is difficult since the images are low resolution and with limited contrast. By default in oxford_asl
registration is carried out in multiple steps using the perfusion image directly after the BASIL analysis, an intial registration having already been done using the raw (undifferenced) ASL data. BASIL now exploits the BBR cost function for registration and this has been found to be more robust and accurate, when using the perfusion image itself, than previous methods that relied on the raw data.

You should *ALWAYS* inspect the results of registration to determine whether it has been effective. It is possible use alternative registration strategies with ``oxford_asl`` (e.g., using the ``--regfrom`` option) or even do the registration separately on the ``native_space`` results from ``oxford_asl``, the ``asl_reg`` tool exists as a separate function if you wish to explore the ASL registration process apart from the main ``oxford_asl`` pipeline.

Arterial (macrovascular) contribution
--------------------------------------

If flow suppresion has not been applied to your data and you have short PLDs (<1 second), then there may be significant signal from labeled arterial blood in the region of major vessels in the ASL data. In single PLD ASL data you will need to examine the perfusion images for signs of arterial contaimination (see the 'White Paper' for an example of this). This can also be an issue in patients with vascular diseases, where slow flow and thus long arterial transit times are expected.

For multi delay data the arterial signal can be accounted for by modelling this arterial component (by ``default oxford_asl`` will includes this component). When the arterial component is included in the analysis then a further parameter, the arterial blood volume, is available in the output images.

Partial volume correction
-------------------------

The low resolution of ASL data typically means that there is substantial partial voluming of grey (GM) and white matter (WM), plus CSF too. Since GM and WM have very different kinetics (WM tends to have lower perfusion and longer arterial transit time) a normal analysis will provide a perfusion that is something of a combination of the two tissue types. BASIL can attempt to automatically correct for the different tissue types. BASIL via ``oxford_asl`` can do this automatically as long as you supply a structural image that has been already been processed using ``fsl_anat`` (or if you supply suitable partial volume estimate images).

Partial volume correction is available though the basil command line tool. For this implementation you need to provide partial volume estimates (PVE) at the same resolution as the ASL data. PVE can be obtained from a structural image, for example using ``FAST``, the high resolution PVE images can then be converted using a transformation matrix from the structural to ASL image space. This step is best done using ``applywarp`` to ensure that the values are the total PVE within the voxel, something like::

    applywarp --ref={asl_data} --in={PV_estimate_image} --out={PV_estimate_low_res} 
              --premat={structural_to_ASL_tranformation_matrix} --super --interp=spline 
              --superlevel=4

T1 values
---------

T1 values are important to the kinetic model inversion and should be chosen based on the field strength that data was acquired at, consideration might also need to be taken of the subject in which analysis is being carried out. BASIL by deafult takes values for 3T and assumes for the tissue only a grey matter value, unless partial volume correction is applied when separate grey and white matter values are specified. By deafult a separate value for the T1 of bloos is used unless operating in 'white paper' mode, where the blood T1 value is also used for the tissue.

Commonly it is assumed that T1 values are fixed across the brain in the quantification. However, these value are not absolutely certain and may well vary across the brain and between individuals. BASIL can take this into account by inferring on T1 values, you should still, however, set sensible expected values. NOTE: maps of T1 produced by this process are unlikely to be accurate measures of T1 in the brain - ASL data is not suitable for this. The purpose of including T1 the inference is primarily to take account of their varaibility when estimating the other parameters. An exception to this is QUASAR data (in quasil) where a tissue T1 image is estimated from the saturation recovery of the control data (and subsequently applied to the kinetic curve fitting).

Further Reading
===============

To learn more about ASL, acquisition choices, the
principles of analysis and how perfusion images can be used in group
studies you might like to read:

*Introduction to Perfusion Quantification using Arterial Spin
Labelling*, Oxford Neuroimaging Primers, Chappell, MacIntosh & Okell,
Oxford University Press, 2017.

Online examples are availble to go with this primer using the BASIL
tools. These can be found on the Oxford Neuroimaging Primers
website: http://www.neuroimagingprimers.org

The following book reamins a good introduction to functional imaging
including perfusion using ASL:

*Introduction to Functional Magnetic Resonance Imaging: principles and
Techniques*. Buxton, Cambridge University Press, 2009.
