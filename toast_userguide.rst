=====================
TOAST User Guide
=====================

Usage
-----------

TOAST expects the input data without label-control subtraction being performed. A typical command line usage would be::

    toast -i <asl_data> -o <output_directory>  --infert1
 
This would carry out a model-based analysis of Turbo-QUASAR data and provide voxelwise quantification of perfusion and arterial transit time. Note: the current implementation of TOAST does NOT support dispersion correction, model-free analysis, or partial volume correction.

Output files
----------------

+------------------------+-----------------------------------------------------------+
| File name              | Description                                               |
+========================+===========================================================+
| ABV_absolute           | Arterial blood volume (in decimals) after calibration     |
+------------------------+-----------------------------------------------------------+
| Arrival_time_blood     | Arterial arrival time (in seconds) to macrovasculature    |
+------------------------+-----------------------------------------------------------+
| ATT                    | Arterial transit time (in seconds)                        |
+------------------------+-----------------------------------------------------------+
| calib_M0t              | M0 of tissue                                              |
+------------------------+-----------------------------------------------------------+
| CBF_absolute           | CBF (in ml/100g/min) in absolute units after calibration  |
+------------------------+-----------------------------------------------------------+
| M0a_for_absolute_CBF   | M0 of arterial blood used for calibration                 |
+------------------------+-----------------------------------------------------------+
| mask                   | Mask used in the analysis                                 |
+------------------------+-----------------------------------------------------------+
| T1_tissue              | T1 (in seconds) of tissue                                 |
+------------------------+-----------------------------------------------------------+

Sequence parameters
-------------------

A number of parameters are similar with QUASAR so users may wish to consult the user guide of QUASIL. Only the sequence parameters unique to Turbo-QUASAR are explained here.

--shift  Slice shifting factor to increase the effective temporal resolution. Default: 2
--break_1  Slice number of first acquisition point (start from 0). Default: 0
--break_2  Slice number of middle acquisition point (start from 0). Default: 7
--break_3  Slice number of last acquisition point (start from 0). Default: 14
--taupat	Specify the pattern of Turbo-QUASAR labeling pulses. Label: 1, no label: 0. Default: 1, 1, 1, 1, 1, 1, 1.

Extended options
---------------------------

These options include the estimation of T1 of tissue, correcting the partial volume effects of the calibration data, and estimation of the arterial blood volume.

--infert1  Estimate voxelwise T1 of tissue
--calib  Include a calibration image
--tr  TR (in seconds) of the calibration image. Default: 5.0 seconds.
--struct  Include a structural image
--corrcal  Includecorrection for partial volume effects present around the edges of the calibration image.
--inferart  Estimate voxelwise arterial blood volume (ABV or aCBV)



