==================================================
asl_file: command line manipulation of ASL data
==================================================

``asl_file`` is a command line tool designed for the convenient manipulation of ASL data within FSL. It is part of the BASIL toolset (and is used extensively within the ``oxford_asl`` and ``Asl_gui`` tools).

ASL data has the relatively unique feature compared to other MRI datasets that it is comprised of an interleaved series of label and control images. Common manipulations of ASL data require either the pairwise subtraction of the volumes and/or the extraction of control (or label) images, this can be quite tedious with existing image file manipulation tools. This gets even more complicated with multi inflow-time ASL that contains label-control pairs at a range of inflow-times. ``asl_file`` was thus designed to know about the common structures of ASL data and permits direct operations without the need to separate out the individual volumes.

``asl_file`` also includes some more advanced features including:
- the ability to generate epochs of ASL data so that perfusion variations during acquisition can be investigated.
- simple partial volume correction using the Linear Regression method (this is an alternative to the spatial method implemented in BASIL itself).
- a simple routine to correct for partial volume effects at the end of the brain in the M0/calibration image that causes overstimation artifacts in voxelwise calibration.
