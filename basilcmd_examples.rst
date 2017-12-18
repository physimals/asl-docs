==========================
BASIL (command) Examples
==========================

The following provides some examples of the usage of the BASIL command line tool.

-------------------------------
Single PLD pcASL
-------------------------------

This example uses the single-PLD pcASL data from the Oxford
Neuroimaging Primer: Introduction to Perfusion Quantification using
Arterial Spin Labelling MRI. This can be found here_.

.. _here: http://www.neuroimagingprimers.org/examples/introduction-to-perfusion-quantification-using-asl/

Firstly, we need a mask in which to do the analysis. We will form a
very simple mask using BET on the raw ASL data (more robust options
are typically used in ``oxford_asl`` based on the structural image if
available).::
  
  bet asltc.nii.gz asltc_brain -m

Secondly, we need to do label-control subtraction prior to basil
analysis, we can use ``asl_file`` for this (for more informtion see
the asl_file examples).::
  
  asl_file --data=asltc.nii.gz --ntis=1 --iaf=tc --diff --out=diffdata

For analysis we need a basil_options.txt file. For this data the
following file specifies all the information we need, taking the
default values of T1 as adequate.::
  
  #BASIL options file
  --casl
  --bolus=1.8
  --pld=1.8
  --repeats=30

Finally, we can perform the analysis.::
  
  basil -i diffdata.nii.gz -o basilout -m asltc_brain_mask -@
  basil_options.txt --spatial

We have used the recommened ``spatial`` option in this case. The
terminal should display an output similar to::
  
  Creating output directory: basilout
  STEP 1: VB - Tissue
  ----------------------
  Welcome to FABBER v3.9.2-36-g4ba2db9
  ----------------------
  Logfile started: basilout/step1/logfile
  100%
  
  Final logfile: basilout/step1/logfile
  STEP 2: Spatial VB Tissue - init with STEP 1
  ----------------------
  Welcome to FABBER v3.9.2-36-g4ba2db9
  ----------------------
  Logfile started: basilout/step2/logfile
  100%

  Final logfile: basilout+/step2/logfile
  End.

Note that BASIL has run in two steps, the second step is 'spatial' and
was intialised by the first step. In both steps only a tissue
component was inferred.

The contents of the ``basilout`` directory should look something
like::
  
  logfile	params.txt	step1	step2

Both ``step1`` and ``step2`` contain a similar set of files, the
difference in this case being whether the spatial method was applied or
not. In general, the contents of the highest numbered step
subdirectory is the result you will want.

The ``step2`` subdirectory should have contents similar to::
  
  finalMVN.nii.gz        mean_delttiss.nii.gz   noise_stdevs.nii.gz    std_ftiss.nii.gz       zstat_ftiss.nii.gz     
  info.txt               mean_ftiss.nii.gz      paramnames.txt         uname.txt              
  logfile                noise_means.nii.gz     std_delttiss.nii.gz
  zstat_delttiss.nii.gz
  
Of most interest in this case is ``mean_fitss.nii.gz`` which is the
(relative) tissue perfusion image. If you compare this to the same
file in the ``step1`` subdirectory you will be able to see the
difference that the spatial prior makes in this case.

Of note are:

- ``std_fitss.nii.gz`` an estimate of the standard deviation on the
  tissue perfusion estimates.
- ``mean_delttiss.nii.gz`` since this is single-PLD data this image
  looks like the mask we supplied with a value of 1.3, which is the
  default value for the ATT parameter for pcASL. Since we cannot
  estimate ATT from single-PLD pcASL data, BASIL has applied the
  default value in the model inference for us. If we had wanted a
  different value we could have set that using the ``--bat=<value>``
  option in the basil_options.txt file.

-------------------------------
Multi PLD pcASL
-------------------------------

This example uses the multi-PLD pcASL data from the Oxford
Neuroimaging Primer: Introduction to Perfusion Quantification using
Arterial Spin Labelling MRI. This can be found here_.

As in the single-PLD example we need a brain mask::

  bet asltc.nii.gz asltc_brain -m

We need to do label-control subtraction::

  asl_file --data=asltc.nii.gz --ntis=6 --iaf=tc --diff --out=diffdata

Note that this data has six PLD, hence ``--ntis=6``. Also note that
helpfully the call to ``asl_file`` calcuates the number of repeats for
us::

  Number of voxels is:98304
  Number of repeats in data is:8
  Done.

We need a ``basil_options.txt`` file that includes a specification of the PLD in the
data::

   #BASIL options file
  --casl
  --bolus=1.8
  --pld1=0.25 --pld2=0.5 --pld3=0.75 --pld4=1.0 --pld5=1.25 --pld6=1.5
  --repeats=8

We are ready to call basil::

  basil -i diffdata.nii.gz -o basilout -m asltc_brain_mask -@
  basil_options.txt --spatial

Which procduces an output that is essentially identical to that for
the single-PLD case (as we are doing the same analysis here, just on
different data). Note that if you are running this example after the
single-PLD case you will get ``basilout+`` as your output directory,
``basil`` preserves any existing directories with the same name as the
output directory specified.

As with the single-PLD example we can examine the perfusion image from
the highest numbered step: ``mean_ftiss`` in subdirectory
``step2``. We can now also examine the ATT map ``mean_delttiss``.

Being multi-PLD data, we might consider a more advanced analysis. For
example, we could add an arterial (or macrovascular) component to the
model::

  basil -i diffdata.nii.gz -o basilout -m asltc_brain_mask -@
  basil_options.txt --spatial --inferart

This gives a three step analysis::
  
  Creating output directory: basilout+
  STEP 1: VB - Tissue
  ----------------------
  Welcome to FABBER v3.9.2-36-g4ba2db9
  ----------------------
  Logfile started: basilout+/step1/logfile
  100%
  
  Final logfile: basilout+/step1/logfile
  STEP 2: VB - Tissue Arterial - init with STEP 1
  ----------------------
  Welcome to FABBER v3.9.2-36-g4ba2db9
  ----------------------
  Logfile started: basilout+/step2/logfile
  100%
  
  Final logfile: basilout+/step2/logfile
  STEP 3: Spatial VB Tissue Arterial - init with STEP 2
  ----------------------
  Welcome to FABBER v3.9.2-36-g4ba2db9
  ----------------------
  Logfile started: basilout+/step3/logfile
  100%
  
  Final logfile: basilout+/step3/logfile
  End.

The arterial component was added in step two, with the spatial prior
applied in the third and final step.

Now in the output directory are three subdirectories for the different
steps. In the both ``step2`` and ``step3`` you will find, alongside
the files present in the previous analysis, files related to the
arterial cerebral blood volume parameter, named ``fblood``.

