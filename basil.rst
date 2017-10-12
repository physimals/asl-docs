==================
Basil Introduction
==================

Bayesian Inference for Arterial Spin Labelling MRI
==================================================

.. image:: images/basil_perfusion.jpg
   :scale: 100 %
   :alt: BASIL perfusion image
   :align: right

Arterial Spin Labeling (ASL) MRI is a non-invasive method for the quantification 
of perfusion. Analysis of ASL data typically requires the inversion of a kinetic 
model of label inflow along with a separate calculation of the equilibrium 
magnetization of arterial blood. The BASIL toolbox provides a means to do this 
based on Bayeisan inference principles. The method was orginally developed for 
multi delay (inversion time) data where it can be used to greatest effect, but 
is also sufficiently fleixble to deal with the widely used single delay form 
of acquisition.

If you have resting ASL data with only a single inversion time then you can 
still use the tools in BASIL for perfusion quantification. If you want to 
perform analysis of a functional experiment with ASL data, i.e. one where 
you want to use a GLM, then you should consult the perfusion section of 
`FEAT <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FEAT/UserGuide>`_, 
or if you have dual-echo (combined BOLD and ASL) data then consult 
`FABBER <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FABBER>`_.

For single delay ASL data kinetic model inversion is realtively trivial and 
solutions to the standard model have been described int he literature. However,
it is becoming increasingly common to aquire ASL data at multiple times 
post-inversion and fit the resultant data to a kinetic curve model. This 
permits problems in perfusion estimation associated with variable bolus arrival 
time to be avoided, since this becomes a paramter of the model whose value is 
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

Pre-release
===========

A pre-release of the latest version of the BASIL tools, inlcuding the new GUI as 
demonstrated at ISMRM, can be found by following the link below. Use with caution, 
as this is still under development!

https://github.com/ibme-qubic/oxford_asl/releases

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

 - Asl (Asl_gui) - The graphical user interface that brings the BASIL tools together 
   in one place. [BETA from FSL 5.0.3 onward]

 - Oxford_asl - A command line interface for most common ASL perfusion analysis.

(Note: there are a couple of changes in oxford_asl in the FSL 5.0.6 release that might 
affect perfusion quantification compared to previous versions - see the user guide for more 
information)

The BASIL toolset
-----------------

 - BASIL (itself) - this is the core tool that performs kinetic-model inversion to the 
   data using a Bayesian algorithm. You should only need to use it directly for more 
   custom analyses than that offered by oxford_asl/Asl_gui.
 - QUASIL - A special version of BASIL optimised for QUASAR ASL data, includes model-based 
   or model-free analyses along with calibration.
 - asl_calib - this tool takes a supplied calibration volume and calculates the 
   magnetization of arterial blood allowing CBF to be quantified in absolute units. The 
   main functionality of asl_calib is built into oxford_asl, Asl_gui and QUASIL, but 
   more options are available when using it directly.
 - asl_reg - this tool is designed to assist in registration of (low resolution) ASL 
   images to structural or standard brain images. The functionality of asl_reg is built 
   into oxford_asl and Asl_gui.
 - asl_file - a command line tol for the manipulation of ASL data files that respects the 
   normal structure of ASL data.

References
==========

If you employ BASIL in your research please reference the article below, plus any others 
that specifically relate to the analysis you have performed:


 - *Chappell MA, Groves AR, Whitcher B, Woolrich MW. Variational Bayesian inference for a non-linear forward model. IEEE Transactions on Signal Processing 57(1):223-236, 2009.*

If you employ spatial priors you should ideally reference this article too.

 - *A.R. Groves, M.A. Chappell, M.W. Woolrich, Combined Spatial and Non-Spatial Prior for Inference on MRI Time-Series , NeuroImage 45(3) 795-809, 2009.*

If you fit the macrovascular (arterial) contribution you should reference this article too.

 - *Chappell MA, MacIntosh BJ, Donahue MJ, Gunther M, Jezzard P, Woolrich MW. Separation of Intravascular Signal in Multi-Inversion Time Arterial Spin Labelling MRI. Magn Reson Med 63(5):1357-1365, 2010.*

If you employ the partial volume correction method then you should reference this article too.

 - *Chappell MA, MacIntosh BJ, Donahue MJ,Jezzard P, Woolrich MW. Partial volume correction of multiple inversion time arterial spin labeling MRI data, Magn Reson Med, 65(4):1173-1183, 2011.*

If you perform model-based analysis of QUASAR ASL data then you should reference this article too.

 - *Chappell, M. A., Woolrich, M. W., Petersen, E. T., Golay, X., & Payne, S. J. (2012). Comparing model-based and model-free analysis methods for QUASAR arterial spin labeling perfusion quantification. doi:10.1002/mrm.243*

  