======================
Background Information
======================

For a good introduction to ASL and using it to quantify perfusion you might like to consult the following references:

*Buxton, R. B. (2002 or 2009). Introduction to Functional Magnetic Resonance Imaging: principles and Techniques. Cambridge University Press.*

*Tofts, P. (2003). Quantitative MRI of the brain: measuring changes caused by disease. (P. Tofts, Ed.). Wiley. http://qmri.org/*

*Golay, X., Hendrikse, J., & Lim, T. (2004). Perfusion Imaging Using Arterial Spin Labeling. Topics in Magnetic Resonance Imaging, 15(1), 10–27.*

*Buxton, R. (2005). Quantifying CBF with arterial spin labeling. Journal of magnetic resonance imaging : JMRI, 22(6), 723–726. doi:10.1002/jmri.20462*

Future Work
===========

Some improvements and new features are planned for BASIL, in some cases these already exist in a beta form and may be made available on request for research purposes.

 - Graphical user interface providing similar functionality to oxford_asl. DONE see asl_gui (from FSL 5.0.3 onward) - still in BETA!
 - Partial volume correction pipleline in ``oxford_asl``. DONE (FSL 5.0.6)
 - Partial volume correction for QUASAR data in ``quasil``.
 - Analysis of multi-TI ASL data in epochs. This would permit variations in perfusion during a multi-TI ASL experiment to be quantified by dividing the data into a series of shorter (overlapping) epochs. This can be used for functional studies in which there is no a priori design. DONE (FSL 5.0.6)
 - Extension of the kinetic model to include the effects of labelled bolus dispersion, restricted exchange of label from capillaries into tissue and the presence of pre-capilliary blood signal.