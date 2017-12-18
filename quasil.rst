======================
QUASIL
======================

QUASIL is a special implementation of BASIL specifically designed to exploit the features of QUASAR ASL data. It uses the same two component (tissue plus macro vascular signal) model that is employed by BASIL, but it has been extended to use all the information provided by the various phases for flow suppression provided by the QUASAR sequence. QUASIL uses information from the full QUASAR dataset to produce CBF images in absolute units (using an implementation of ``asl_calib``). QUASIL also provides the option to perform a 'model-free' analysis using a very similar methodology as presented in the original QUASAR paper.

More information on the model used can be found in:

  *Chappell, M. A., Woolrich, M. W., Petersen, E. T., Golay, X., & Payne, S. J. (2012). Comparing model-based and model-free analysis methods for QUASAR arterial spin labeling perfusion quantification. Magnetic resonance in medicine. doi:10.1002/mrm.24372*

More information on the model-free method can be found in the original QUASAR paper:

 *Petersen, E., Lim, T., & Golay, X. (2006). Model-free arterial spin labeling quantification approach for perfusion MRI. Magnetic resonance in medicine , 55(2), 219–232. doi:10.1002/mrm.20784*
