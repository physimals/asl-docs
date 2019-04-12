==========================
asl_calib User Guide
==========================

---------------------------------------------------------
Using M0 and sensitivity images to calculate absolute CBF
---------------------------------------------------------

``asl_calib`` can be instructed to save the M0 value and the sensitivity image (if calcuated) for subsequent use to calculate absolute CBF. Given an estimated perfusion image, e.g. from ``basil``, absolute CBF in ml/100g/min can be obtained using fslmaths:

With M0 only::

  fslmaths [perfusion_image] -div cat [M0_text_file] -mul 6000 [absolute_CBF_output_image]

With M0 and sensitivity image::

  fslmaths [perfusion_image] -div cat [M0_text_file] -div [sensitivity_image] -mul 6000 [absolute_CBF_output_image]

For these calculations the CBF image should still be in the native resolution of the ASL data. The first option (with M0 only) will work with perfusion images that have been converted to an another resolution, e.g. standard space.


---------------
asl_calib usage
---------------

Typing the asl_calib with no options will give the basic usage information, the following is a more detailed version:

-c <calib_data>  Calibration data in Nifti file format with the individual images stacked in the time dimension.
-s <structural_image>  Structural image used for determining reference 'tissue' mask (not required if reference 'tissue' mask is supplied, see below).
-t <asl->structural_transformation_matrix>  Transformation matrix for ASL images to structural image space, e.g. from ``asl_reg``, (not required if reference 'tissue' mask is supplied, see below).
--mode <mode>  Specify what form the calibration data takes, options are: longtr, satrecov. See below for mode specific options.
--tissref <Reference_tissue_type>  The 'tissue' type to use as a reference, see below, options are: ``csf, wm, gm, none``.
-te <TE_value>  TE of the calibration sequence in seconds, deafult is 0 s.
-i <perfusion_image>  A perfusion image for calibration. This should be still at the native resolution of the ASL data.

**Output options**

-o <absolute_CBF_image_name>  File to which absolute CBF image should be saved, if input image has been supplied with ``-i``.
--Mo <M0_value_save_file>  The estimated M0 value of arterial blood will be saved as text to a file of this name. This can then be used to convert a perfusion image into absolute values.

**Extended Options**

-m <CSF_mask>  Provide a 'tissue' reference mask, e.g. hand drawn, instead of relying upon automated mask creation. If a mask is supplied the structural image and ASL to structural transformation are no longer required.
-bmask <brain_mask>  A mask of the brain in (ASL native space), this will be used for sensitivity estimation (LongTR method) or T1 estimation (SatRecov method). If not supplied a brain mask will be generated automatically from the calibration data if it is needed, this option allows the same mask from other processing steps to be employed for consistency.
-t2star  Tells ``asl_calib`` to do T2* correction rather than T2 correction. This option simply alters which set of default T2(*) values are used.
-t1r <T1_reference_tissue>  T1 (in seconds) for the reference tissue, the defaults for the different ``--tissref`` options are (based on 3T): csf 3.4, gm, 1.3, wm 1.0.
-t2r <T2_reference_tissue>  T2(*) (in miliseconds) for the reference tissue, the defaults for the different ``--tissref`` options are (based on 3T) T2/T2*: csf 750/500, gm, 100/50, wm 50/20. These defaults are general estimates based on the literature and should be used with care.
-t2b <T2_blood> T2 (in miliseconds) for blood, the default is 150/50 (T2/T2*). The defaults are a general estimate based on the literature and should be used with care.

**Mode specific options**

*LongTR*

--tr <TR_value>  TR of the calibration sequence in seconds, default is 3.2 s.
--cagin <calibration_gain>  The relative gain of the ASL data to that of the calibration image, default 1. This allows for the case where the ASL data has been acquired with a higher gain than the calibration images, for example where background suppression was used allowing for a higher gain to be set for the ASL data.
-cref <calibration_reference_image>  A further image aquired using the same parameters as the main calibration file, but with a different coil to be used as a reference to calculate the sensitivity of the coil used for the main ASL data.
-osen <sensitivity_image_out_file>  Specify where the sensitivity file can be saved, if a reference image has been supplied with ``--cref``. This can be used later to correct an estimated CBF image for coil sensitivity.
-isen <sensitivity_image>  provide a sensitivity image (that matches the calibration image) to be used in calcuations.

*SatRecov*

--tis <List_of_tis>  Comma separated list of inversion times in the data (in seconds), e.g. ``--tis 0.2,0.4,0.6``.
--fa <Flip_angle>  Flip angle in degrees for Look-Locker readouts, do not set if not using Look-Locker.
--lfa <Low_flip_angle>  Low flip angle for Look-Lokcer readouts in which an extra set of TIs were acquired with a lower flip angle. This is used to estimate the correction for true flip angle at every voxel. It is assumed that the low flip angle data is the final phase (set of TIs) in the calibration data.
--nphases <number_of_phases>  The number of phases (sets of TIs) at the higher flip angle.

**'Tissue' reference type**

``asl_calib`` will let you choose what 'tissue' you want to use as the reference. M0 is calculated within a mask of this 'tissue', as the mean over all the voxels within the mask. This option tells ``asl_calib`` which 'tissue' from the automatic segmentation as well as what T1 and T2(*) values should be used.

By default ``asl_calib`` uses CSF as the reference because it is relatively easy to segment and a mask can be defined containing a reasonable number of voxels that do not suffer substantial partial volume effects. The automated masking is optimized to extract CSF from the ventricles and this is probably the best reference to use. However, ventricular CSF is likely to be in the region of lowest coil sensitivity for multi-channel coils, and the longer T1 value of CSF can lead to bias when the TR is comparatively short (< 5 seconds). White matter is a reasonable alternative as partial volume effects can be minimized to a good degree. Grey matter is generally not a good option for that reason.

**Automatic reference 'tissue' mask**

``asl_calib`` attempts to automatically generate the reference 'tissue' mask from the structural image, unless you supply your own custom mask with the ``-m`` option. It does this using ``FAST``, thus the normal caveats for segmentation when using that program apply, for example the structural image must already have been brain extracted.

Having a really perfect mask is not vital, since the M0 calcuation is performed over all the voxels within the mask. However, the mask needs to at least be sensible, hence it is a very good idea to check the mask created at the end. If ``asl_calib`` detects that after segmentation, transformation into ASL native space and thresholding, that there are no voxels in the mask it will halt and tell you that the automated method has failed.

