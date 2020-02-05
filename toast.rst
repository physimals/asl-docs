===========================================
TOAST - quantification of Turbo-QUASAR data
===========================================

Overview
========

TOAST is a pipeline designed to quantify the hemodynamic parameters of Turbo-QUASAR data. Turbo-QUASAR is a PASL based technique that improves upon the SNR of QUASAR using multiple labelling pulses while preserving the application of crushing gradients and the Look-Locker readout multi-TI acquisition in QUASAR. Each labelling pulse creates a sub-bolus, and the duration of each sub-bolus is equal to the time between each acquisition under optimal blood flow velocity. TOAST uses full Turbo-QUASAR data to produce perfusion in absolute units as well as arterial transit time and ABV images. TOAST also include the option to correct MT effects and estimate the duration of sub-boluses.

More information on the model used can be found in:

  *Zhao M Y, Václavů L, Petersen E T, Biemond B J, Sokolska M J, Suzuki Y, Thomas D L, Nederveen A J, Chappell M A, (2019). Quantification of Cerebral Perfusion and Cerebrovascular Reserve Using Turbo-QUASAR Arterial Spin Labeling MRI. Magnetic resonance in medicine. https://doi.org/10.1002/mrm.27956*

  *Chappell, M. A., Woolrich, M. W., Petersen, E. T., Golay, X., & Payne, S. J. (2012). Comparing model-based and model-free analysis methods for QUASAR arterial spin labeling perfusion quantification. Magnetic resonance in medicine. doi:10.1002/mrm.24372*

  *E. T. Petersen, J. B. De Vis, C. a. T. van den Berg, and J. Hendrikse, “Turbo-QUASAR: a signal-to-noise optimal arterial spin labeling and sampling strategy,” Proc. Intl. Soc. Mag. Reson. Med. 21 2146., vol. 60, no. 6, p. 2146, 2013.*

Turbo-QUASAR Description
------------------------
As an improvement of the QUASAR method, Turbo-QUASAR was designed to overcome the low SNR of PASL when compared to PCASL by applying a series of labeling pulses to create a longer effective bolus duration. These labeling pulses are inserted between readout (also replacing the QUIPPS II pulse used in QUASAR) to maintain the magnetization level of the tracer for a longer period than conventional PASL techniques, thus increasing the overall SNR of the resulting ASL data. The figure below shows the different labeling techniques and the associated arterial input function for QUASAR, Turbo-QUASAR, and PCASL.

.. image:: /images/turbo_quasar/Turbo_QUASAR_description.png

Magnetisation Transfer (MT) effects in Turbo-QUASAR
---------------------------------------------------
Due to the RF pulses in the label and control experiments of Turbo-QUASAR, MT effects could potentially affect the estimation accuracy of CBF. Turbo-QUASAR uses Look-Locker readout and the spins follows a saturation recovery. The figure below shows the saturation recovery curve for spins at different locations of the brain. The dash line indicates the time point that the labeling stopped. In essence, the MT effects have a stronger influence to spins that are closer to the labeling region. A correction method has been implemented in TOAST to correct the MT effects by modeling the saturation recovery signal in two parts: (1) under the influence of MT effects and (2) without the influence of MT effects. The correction is achieved by executing the --infert1 option (default).

.. image:: /images/turbo_quasar/Turbo_QUASAR_MT_effects.png

User Guide
==========

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



