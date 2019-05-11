=========================================================
Cerebrovascular Reserve Quantification Using ASL Tutorial
=========================================================

Introduction
============

Cerebrovascular reserve (CVR) is defined as the maximum change in perfusion in response to a vasoactive stimulus. CVR has become an important biomarker to assess tissue health. ASL can be a non-invasive technique to measure CVR in vivo. In this tutorial, we are going to explore how to apply ASL to quantify CVR induced by a vasoactive stimulus.


CVR Experiment Design
======================
Measuring CVR requires the quantification of perfusion at two different physiological conditions: baseline and stimulus. In the baseline condition, it is common for us to follow the routine procedures where we acquire data while the subject is in a resting state in the scanner. In the stimulus condition, we need to administer a stimulus to manipulate the perfusion of the subject. In this tutorial, we are going to use acetazolamide, a commonly used vasoactive stimulus administered through intravenous injection. The following diagram illustrates the basic design of our CVR experiment.

.. image:: /images/cvr_tutorial/CVR_experiment.png

In this experimental design, we could see that we would perform the identical acquisition before and after the injection of acetazolamide (the vasoactive stimulus). Since acetazolamide affects the flow velocity of the arterial blood, which could further affect the inversion efficiency of ASL, we would also include a phase contrast MRI scan to estimate the flow velocity and the inversion efficiency to improve the accuracy of perfusion estimation in ASL. In this tutorial, we are going to use single-PLD PCASL as our ASL technique.


Data Analysis
=============
Once we have collected our data, we would perform the analysis to quantify the perfusion at baseline and stimulus conditions as well as estimate CVR using these two perfusion measurements.

The perfusion quantification follows the same procedure as we learned in the BASIL tutorial except that the inversion efficiency of the baseline and stimulus conditions are different.

For the baseline perfusion quantification, we are going to use the parameter values shown in the following three screenshots to setup BASIL. Note that the inversion efficiency of baseline remains the same with the default value (0.85).

.. image:: /images/cvr_tutorial/baseline_data.jpg
.. image:: /images/cvr_tutorial/baseline_calib.jpg
.. image:: /images/cvr_tutorial/baseline_output.jpg


For the stimulus perfusion quantification, we will need to change the inversion efficiency value to 0.80. This can be estimated using Bloch equation simulation on the flow velocity from the phase contrast MRI data.

.. image:: /images/cvr_tutorial/stimulus_data.jpg
.. image:: /images/cvr_tutorial/stimulus_calib.jpg
.. image:: /images/cvr_tutorial/stimulus_output.jpg


After we have quantified the absolute perfusion of baseline and stimulus, we are going to apply the following formula to estimate CVR.

.. math::
	CVR=\frac{CBF_{stimulus}-CBF_{baseline}}{CBF_{baseline}}\times 100\%

This can be done using the ``fslmaths`` command::

    fslmaths output_stimulus/native_space/perfusion_calib -sub output_baseline/native_space/perfusion_calib -div output_baseline/native_space/perfusion_calib -mul 100 CVR


Results
=======
Finally, we may use FSLeyes to view the CVR results:

.. image:: /images/cvr_tutorial/CVR_results.jpg
