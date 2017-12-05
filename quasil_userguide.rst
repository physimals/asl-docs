=====================
QUASIL User Guide
=====================

Usage
-----

Since the acquisition of data using QUASAR is very well defined there are far fewer options to set with QUASIL than a typical BASIL analysis. NOTE that QUASIL expects the data without tag-control subtraction having been performed. A typical command line usage would be::

    quasil -i [asl_data] -o [output_directory]
 
This would carry out a model-based analysis of the ASL data and provide voxelwise estimates of CBF, arrival time and arterial blood volume (aBV). The calibration of the data to the equilibrium magnetization is also carried out as part of the processing so that the perfusion image is provided in absolute units (ml/100ml/min). Additionally, the perfusion image prior to calibration is also provided: perfusion_raw.

Typing quasil with no options will give basic usage information.

Extended options
----------------

 - ``-i <asl_data>`` The QUASAR ASL data in Nifti file format. The data order should 'as acquired', i.e. as blocks of TIs measured in the different phases of flow suppression.
 - ``-o (optional) [output_directory]`` use this to place the result in a different directory to the current working directory.
 - ``-m (optional) [brain_mask]`` Use this to provide a brain mask in which data analysis should take place. If this is not set a mask will be generated automatically from the data.
 - ``--mfree`` Do a 'model-free' rather than model based analysis of the data.

Calibration
-----------

The calibration is carried out by ``asl_calib`` and uses the saturation recovery of the control images. M0 of the tissue is estimated voxelwise from fitting a saturation recovery model and from this a voxelwise estimate of M0 of the blood is derived and applied to the estimated perfusion images. More details are given in the references above. An alternative is to calculate the M0 of CSF within a CSF mask and from this estimate a single value of M0 of arterial blood, as is done by ``oxford_asl`` by default. This can be achieved using ``asl_calib`` and the resulting M0 value applied to the ``perfusion_raw`` image.
