===========================
BASIL (command) User Guide
===========================

-------------
Calling BASIL
-------------

A typical call to BASIL would look like::
  
  basil -i asldiffdata.nii.gz -m mask.nii.gz -o basilout --spatial -@ basil_params.txt

You should always supply a parameter file using the ``-@`` option (see
parameter file)

We highly recommend the use of the ``--spatial`` option for automated
spatial regularisation of your data.

**Basic options**

BASIL can be called from the command line with the following information:

-i <file>  Input file containing label-control differenced data.
-m <file>  Brain mask for the data.
-o <dir>  Name of directory into which results are to be written (default is a subdirectory called basil within the input directory).
--optfile <file>  Model and sequence parameters (to be passed to FABBER) (was previouosly ``-@``).
--spatial  Apply a spatial regularising prior to the estimated perfusion image, this is preferable to spatial smoothing of the data before analysis.
  
**Model options**
   
BASIL provides a number of options to access more advanced parts of
the kinetic curve models, you should consult the literature to
determine whether you want to explore these model options (the
Further Reading and Literaure sections for BASIL should be a good start):

--infertau  Infer the bolus duration from the data.

 This option is particularly suitable for pASL data in which the bolus duration is undefined (e.g. when not using QUIPSSII or Q2TIPS)
    
--inferart  Include an arterial compartment in the model.
  
  This option will infer the arterial blood volume (aCBV) and arterial blood arrival time.
  This option is suitable for data with multiple post-labelling delays, especially where short PLD (or TIs) are used.
    
--inferpc  Include a non-exchanging compartment in the model.
  
  This option might be used to model pre-capillary vessels assuming minimal water exchange.
  This parameter adds a pre-capillary transit time parameter.
    
--infert1  Infer the values of T1 and T1b from the data.
  
  This option is primarily to account for uncertainty in the T1 values
  in the inference. ASL data does not have sufficient sensitivity to T1 to estimate it accurately.

**Advanced Options**
    
BASIL also has a few more advanced options:

--t1im  For loading a image of T1 (tissue) values to be used in the kinetic modelling (same resolution as the ASL data).
--fast=<value>  Use a value of ``2`` to perform the analysis in a single step, mostly for use with --spatial. A value of ``1`` reduces the number of iterations performed in each step.
--pvgm  Perform partial volume correction with the supplied partial volume estimates for grey and white matter (these should be the same resolution as the ASL data).
--pvwm  White matter partial volume estimates (to go with ``--pvgm``).
--init  Initialise BASIL with the results of a previous run - this option expects the ``finalMVN.nii.gz`` image from a previous ``basil`` run (model specification must match - use with caution).



**Kinetc model choice**
    
BASIL also offers a number of variants on the kinetic model used:

--disp=<option>  Model of the label dispersion

  - ``--disp=none``  No dispersion.
  - ``--disp=gamma``  Dispersion modelled according to a gamma dispersion kernel (vascular transport function).
  - ``--disp=gauss``  Dispersion modelled according to a Gaussian dispersion kernel.
  - ``--disp=sgauss``  Dispersion modelled according to a spatially (rather than temporally) derived Gaussian dispersion function.
  
--exch=<option>  Model of the exchange of labeled water in the capilliary bed (selects the residue function).

  - ``--exch=mix``  Well-mixed single compartment
  - ``--exch=simple``  Simple single compartment with T1 of blood (mimics the assumptions made in the white paper)
  - ``--exch=2cpt``  A two compartment exchange model following Parkes & Tofts (by default the slow solution is used).
  - ``--exch=spa``  An implementation of the single pass approximation from St. Lawrence.

BASIL assumes by default a single well-mixed tissue
compartment (``--exch=mix``) and no dispersion of the bolus of labeled
blood water (``--disp=none``).

   
BASIL parameter file
----------------------
BASIL requires a text file in which you specify model parameters, plus
information about the collected data. 

A generic BASIL options file for single-PLD pcASL (at 3T) might look like (preceding a line with # indicates it is a comment and will be ignored)::

    # Sequence/scanner parameters
    --casl
    --t1=1.3
    --t1b=1.65
    --tau=1.8
    # tau specified label/bolus duration

    # Data information
    --repeats=10 --pld=1.8
      
An generic file for multi-TI pASL might look like::

     # Sequence/scanner parameters
    --t1=1.3
    --t1b=1.65
    --tau=0.7

    # Data information
    --repeats=10 --ti1=0.25 --ti2=0.5 --ti3=0.75 --ti4=1.0 --ti5=1.25 --ti6=1.5 --ti7=1.75 --ti8=2.0

**Model parameters**

By default BASIL assumes that your data is pulsed ASL (pASL), if you are using continuous (cASL) or pseudo continuous (pcASL) labelling then you should set the cASL option:

--casl  Use the cASL version of the model (NOTE: the default ATT value is likely to be poorly suited to pcASL/cASL data, see below).

For the model you can set the appropriate values of T1 (and T1b) as well as the duration of the label as set by your sequence, if these are not specified in the parameter file then the default values are used:

--t1=<value>  The value of T1 (default 1.3 seconds).
--t1b=<value>  The value of T1b (default 1.65 seconds).
--t1wm=<value>  The T1 value of white matter (default 1.1 seconds) - only for partial volume correction.

You can set an appropriate Arterial Transit Time (sometimes called
Bolus Arrival Time) value. This will be used as the mean of the prior
distribution for the ATT parameter during inference, i.e., the default
value for ATT which will be updated based on the data.

--bat=<value>  The value of ATT (aka Bolus Arrival Time) (default 0.7 seconds).

NOTE: in ``oxford_asl`` the default ATT is automatically changed from
0.7 seconds to 1.3 seconds for cASL/pcASL. This does not happen in
``basil``, you need to do this using the ``--bat`` option.

--batsd=<value>  The value of the standard deviation for the ATT prior distribution (default 0.316 seconds).

The default value is appropriate if you are treating ATT as a confoud. If you are
interested in estimating ATT from multi-PLD/TI ASL you may wish to use
``--batsd=1``, the default value chosen by ``oxford_asl``.

Some models variants will have their own specific options, see Kinetic Model.

**Data Parameters**

Alongside model information the parameter file also contains
information about the data, including the post-label delay(s) for
pcASL or the inversion times for pASL and how many repeats of each are
contained in the file.    You should specify each PLD/TI individually in the order that they appear in the data.

Post Label delay(s)

--pld=<value>  The time (in seconds) for the PLD in single-PLD cASL/pcASL.
--pld1=<value>, --pld2=<value>, --pld-n-=<value>  The time (in seconds) of the *n*\ th PLD in multi-PLD cASL/pcASL.

Inversion time(s)
   
--ti1=<value>, --ti2=<value>, --ti-n-=<value>  The time (in seconds) of the *n*\ th TI for multi-TI pASL.

Label duration(s)
   
--tau=<value>  Label bolus duration (default is infinite).
--tau1=<value>, --tau2=<value>, --tau-n-=<value>  Label duration for the nth PLD measurement. Used where pcASL has been applied with different label durations.

A fixed bolus duration is set in any cASL/pcASL implementation.
For pASL a fixed bolus duration is often implemented using QUIPSS2 for example. If the bolus length is not fixed, e.g. FAIR then BASIL can estimate the bolus duration from multi-TI data if you use the ``infertau`` option when calling BASIL.
     
Slice timing

--slicedt  The time (in seconds) between acquisition of different slices in a 2D multi-slice readout. This is used to adjust the PLD for more superior slices (this assumes that the most inferior slice is acquired first with a PLD/TI that matches the value supplied via ``--pld`` or ``--ti``).

Look-locker readout (for multi-PLD/TI)
    
--FA=<value>  The flip angle in a Look-Locker readout scheme.

Flow suppression (multiple phases)
   
--crush1=<value>, --crush2=<value>, --crush-n-=<value>  Specification of the flow suppressing
   crusher direction for the nth PLD/TI. Any one of ``xyz, -xyz, x-yz,
   -x-yz``.

Time or Hadamard encoding

BASIL is directly compatible with time/hadamard encoding where
'decoding' has been performed. In that case the multi-PLD data can be
used exactly like any other multi-PLD pcASL with suitable setting of
the PLDs and label duration.

BASIL can also directly estimate perfusion from 'raw', i.e. not
decoded, data. Although this is currently limited to specific cases -
largely ones that use the same duration for each of the encoded
blocks. To use this option the input data is the raw data as acquired
and you tell BASIL the number of cycles to expect,  you shoud specify
the appropriate **single** PLD
and label duration values.

--hadamard=<value>  Labeling has been performed using hadamard encoding with the number of cycles specified, and the data has not been 'decoded' prior to being input to BASIL.
  
For this analysis it is necessary to also infer the static tissue component (that would otherwise have been removed during decoding). Thus the following options need to be added to the basil options file: ``--incstattiss --inferstattiss``
      
--fullhad  When the full Hadamard matrix is needed. This is for the case where the hadamard encoding included the first 'column' of all control boluses. (If this doesn't mean anything to you, the chances are that it isn't relevant).
   
Repeated measurements

--repeats=<n>  The number of repeats of each PLD or TI in the data (default is 1).

BASIL processes data where there are multiple measurements at the same
PLD/TI, as indicated by the ``--repeats`` option: in which case it is
assumed that the data comes with the individual time points in the 4th
dimension, with **repeats at each PLD/TI coming in blocks (gorups)**. Suitable manipulation of the data can be done using asl_file.

For example: the data contains 8 readings taken at 4 TIs (0.5, 1, 1.5,
2 seconds), repeated twice. It should be presented to BASIL with each TI grouped together

i.e. TI1 TI1 TI2 TI2 TI3 TI3 TI4 TI4

Hence the parameter file would contain::

    --ti1=0.5 --ti2=1 --ti3=1.5 --ti4=2 --repeats=2

NOTE that the number of TIs specified multiplied by the number of repeats should equal the number of time points in the 4D input data set.

It is possible to deal with more complicated data by specifying an
individual ``--ti[n]=`` for every time point in the data, for the
above example we could equally input it to BASIL as::

    --ti1=0.5 --ti2=0.5 --ti3=1 --ti4=1 --ti5=1.5 --ti6=1.5 --ti7=2 --ti8=2
   
Results (outputs)
--------------------------

Within the output directory a number of subdirectories will be created containing the results from each step these comprise:

- ``info.txt`` Text file containing information from BASIL about what was done in this step.
- ``paramnames.txt`` A list of names of the parameters inferred, these will correspond with the names of the results files.
- ``mean_{paramname}.nii.gz`` The parameter estimate image for paramname.
- ``var_{paramname}.nii.gz`` The estimate variance image for parameter paramname.
- ``zstat_{paramname}.nii.gz`` A pseudo z-statistic image for paramname, uses variance information to give a measure of the confidence with which that parameter deviates from 0.
- ``finalMVN.nii.gz`` All the parameter estimates and variances
  (including noise parameters) in one file. This can be interrogated with mvntool and can be used to initalise a further run of BASIL.
- ``logfile`` The logfile from FABBER.
- ``FreeEnergy.nii.gz`` Images of the free energy from FABBER, see
  references for more information.

Depending upon the model options chosen there will be a range of
parameters for which results will be provided. The multi-step nature
of basil means that more parameters are likely to be found in the
later steps, as models of increasingly complexity are fit as the step
number is increased.

Typical parameter names from BASIL are:

- ``ftiss`` (relative) tissue perfusion.
- ``delttiss`` arterial transit time (transit time or bolus arrival time to the tissue component). 
- ``fblood`` (relative) arterial cerebral blood volume, the scaling parameter of the arterial/macrovascular component.
- ``deltblood`` bolus arrival time (to arterial component).
- ``fwm`` (relative) white matter perfusion.
- ``deltwm`` arterial transit time for white matter.

Noise Model (Advanced option)
-----------------------------

BASIL assumes that you wish to use a standard white noise model to
analyse resting-ASL data. This model assumes that the noise in each
voxel can be described by a single noise magnitude, this is sufficient
in practice for most ASL data. If you are feeling adventurous (or have
good reason) you may instruct BASIL to use different noise magnitudes
for different sections of the input data, e.g. a different value at
each inversion time.

This is done in the parameter file using the ``--noise-pattern=``
option, which is used as follows: Taking the example of data with 4
TIs each repeated 5 times, to get a different noise magnitude at each
inversion time use::

--noise-pattern=11111222223333344444

i.e. the first 5 entries correspond to the first TI and these should
use the first noise magnitude, the next 5 entries are the next TI and
next noise magnitude etc. The numerbs here are purely labels and do
not relate to the actual magnitude of the noise, which will be estimed
by ``basil`` from the data.

NOTE: if you have more than 9 TIs then for the 10th TI and onward
letters should be used in place of numbers starting with a, i.e. for
12 TIs and 2 repeats::

--noise-pattern=112233445566778899aabbcc

NOTE: if you have only a small number of repeats (like these examples) then this more complex noise modelling is probably not a good idea.
