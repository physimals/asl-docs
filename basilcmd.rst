===========================
BASIL (command) 
===========================

.. toctree::
   :maxdepth: 2

   basilcmd_userguide
   basilcmd_examples

The BASIL command line tool performs kinetic model inversion on ASL label-control difference data. It uses a common Bayesian inference method regardless of whether the data contains a single or multiple post labelling delays. BASIL includes a flexibly defined kinetic model appropriate for ASL kinetics that can be applied in humans and also other species - for more information see the model section.

To run BASIL on resting-state ASL data you will need:

- ASL difference data (single or multiple post labeling delays)
  
  - differencing of label and control images should have been done
    already, see ``asl_file``.
    
- Details of the sequence, i.e. post-lableing delay(s), bolus
  duration, etc.

Multi-step inference
-----------------------

BASIL runs in multiple steps increasing the model complexity at each
stage, this ensures a more robust final result by ensuring good
convergence upon the global solution in all voxels. In general we
recommend including the spatial prior/regularisaiton option that BASIL
offers, this is run as a final step.

A rough overview of the process would be:

- STEP 1: Bayesian inference - Inference for CBF and arrival time (and optionally label duration)
- STEP 2+: Bayesian inference - further parameters of the model can be
  inferred from the data.
- STEP N: Bayesian inference with spatial prior - a final run
  for all the parameters inlcuding a spatial prior on the perfusion
  parameter, initalised by the prior step. 


Kinetic model
-----------------------

The Kinetic curve model for resting state ASL is built into FABBER and
called by BASIL. The model implemented follows the 'standard' or
'Buxton' model, for more information see:

Buxton, R. B., L. R. Frank, et al., 'A general kinetic model for
quantitative perfusion imaging with arterial spin labeling', Magnetic
Resonance in Medicine 40(3): 383-396, 1998.

As per this paper, BASIL assumes by default a single well-mixed tissue
compartment and no dispersion of the bolus of labeled
blood water. Different T1 values are assumed for blood and tissue
water, but it is posisble to set these to be identical to match the
simple model assumed by the quantification formula in the 'white paper'.

BASIL also implements a range of alternative arterial input
functions - to model disperion - and residue functions - to model
restricted water exchange.

**Dispersion and Arterial Input Functions**

BASIL includes a number of Vascular Transport Function (Dispersion
Kernel) models of dispersion. These include modelling the VTF as
either a Gamma or Gaussian function. For more information see:

Chappell, M. A., Woolrich, M. W., Kazan, S., Jezzard, P.,
Payne, S. J., & MacIntosh, B. J. (2013). Modeling dispersion in
arterial spin labeling: validation using dynamic angiographic
measurements. Magnetic Resonance in Medicine, 69(2),
563–570. http://doi.org/10.1002/mrm.24260

Hrabe, J., & Lewis, D. (2004). Two analytical solutions for a model of pulsed arterial spin labeling with randomized blood arrival times. Journal of Magnetic Resonance, 167(1), 49–55.

**Exchange and residue functions**

As well as the single well-mixed tissue compartment model in which the
residue function just accounts for T1 decay (and a small venous
outflow), BASIL includes two-compartment exchange models as described
in the following papers:

Parkes, L., & Tofts, P. (2002). Improved accuracy of human cerebral
blood perfusion measurements using arterial spin labeling:
Accounting for capillary water permeability. Magnetic Resonance in
Medicine, 48(1), 27–41.

St Lawrence, K., Frank, J., & McLaughlin, A. (2000). Effect of
restricted water exchange on cerebral blood flow values calculated
with arterial spin tagging: A theoretical investigation. Magnetic
Resonance in Medicine, 44(3), 440–449.
    
