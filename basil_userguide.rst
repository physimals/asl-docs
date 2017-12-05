================
Oxford ASL User Guide
================


Asl_gui
=======

The graphical user interface to the BASIL tools can be accessed by typing either Asl (linux) or Asl_gui (OS X) at the command line. It should provide most of the options required for analysis of ASL data inlcuding the majority of the more advanced features of BASIL.

Note: Asl_gui was only officially released with FSL 5.0.3 (any previous versions are unlikely to be very stable and will not adhere to the documentation here). This is still a beta version, we expect to add further features and refine the interface for a future release.

Note: Changes in oxford_asl in FSL 5.0.6 also apply to asl_gui - namely that inversion efficiency is now included in the calculation (using default values) and that structural images shoud have been brain extracted before input to asl_gui.

Asl_gui has four tabs, whose function are fairly obvious:

- Data: Specify details of the ASL data here, as well as any supplementary data such as a structural image.
- Analysis: Options relating to the analysis, primarily the kinetic model and the estimation process.
- Registration: Options relating to the registration of the results to the structural image.
- Calibration: Options relating to the estimation of M0a (the equilibrium magnetization of arterial blood) for absolute quantification of pefusion.

More details on each tab are provided below. Note that some of the options available on each tab depend on what information is present in your data (set on the data tab). Thus your view of the tab might differ from the one shown here slightly.

Data
----

.. image:: images/aslgui_data.jpg

- Input Filename: Select here the ASL data file - it should be a single 4D nifti file, with the individual measurements in the 4th dimension
- Inversion Times: The inversion times present in the data as a comma separated list. If the data contains multiple repeats of the same indiviual/set of inversion times then it is only necessary to list this once.
- Bolus duration: For cASL/pcASL this is the labeling duration, for pASL this is the assumed value for the bolus duration that may have been set by a QUIPSSII method or otherwise a reasonable estimate of its value (usually int he range 1-1.5s). If the bolus duration has not be fixed by the acquisition then estimating its value from the data should be selected on the analysis tab.
- Labeling: Choose the labelling scheme employed.
- Data is tag-control pairs: Instructs BASIL to do tag control subtraction on the data, turn off if this has already been done.
- Data order (grouped by): This is only applicable to multi delay ASL data and specifies how the different inversion times appear in the data - see the oxford_asl help section.
- Static tissue: Specify whether the static tissue has been manipulated in any way (not relevant to data that is not tag-control pairs). This determines what options are available for calibration.
- Structural image: provide a structural image to which to register the resulting images.

Analysis
--------

.. image:: images/aslgui_analysis.jpg

- Output directory: where to put the results.
- Optional brain mask: BASIL will try to create a brain mask for you using the available data. This permits you to specify your own mask.
- Output parameter variance: Instructs BASIL also to output the variance images for perfusion (and other paramters) allowing you to assess the uncertainty of estimation and pass these up into a higher-level analysis.
- Bolus arrival time: The assumed value for the BAT. For multi dealy data BAT is estimated from the data and this value is used as prior information, for single delay data this value can be treated as fixed. The default 0.7 appears to be reasonable for pASL, but logner values ~1.3s have been found to be more suitable for pcASL data.
- T1/T1b: T1 values for tissue and blood.
- Use adaptive spatial smoothing on CBF: applys a spatial prior to the perfusion image during estimation, thus making use of neighbourhood information. This is a highly recommended option, but is off by default.
- Incorporate T1 uncertainty: Permits voxelwise variability in the T1 values, this will primiarly be reflected in the variance images.
- Include macro vascular componet: Corrects for MV contamination and it suitable where the data contains multiple delays (including the case with flow suppression)
- Fix bolus duration: Takes the value from the data tab as fixed, turn off to estimate this from the data, where the value on the data tab will be used as prior information.

Registration
------------

.. image:: images/aslgui_reg.jpg

- Structural to standard space transform: a .mat from flirt that specifies the transformation from structural to 'standard' space.
- Alternate standard brain iamge: The 'standard' brain for the above transformation if MNI152 has not been used.
- Low-resolution structual image: Another structural image of lower resolution (similar to the ASL data) to be used as an intermediary for registration.

Calibration
-----------

.. image:: images/aslgui_calib.jpg

- Perform calibration: by default M0a estimation is not done.
- Mode: either 'LongTR' or 'Saturation Recovery' - the options present here will depend upon the choice of 'static tissue' on the data tab.
- M0 calibration image (only for background suppressed data): a separate 'calibration' image to be used for M0a calculation.
- Use coil sensitivity reference image: A separate image with the same acquisition parameters as the main calibration (either image above or the control images in the ASL data) but with a different coil with flatter sensitivity that used for the main data.
- Calibration gain: Only relevant if the gain was higher for the ASL data than the calibration image, in which case this is how much higher the gain was for the ASL data (normally this might only apply for backgroudn suppressed data).
- Reference tissue: Here details of the reference tissue to used for M0a calculation are specified. Voxelwise calculation of M0a cannot be carried out using Asl_gui, use the asl_calib tool directly.
- Reference tissue type: CSF/white matter/grey matter/none. For the first three options a mask will be generated automatically from the structural image (if you have specfied one). Otherwise you have to add your own mask in the Reference Tissue Mask box. Generally CSF or white matter are good choices, avoid grey matter.
- Reference T1: T1 of the reference tissue - currently this defaults to the CSF value, so will need to be changed if you change the tissue type (see asl_calib).
- Reference T2/ Blood T2: T2 values, these are only relevant if you specify the TE of your sequence. T2 of the reference deafults to a CSF value. These should be replaced by T2* values if appropriate.
- Sequence parameters
  - TR: This is for the longTR mode and should be the Tr of the ASL sequence, unless you have a separate calibration image in which case use that TR.
  - TE: This corrects for T2 differences between the reference tissue and the tissue (using a blood T2 value) using the TE of the data (which is assumed to be the same as any calibration image).

Output
------

The outputs from Asl_gui are a resting perfusion image called perfusion.nii.gz, which provides blood flow in relative (scanner) units, and an arrival time image called arrival.nii.gz. If a calibration has been performed then a further image perfusion_calib.nii.gz is also produced, which is a flow map in absolute units (ml/100g/min). Results in standard space (assuming that the transformation matrix has been supplied) will appear in the output directory directly. Results in the native space of the data and structural space (along with any transformation matrices from the registration process) will appear in their own subdirectories.

If calibration was performed then a separate subdirectory will be created and will contain text file called M0b.txt that records the estimated M0 value from arterial blood. If a reference tissue mask was not supplied then the automatically generated one will also be saved in as refmask.nii.gz






