==========================
Calibration (asl_calib)
==========================

.. toctree::
   :maxdepth: 2

   aslcalib_userguide

ASL tag-control difference data can be used to quantify perfusion. However, the values obtained are not by default provided in conventional units. To get absolute CBF quantification it is also necessary to estimate the equilibrium magnetization (M0) of arterial blood.

A popular option is to correct for the equilibrium magnetization of arterial blood using a proton density (PD) weighted image (using a relatively long TR) and dividing the ASL perfusion image (the output of ``basil``) by the PD image voxel-by-voxel. Alternatively, the M0 value for arterial blood can be estimated indirectly from a measurement in a reference 'tissue', such as the CSF or white matter, either:

 - LongTR: From a separate calibration image that uses the same acquisition as the ASL data, but contains no inversion (i.e. a 'control' image) and no background suppression. Ideally the images would be acquired with a very long TR.   However, it is possible to account for shorter TR values, for example matching that the of ASL sequence, with an estimate of the T1 of the reference 'tissue'.

 - SatRecov: From the saturation recovery of the control images in the ASL data sequence, if a presaturation has been applied in the imaging region.
   
``asl_calib`` performs the necessary steps to obtain the M0 of arterial blood value from such a calibration images. It can also:

 - LongTR method: produce a spatial sensitivity estiamte for the coil used for aquisition, if another calibration image is supplied that was acquired using some other coil (assumed to have a flat spatial sensitivity) as a reference (e.g. the body coil).
   
 - SatRecov method: produce an estimated T1 of tissue image for use in kinetic curve model fitting.

   
 
