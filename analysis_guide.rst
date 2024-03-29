=============================
ASL Analysis Guide
=============================

.. image:: images/basil_perfusion.jpg
   :scale: 100 %
   :alt: BASIL perfusion image
   :align: right

Perfusion Quantification using Arterial Spin Labelling MRI
==========================================================

Arterial Spin Labeling (ASL) MRI is a non-invasive method for the quantification 
of perfusion. This guide introduces the essential concepts you need to understand when acquiring and
analysing ASL data, as well as more advanced analysis techniques you
might exploit when aiming for higher accuracy and senstivity when
using ASL in a study.

This guide complements the information contained in the `Introduction
to Perfusion quantification using Arterial Spin Labelling (OUP, 2017) <https://global.oup.com/academic/product/introduction-to-perfusion-quantification-using-arterial-spin-labelling-9780198793816?q=%22Oxford%20Neuroimaging%20Primers%22&lang=en&cc=gb>`_. You can perform the analyses shown in the
guide using the BASIL toolbox by following the instructions in the `Tutorials section <https://asl-docs.readthedocs.io/en/latest/tutorials.html>`_ of this website. Alternatively, similar
practical activities are also available on `neuroimagingprimers.org <http://www.neuroimagingprimers.org>`_.

The guide includes five pre-recorded video lectures that are used
in the BASIL course (an FSL mini-course).

Preparatory materials
---------------------

If you are new to Neuroimaging or to FSL tools you might find the
following resources helpful before looking at the material on ASL.

If you are not particularly familar with MRI you might like to
read a `Short Introduction to MRI Physics for Neuroimaging 
<http://www.neuroimagingprimers.org/online-appendices/>`_ 
available via the neuroimagingprimers.org website.

The `FSL course <http://fsl.fmrib.ox.ac.uk/fslcourse/online_materials.html>`_
provides a wide range of videos and practical
exercises. Whilst you do not need to have looked at any of this before
reading this guide, you might find some of it helpful background for
topics that will be covered (especially for the group analysis
section).

We would recommend familarity with:

 - Section 1: Image Registration and Distorition Correction (videos 1-5
   are all helpful)
 - Section 2: Segmentation and Structural Analysis (video 7 on FAST)
 - Section 4: Statistics & Task fMRI: Inference and Group Analysis (videos
   15-20 provide useful background on group analysis)

Introductory video
------------------

In this video we examine what perfusion is
and why we might be interested in measuring it in the brain. We
briefly consider alternative established perfusion imaging techniques
to understand when and where we might use ASL. Finally, we introduce
the BASIL toolbox, avaiable as part of FSL.

.. raw:: html

    <div style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
      <iframe src="https://youtube.com/embed/grSeSiZZ8hE" frameborder="0" width="560" height="315"   allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>

ASL acquisition
---------------

There are various parameters associated with an ASL acquisition. Some of which are 
important for the quantification/analysis process. Whilst you do not necessarily need 
to know all of the details of an ASL acquisition to be able to quantify perfusion 
image, in this section we provide an overview of the key
parmeters when designing an ASL protocol and that you need to know for
sucessful analysis.

.. raw:: html

    <div  style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
      <iframe width="560" height="315" src="https://youtube.com/embed/PpUq7eX8KZA" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>

pcASL or pASL
~~~~~~~~~~~~~

The labelling may either have been pseudo-continuous ASL (pcASL, most common) or 
pulsed ASL (pASL). There are important differences between these two forms of ASL 
that affect the quantification, since they determine how the
blood-water is labelled.

Post-label delay(s)
~~~~~~~~~~~~~~~~~~~

After labeling, a delay is left for the labeled blood-water to travel into the brain. 
For pcASL this is called the Post-Label Delay (PLD) and is the time from the *end* of 
the label duration (see `Label duration`_) until imaging. For pASL the
labeling process is instantaneous and it is more common to refer to
the inversion time (TI). Note that we can define a common delay measure: the inflow time (also TI), 
the time from the *start* of labeling. This is identical to the inversion time for pASL, 
but for pcASL is the sum of the label duration and PLD:

pcASL:  TI = PLD + Label duration

It is quite common to meet ASL data with multiple repeats/measurements (and thus volumes 
in the resulting images) that all have the same PLD (or TI) - single delay ASL. It is, 
however, possible to use a range of different PLD in an acquisition in an attempt to 
extract more information, or achieve a better SNR - multi-delay (multi-PLD) ASL. 

Label duration
~~~~~~~~~~~~~~

The label (or bolus) duration is an important measure of how much labeled-blood water 
has been delivered to the tissue and is thus important for quantification. For pcASL 
the value is set by the sequence and thus is something you need to define/know. It is quite 
common to use a 1.8 second (or longer) label duration with pcASL.

In principle in pASL the label duration is unknown (a spatial region is labeled instead 
of a known duration of flowing blood). You may find that your pASL acquisition is using 
Q2TIPS or QUIPSSII, in which case the label duration has been set using extra pulses. 
Quite often the value of label duration can then be determined from the associated 
parameter, often called TI2 - a value of 0.7 or 0.8 seconds would be quite normal. 
Where the label duration is genuinely unknown (e.g. a FAIR pASL
acquisition), it is possible to estimate it as long as the data is
multi-TI. It is possible even with 
Q2TIPS/QUIPSSII that the duration will be shorter than expected due to
high flow in the 
labelling region.

Readout
~~~~~~~

A variety of readouts can be combined with ASL labelling to acquire
ASL data. The important distinction is between (multi-slice) 2D and 3D
readouts, since in the former the later time of acquisition of mroe
superior slices needs to be acocunted for in the quantification.

Background Suppression
~~~~~~~~~~~~~~~~~~~~~~

It is common for background suppression to be applied in an ASL
acquistion to suppress signal not associated with labeled-blood water
(static tissue signal) and reduce artefacts arising from motion.

Analysis of ASL data
--------------------

The very simplest analysis of ASL data requires the subtraction of
label and control images in the data to produce a perfusion weighted
image. With the addition of kinetic model inversion and calibration
(requring calibration data acquired as part of the ASL dataset) it is
possible to produce quantitative perfusion images with conventional usings of ml/100g/min.

.. raw:: html

    <div  style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
      <iframe width="560" height="315" src="https://youtube.com/embed/baK7XRmmSOk" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>

Subtraction
~~~~~~~~~~~

Central to ASL analysis is the subtraction of label and control images. Both label and 
control images will contain some signal from brain tissue - called the static tissue 
signal (this is true even if background suppression has been used to reduce this 
contribution). Subtraction of the label-control pair reveals the contribution from 
labelled blood-water. This image is often referred to as the difference image and is 
perfusion-weighted, which means it reflects the perfusion in each voxel, but the 
intensity value in each voxel does not alone provide an absolute measure of perfusion.

To go beyond the perfusion weighted image, and generate 
quantitative voxelwise measures of perfusion with values in the typical units of 
ml/100 g/min, we need to use the kinetics of ASL.

Kinetic Model Inversion (Kinetic Modelling)
~~~~~~~~~~~~~~~~~

The voxel intensity in an ASL difference image is directly related to the labelled 
blood-water. More accurately, it relates to the amount of labelled blood-water that 
has accumulated in the voxel in the time between creation of the label and the 
collection of a brain image. This means that it is a measure of delivery and thus 
perfusion (rather than blood volume or blood flow rate). To be able to say how much 
labelled blood has been delivered, and thus what the perfusion is, it is necessary 
to describe the delivery process, as well as what happens to the labelled blood once 
it has been delivered. This is achieved by means of a kinetic model.

At its very simplest the kinetic model for labelled blood-water in an ASL study 
needs to account for the delivery of a finite duration (the label duration) of 
labelled blood-water into the voxel where it accumulates. At the same time as it 
is being delivered, the label is also decaying away. THe tracer decays at a rate 
defined by the T1 time constant, which is of the order of a second in the brain at 
typical MRI field strengths. The kinetic model allows the relationship between the 
signal and perfusion to be expressed as an equation and this can be rearranged to 
give an equation that takes signal magnitude and returns perfusion, or fit to the 
data using optimisation techniques.

Calibration
~~~~~~~~~~~

The ASL calculation relies on knowledge of the tracer concentration, strictly the 
quantity called the equilibrium magnetization of arterial blood, which will vary 
between individuals and other MRI-related factors (e.g. the main magnetic field 
strength). The simplest approach for estimating this parameter is by the acquisition 
of a separate proton-density-weighted image. This can be converted to a measure of 
arterial magnetization by accounting for the relative density of hydrogen nuclei 
in tissue and blood (the partition coefficient). Various corrections can be performed 
where the calibration image is not a pure proton-density weighted image, e.g., where 
it has a (realtively) short repetition time.

Further Quantification of ASL data
----------------------------------

For single delay ASL data kinetic model inversion is relatively trivial and 
solutions to the standard model have been described in the literature. However,
there are various advantages to aquiring ASL data at multiple times 
post-inversion and fitting the resultant data to a kinetic model. This 
permits problems in perfusion estimation associated with variable
arterial transit time (ATT) to be avoided, since this becomes a parameter of the model whose value is 
determined from the data. ATT can also be a valaube parameter
(describing the passage of blood throught the vasculature) in its own right.

.. raw:: html

    <div  style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
      <iframe width="560" height="315" src="https://youtube.com/embed/yC46T4kvJKI" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>

The model fitting can be performed by a variety of (non-linear)
regression techniques, inlcude two step processes that or
least squares algorithms. BASIL uses a (fast) Bayesian inference method 
for the model inversion, this provides a number of advantages:

 - Voxel-wise estimation of perfusion and ATT along with parameter 
   variance (allowing confidence intervals to be calculated).

 - Incorporation of natural varaibility of other model parameters, e.g. values of T1,
   T1b and labeling/bolus duration.

 - Spatial regularization of the estimated perfusion image.

 - Correction for partial volume effects (where the appropriate segmentation 
   information is available).

Spatial regularization
~~~~~~~~~~~~~~~~~~~~~~

BASIL can apply a spatial regularisation to the estimated perfusion image and this is 
highly *recommended*. This exploits the fact that neighboring voxels are likely to have 
similar perfusion values, i.e. perfusion variation in the brain is relatively smooth. It 
brings the advantages associated with the more common pre-processing step of spatially 
smoothing the data. However, unlike smoothing the data it correctly preserves the 
non-linear kinetics exploited by the perfusion estimation. It is also adaptive, so that 
in regions where the data does not support the use of smoothing the perfusion image will 
not be smoothed.

Group analysis using ASL data
-----------------------------

In a study ASL data acquired in individuals can be combined to examine
differences or changes in perfusion (or ATT). Group analyses using ASL
are similar to that used for other neuroimaging modalities, e.g. BOLD
fMRI. I this section we consider specific issues that relate to ASL
data, including acheiving good alignment between subjects
(registration), the influence of the partial volume effect on
computing mean grey matter perfusion values, and what we can do with
*quantitative* measures.

.. raw:: html

    <div  style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
      <iframe width="560" height="315" src="https://youtube.com/embed/2zVQ7vYe73k" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>

Registration
~~~~~~~~~~~~

Registration of ASL data to the structural image is difficult since the images are low 
resolution and with limited contrast. The most robust approach appears
to be to use the perfusion (or perfusion weighted image) since this
has greater tissue contrast and is a closer match to a T1-weigthed
image than raw ASL (control/label) images. You should *ALWAYS* inspect the results of registration to determine whether it has 
been effective.

By default in BASIL registration is carried 
out in multiple steps using the perfusion image directly after the
kinetic model inversion, an 
intial registration having already been done using the raw (undifferenced) ASL data. BASIL 
now exploits the BBR cost function for registration since this
exploits the boundary between grey and white matter seen in the
perfusion images. It is possible use alternative registration
strategies and BASIL always produces images in the native space of the
data, so that registration can be revisted at a later point.

Advanced Analysis
-----------------

In the previous sections we have consider what is needed to get a
quantative perfusion image out of ASL data. There are a series of
additional techniques that can be used to improve the quality and
potentially the interpretability of the results. Whilst these
techniques are 'advanced', since they go beyond the minimum steps
outlined in earlier sections, they are by no means necessarily
complicated to perform in practice (being built into BASIL).

.. raw:: html

    <div  style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
      <iframe width="560" height="315" src="https://youtube.com/embed/Pp-jRHpGrOQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>

Correction for Motion, Distortion and Subtraction Artefacts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Strategies used in other neuroimaging modalities to correction for
motion and distortion can also be used with ASL data. A particular
source of artefacts for ASL arising in the subtraction of label and
control images, giving rise to spurious non-perfuion signal components
due to motion related differences. Various (and a growing number) of
strategies exist to compendate for these.

Arterial (macrovascular) contribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There can arise signal from labeled arterial blood in the region of major 
vessels in ASL data. This is most common in data with short PLD
(<1.5 s)  or in subjects with particular prolonged ATT.

In single PLD ASL data you will need to examine the perfusion 
images for signs of arterial contaimination (see the 'White Paper' for an example of this).
This can also be an issue in patients with vascular diseases, where slow flow and thus 
long ATT are expected and thus longer PLD might be beneficial

For multi delay data the arterial signal can be accounted for by modelling this arterial 
componen, something included in BASIL by default. When the arterial 
component is included in the analysis then a further parameter, the arterial blood volume,
is available in the output images.

Partial volume correction
~~~~~~~~~~~~~~~~~~~~~~~~~

The low resolution of ASL data typically means that there is substantial partial voluming
of grey (GM) and white matter (WM), plus CSF too. Since GM and WM have very different 
kinetics (WM tends to have lower perfusion and longer arterial transit time) a normal 
analysis will provide a perfusion value that is a weighted combination of the two tissue 
types. Partial Volume Correction attempts to automatically correct for
the different tissue type using separately supplied esatimtes of the
partial volumes of the tissues. BASIL can do this automatically as long as you supply a structural image 
that has been already been processed using ``fsl_anat`` (or if you supply suitable 
partial volume estimate images).

T1 values
~~~~~~~~~

T1 values are important to the kinetic model inversion and should be chosen based on the
field strength that data was acquired at, consideration might also need to be taken of 
the subject in which analysis is being carried out. BASIL by deafult takes values for 
3T and assumes for the tissue only a grey matter value, unless partial volume correction 
is applied when separate grey and white matter values are specified. By deafult a separate
value for the T1 of blood is used unless operating in 'white paper' mode, where the blood
T1 value is also used for the tissue.

Commonly it is assumed that T1 values are fixed across the brain in the quantification. 
However, these value are not absolutely certain and may well vary across the brain and 
between individuals. BASIL can take this into account by inferring on T1 values, you 
should still, however, set sensible expected values. 

ASL variants
------------

You are most likely to be pcASL data in practice. There are variuos
other variants of ASL which bring particular advantages, a summary of
some notable variants is provided here for reference.

Hadamard/Time-encoded ASL
~~~~~~~~~~~~~~~~~~~~~~~~~

This is a form of pcASL where the labelling performed via a series of sub-labels with 
shorter duration. Individual volumes in the ASL acquisition will vary whether for given 
periods during the label duration labeling is actually taking palce or not. This is 
normally done accoridng to a specific scheme that means that after decoding it is posisble 
to recover multi-PLD data that appears as if it has been collected with a PLD equal to 
the sub-label duration. Even more advanced versions vary the sub-label durations.

To analyse this data you can first perform the 
decoding step to reveal the multi-PLD data. Thereafter this can be used in BASIL (and 
associated tools) treating the data as label-control subtracted and specifying the 
relevant (sub-) label duration and PLDs. 

QUASAR
~~~~~~

This is a special version of pASL which combines data with and without vascular signal 
suppression. QUASAR can be used to separate signal from tissue and macrovasular 
contamination. It is possible using QUASAR to isolate the macrovascular signal and thus 
estimate an arterial input function, which enables 'model-free' deconvolution. QUASAR 
uses a Look-Locker readout to achieve sampling of different TIs.

Analysis using both 'model-based' and 'model-free' methods are provided in the QUASIL 
tool, a version of BASIL optimised for QUASAR data. 

Turbo-QUASAR
~~~~~~~~~~~~

This is a form of pASL where multiple sub-boluses are created using a series of labelling 
pulses. It is a variant on QUASAR ASL. The total effective bolus duration is the 
summation of the duration each sub-bolus, which is equal to the time between each inversion
time (TI) of the Look-Locker readout under normal circumstances where the flow velocity 
of the arterial blood is about 25cm/s. In conditions where the flow velocity is 
significantly different from this value, an estimation of the flow velocity is needed 
from a separate phase contrast MR data. Subsequently, the effective bolus duration can 
be estimated from the flow velocity information.

To analyse Turbo-QUASAR in BASIL, you can the TOAST command line tool.

Further Reading
---------------

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
