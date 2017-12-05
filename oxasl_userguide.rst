================
Oxford ASL User Guide
================

A typical usage would be::

    oxford_asl -i [asl_data] -s [struct_image] -t [struct2std_trans.mat] -c [M0_calib_image] 
               --tis 0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,2.0,2.2

This command would process the data specified by [asl_data] with the list of inverstion times --tis used in the data collection. The resulting tissue perfusion map is registered into standard space by way of the structural image [struct_image] and structural to standard transformation matrix [struct2std_trans.mat]. Finally a calibrated perfusion map (in ml/100g/min) is produced using the calibration image [M0_calib] and an automatically generated CSF mask. In this case the output image(s) will be placed in the current directory.

This performs calibration to get CBF in physiological units using the supplied calibration image. More advanced calibration options (and the use of saturation recovery of the control images) can be achieved using asl_calib separately. Oxford_asl will try to register the resulting CBF image to the structural image if provided. It is very important to inspect whether the registration has worked by examining the final result. There are a couple of options that can improve the robustness of registration. Advanced custom registration can be done using the native_space results directly and either asl_reg or flirt.


Output
------

The outputs from Oxford_ASL are a resting state perfusion image called perfusion.nii.gz, which provides blood flow in relative (scanner) units, and an arrival time image called arrival.nii.gz. If a calibration image has been supplied then a further image perfusion_calib.nii.gz is also produced, which is a flow map in absolute units (ml/100g/min).

If calibration was performed then a text file called M0b.txt will be created that saves the estimated M0 value from arterial blood. If a CSF mask was not supplied then the automatically generated one will also be saved in the output directory as csf_mask.nii.gz

A subdirectory is also created called native_space in which perfusion and arrival time images in the native resolution of the ASL data are saved. These are useful if you find the registration to be unsatisfactory, allowing a new registration to be performed without having to repeat the main analysis.

Usage
-----

Typing oxford_asl with no options will give the basic usage information, the following is a more detailed version:

 - ``-i [asl_data]`` this is the ASL data with the individual ASL images stacked in the time (4th) dimension. The number of volumes should match the number of TIs.
 - ``--tis TI1,TI2,TI3...`` This option specifies the list of inversion times used in the data acquisition, a comma separated list of values should be provided (that matches the order in the data). If the data contains multiple repeats of the same set of TIs then it is only necessary to list the unique TIs. In this case oxford_asl will take the mean of the values for each TI before model-fitting (if you dont want it to do this then list out all the TIs for every volume in the data explicitly).
 - ``-o (optional) [output_directory]`` use this to place the result in a different directory to the current working directory.
 - ``-s (optional) [struct_image]`` high resolution structural image (assumed to be T1 weighted or similar). If this is not provided then results will be provided in native space only.
 - ``-t (optional) [struct2std_trans.mat]`` transformation matrix that takes the structural image into standard space. This matrix is an output from the registration process carried out by FLRIT (this is a normal part of FEAT processing for fMRI data for a subject). If this is not supplied data will be output in structural space.
 - ``-S (optional) [std_image]`` use to specify the standard brain to which registration takes place - this should be the same image as was used in the production of the structural to standard transformation matrix. By default the MNI152_T1_2mm image is used, this is commonly used in other FSL tools.
 
**Acquisition specific**

 - ``--casl`` Data was acquired using cASL or pcASL labelling.
 - ``--bolus [bolus_duration]`` use this to specify the duration of the ASL tagging bolus used in the sequence (in seconds). This is assumed to be 1 second by default, the actual bolus length is estimated as part of the processing (unless you supply the --fixbolus option) - this value is used as the intial guess.
 - ``--t1 [T1_value]`` The T1 value of tissue, 1.3 s by default (assuming acquisition at 3T).
 - ``--t1b [T1b_value]`` The T1 value of arterial blood, 1.6 s by default (assuming acquisition at 3T).
 - ``--slicedt [timing_difference_value]`` For multi-slice acquisitions where superior slices are acquired later than those below. This provides the increase in time after labeling for a superior slice relative to the one directly below. It is assumed that the TIs provided refer to the lowest slice in the dataset.
 - ``--artoff`` Turn off correction for signal arising from ASL signal still within the (macro) vascualture, this might be appropriate if the acquisition employed flow suppression.
 - ``--fixbolus`` Turn off the automatic estimation of bolus duration, this might be appropriate if the bolus duration is well defined by the acquisition sequence (often true for cASL and pcASL, as well as when using pASL plus QUIPSSII).

**Calibration**

 - ``-c [M0_calib_image]`` specifies the M0 calibration image that is used to get flow values in absolute units. This should be an image with the repeated measurements stacked in the time dimension.
 - ``--csf (optional) [csf_mask]`` Image in the same space as the structural (or low res structural image if supplied) that is a mask of voxels containing CSF to be used in calibration. This is a further option of the calibration step and allows the CSF mask to be manually specified if the automated procedure fails.
 - ``--cgain (optional) [relative_gain_value]`` If the calibration image has been acquired with a different gain to the ASL data this can be specified here. For example, when using background suppression the raw ASL signal will be much smaller than the (non background suppressed) calibration image so a higher gain might be employed in the acquisition.
 - ``--t1csf (optional) [T1 value for CSF in s]`` Supply a value for the T1 of CSF to be used in the calibration process. Default values are used by asl_calib based on a 3T field strength (these can be checked by calling asl_calib at the command line).
 - ``--te (optional) [Echo time for readout in ms]`` Set the echo time for the reaodut so that T2(*) effects are taken into account in the calibration. If this is not supplied then TE = 0 ms is assumed, i.e. T2(*) effects are negligible. Default values are assumed by asl_calib for T2(*) values, you might wish to treat these with caution as these are estimates based on the literature.
 - ``--t2star (optional)`` Tells oxford_asl to correct for T2* rather than T2 effects. This simply tells asl_calib to use the default values for T2* in place of T2 in the calculations.
 - ``--t2csf (optional) [T2 value for CSF]`` Supply a value for the T2 of CSF to be used in the calibration process, only relevant if you supply the TE value. Default values are used by asl_calib based on a 3T field strength (these can be checked by calling asl_calib at the command line).
 - --t2bl (optional) [T2 value for blood] Supply a value for the T2 of blood to be used in the calibration process, only relevant if you supply the TE value. Default values are used by asl_calib based on a 3T field strength (these can be checked by calling asl_calib at the command line).

**Registration**

 - -r (optional) [low_res_struct]`` low resolution structural image used as an extra step in the registration to improve resulting transformation.
 - ``--regfrom (optional) [reg_source]`` An alternative image to use as the basis of registration. This should be the same resolution as the ASL data and aligned to it. The raw data before tag-control differencing or the calibration image are often a better reference for registration than the CBF image.

**Analysis**

 - ``--spatial`` Use spatial prior on the estimated CBF image. This exploits the spatial homogeneity (or smoothness) of the CBF image. This is somewhat similar to spatial smoothing the raw data, but it is adaptive and does not interact unfavorably with the non-linear kinetic curve modelling.
 - ``--infert1`` Incorporate uncertainty in the T1 values into the analysis.
 - ``--bat [BAT_value]`` Bolus arrival time value (in seconds). BAT is estimated directly from the data, but this option can be used to supply a different prior estimate from that used by default (0.7 seconds).
