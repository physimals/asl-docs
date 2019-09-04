===============
Oxford_ASL
===============

.. toctree::
   :maxdepth: 2
   
   oxasl_userguide
   
Overview
-----------------

Oxford_ASL is an automated command line utility that can process ASL
data to produce a calibrated map of resting state tissue perfusion. It
also includes a range of other useful analysis methods inlcuding
amongst others:

- motion correction
- registration to a structural image (and thereby a template space)
- partial volume correction
- distorition correction

If you have ASL data to analyse, ``oxford_asl`` is most likely the tool
you will want to use, unless you want a graphical user interface. In
practice, the GUI in BASIL is largely a means to construct the right
call to ``oxford_asl``.


What you will need
-------------------------
As a minimum to use ``oxford_asl`` all you need are some ASL data (label
and control pairs). In practice you will also most probably want:

- *a calibration image*: normally a proton-density-weighted image (or
  a close match) acquired with the same readout parameters as the main
  ASL data. Only once you have a calibration image can you get
  perfusion in absolute units.
- *a structural image*: it is helpful to have a structral image to pass
  to ``oxford_asl`` and if your data incldues this we strongly suggest
  you do use it with ``oxford_asl``. By preference, we strongly
  suggest you process your structural image with ``fsl_anat`` before
  passing those results to ``oxford_asl``. This is a good way to get
  all of the useful information that ``oxford_asl`` can use, and you
  can scrutinise this analysis first to check you are happy with it
  before starting your ASL analysis.
- *multi-delay ASL*: the methods in ``oxford_asl`` are perfectly
  applicable to the widely used single delay/PLD ASL acquisition. But,
  they offer particular advantages if you have multi-delay/PLD data.

Examples
-------------------------

An extensive set of examples of the use of ``oxford_asl`` (for pcASL)
is availabe as part of the primer:

*Introduction to Perfusion Quantification using Arterial Spin
Labelling*, Oxford Neuroimaging Primers, Chappell, MacIntosh & Okell,
Oxford University Press, 2017.

The examples themselves are freely available online at the primer
website: neuorimagingprimers.org, you can access the ASL examples
directly here_.

.. _here: http://www.neuroimagingprimers.org/examples/introduction-to-perfusion-quantification-using-asl/

Things to note
-------------------------
To produce the most robust analysis possible ``oxford_asl`` includes a
number of things in the overall analysis pipeline that you might want
to be aware of:

- *spatial regularisation*: this feature is now enabled by default for
  all analyses and applies to the estimated perfusion image. We do not
  recommend smoothing your data prior to passing to ``oxford_asl``. If
  you really want to, only do 'sub-voxel' level of smoothing.
- *masking*: ``oxford_asl`` will attempt to produce a brain mask in
  which perfusion quantification will be performed. This is normally
  derived from any structural images with which it is provided (highly
  recommened), via registration. Therefore, if the registration is
  poor there will be an impact on the quality of the mask. Where no
  structural information is provided, the mask will be derived from
  the ASL data via brain extraction, this can be somewhat variable
  depending upon your data. It is thus **always** worth examining the
  mask created. ``oxford_asl`` provides the option to input your own
  mask where you are not satisfied with the one automatically
  generated or you need a specific mask for your study.
- *registration*: ``oxford_asl`` performs the final registration
  using the perfusion image and the BBR cost function. We have found
  this to be reliable, as long as the perfusion image is of
  sufficient quality. In practice, an initial registration is done
  earlier in the pipeline using the raw ASL images and this is used
  in the mask generation step. You should **always** inspect the
  quality of the final registered images.
- *multiple repeats*: ASL data typically contains many repeats of the
  same measurement to increase the overall signal-to-noise ratio of
  the data. You should provide this data to ``oxford_asl``, and not
  average over all the repeats beforehand (unlike earlier versions of
  the tool). ``oxford_asl`` now inlcudes a pipeline where it intially
  analyses the data having done averaging over the repeats, followed
  by a subsequent analysis with all the data - to achieve both good
  robustness and accuracy. If your data has already had the repeats
  averaged, it is still perfectly reasonable to do analysis with
  ``oxford_asl``, if you have very few measurements in the data to pass
  to ``oxford_asl`` you might want to use the special 'noise prior'
  option, since this sets information needed for spatial regularisation.
- *Avanced analyses*: Partial volume correction, or analysis of the
  data into separate epochs, are avaialbe as advanecd supplementary
  analyses in ``oxford_asl``. If you choose these options
  ``oxford_asl`` will *always* run a conventional analysis first, this
  is used to intialise the subsequent analyses. This also means that
  you can get both conventional and advanced results in a single run
  of ``oxford_asl``.

