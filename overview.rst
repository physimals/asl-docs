Overview of the BASIL toolset
=============================

Higher-level packages
---------------------

These provide a single means to quantify CBF from ASL data, 
including kinetic-model inversion, absolute quantification via a calibration image and 
registration of the data. This will generally be the first place to go for most people 
who want to do processing of ASL data.

 - ``asl_gui`` - The graphical user interface that brings the BASIL tools together 
   in one place.

 - ``oxford_asl`` - A command line interface for most common ASL perfusion analysis.

Individual analysis tools
-------------------------

These are designed to perform a specific task in the analysis of ASL data. In many cases
the higher-level tools will call them when required, however they can also be used individually
in cases where the high-level processing pipeline is not suitable.

 - ``basil`` (command) - this is the core tool that performs kinetic-model inversion to the 
   data using a Bayesian algorithm. You should only need to use it directly for more 
   custom analyses than that offered by oxford_asl/Asl_gui.
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
 - ``quasil`` - A special version of BASIL optimised for QUASAR ASL data, includes model-based 
   or model-free analyses along with calibration.
 - ``toast`` - A special version of BASIL optimised for Turbo-QUASAR ASL data, includes 
   model-based analyses, calibration, and correction for MT effects.
