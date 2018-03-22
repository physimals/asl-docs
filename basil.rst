==================
Basil 
==================

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

Download
========================

The documentation found here relates to the version of BASIL that is
scheduled for FSL 6.0. A release of the latest version of the BASIL
tools can be found by following the link below. This can be installed
alonside an existing FSL 5.0.x release, we recommend you use this
version instead of the version of BASIL in FSL 5.0.x now.

https://github.com/ibme-qubic/oxford_asl/releases

User Guide
=================

.. toctree::
   :maxdepth: 2

   basil_userguide

Examples
===============

An extensive set of examples of the use of  BASIL (for pcASL)
is availabe as part of the primer:

*Introduction to Perfusion Quantification using Arterial Spin
Labelling*, Oxford Neuroimaging Primers, Chappell, MacIntosh & Okell,
Oxford University Press, 2017.

The examples themselves are freely available online at the primer
website: neuorimagingprimers.org, you can access the ASL examples
directly here_.

.. _here: http://www.neuroimagingprimers.org/examples/introduction-to-perfusion-quantification-using-asl/
   

BASIL tools
===========

BASIL is supplemented by a collection of tools that aid in the creation of quantitative 
CBF images from ASL data, you should either use one of the higher-level analysis packages 
or if you want a more specific analysis select the appropriate tool(s) for the data you 
have.

Higher-level packages
---------------------

These provide a single means to quantify CBF from ASL data, 
including kinetic-model inversion, absolute quantification via a calibration image and 
registration of the data. This will generally be the first place to go for most people 
who want to do processing of ASL data.

 - ``asl_gui`` - The graphical user interface that brings the BASIL tools together 
   in one place.

 - ``oxford_asl`` - A command line interface for most common ASL perfusion analysis.


The BASIL toolset
-----------------

 - ``BASIL`` (itself) - this is the core tool that performs kinetic-model inversion to the 
   data using a Bayesian algorithm. You should only need to use it directly for more 
   custom analyses than that offered by oxford_asl/Asl_gui.
 - ``QUASIL`` - A special version of BASIL optimised for QUASAR ASL data, includes model-based 
   or model-free analyses along with calibration.
 - ``asl_calib`` - this tool takes a supplied calibration volume and calculates the 
   magnetization of arterial blood allowing CBF to be quantified in absolute units. The 
   main functionality of asl_calib is built into oxford_asl, Asl_gui and QUASIL, but 
   more options are available when using it directly.
 - ``asl_reg`` - this tool is designed to assist in registration of (low resolution) ASL 
   images to structural or standard brain images. The functionality of asl_reg is built 
   into oxford_asl and Asl_gui.
 - ``asl_file`` - a command line tool for the manipulation of ASL data
   files, particulary designed to cope with the complex strcuture of
   interleaved lable and control images combined with muliple
   post-labeling delays.

Further Reading
============

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

References
==========

If you employ BASIL in your research please reference the article below, plus any others 
that specifically relate to the analysis you have performed:


 - *Chappell MA, Groves AR, Whitcher B, Woolrich MW. Variational Bayesian inference for a non-linear forward model. IEEE Transactions on Signal Processing 57(1):223-236, 2009.*

If you employ spatial regularisation (priors) you should ideally reference this article too:

 - *A.R. Groves, M.A. Chappell, M.W. Woolrich, Combined Spatial and Non-Spatial Prior for Inference on MRI Time-Series , NeuroImage 45(3) 795-809, 2009.*

If you fit the macrovascular (arterial) contribution you should reference this article too.

 - *Chappell MA, MacIntosh BJ, Donahue MJ, Gunther M, Jezzard P, Woolrich MW. Separation of Intravascular Signal in Multi-Inversion Time Arterial Spin Labelling MRI. Magn Reson Med 63(5):1357-1365, 2010.*

If you employ the partial volume correction method then you should reference this article too.

 - *Chappell MA, MacIntosh BJ, Donahue MJ,Jezzard P, Woolrich MW. Partial volume correction of multiple inversion time arterial spin labeling MRI data, Magn Reson Med, 65(4):1173-1183, 2011.*

If you perform model-based analysis of QUASAR ASL data then you should
reference this article too.

 - *Chappell, M. A., Woolrich, M. W., Petersen, E. T., Golay, X., & Payne, S. J. (2012). Comparing model-based and model-free analysis methods for QUASAR arterial spin labeling perfusion quantification. doi:10.1002/mrm.243*

  
