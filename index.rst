BASIL toolset
=============

BASIL is a collection of tools that aid in the creation of quantitative 
CBF images from ASL data. It is available within `FSL <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki>`_ 
(v6.0.1 or later is strongly recommended). 

BASIL includes complete high-level pipelines for
processing ASL data and also individual tools for more bespoke analysis. 

.. toctree::
   :maxdepth: 2

   analysis_guide
   overview
   tutorials
   gui_userguide
   oxford_asl_userguide
   tools
   
References
==========

If you employ BASIL in your research please reference the article below, plus any others 
that specifically relate to the analysis you have performed:

 - *Michael A. Chappell, Thomas F. Kirk, Martin S. Craig, Flora A. Kennedy McConnell, Moss Y. Zhao, Bradley J. MacIntosh, Thomas W. Okell, Mark W. Woolrich; BASIL: A toolbox for perfusion quantification using arterial spin labelling. Imaging Neuroscience 2023; 1 1–16. doi: https://doi.org/10.1162/imag_a_00041*

For detail of the Variational Bayes method employed in Basil:

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

  
