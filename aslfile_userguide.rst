===================================
asl_file User Guide
===================================

A list of command line options can be found for ``asl_file`` by typing::
  
  asl_file -h

The basic usage is::

  asl_file --data=<asldata> --ntis=<number_if_inflow_times> [options]

This specifies the ASL data source file and the number of inflow-times present in the data. Note that inflow-time here is a genertic reference to the time between labeling and imaging: it refers to a post-labeling delay in pcASL or inversion time in pASL. For ``asl_file`` it is only necessary to specify the number of inflow-times in the file and not the individual parameters (i.e. the delay time) associated with them. 

Various options exits to specify the output required and, where needed, the structure of the data in the source and output files, as well as any operations that need to be done to the data.

Input options
---------------------

By default asl_file assumes that the input data is 'difference data', i.e. label-control subtraction has already been performed. It is often useful to use ``asl_file`` with data in the form of label-control pairs, this can be specified using the ``--iaf`` option.

``--iaf=diff`` Input data is differenced, pairwise label-control subtraction has already been performed.

``--iaf=tc`` Input data is label-control (tag-control) pairs, with the first volume being a tag (labelled) image.

``--iaf=ct`` Input data is label-control pairs, with the first volume being a control image.

``--iaf=tcb/ctb`` Input data contains label-control volumes, but all of the label and control images are grouped together within the data (in a 'block').

**Block format (multi inflow data)**

Additionally, where the data contains repeated volumes at different inflow times (multi inflow-time) it may be necessary to specify the 'block format', i.e. whether repeated measurements at the same inflow time are grouped together or appear grouped by repeat number.

``--ibf=rpt`` Volumes with the same inflow times have been grouped together. This is the inout format expected by the ``basil`` command line tool.
	      For example: **TI1 TI1 TI1 TI2 TI2 TI2 TI3 TI3 TI3**

``--ibf=tis`` Volumes are grouped as repeated of the same set of inflow-times. This is most common, since it reflects a usual acquisition strategy to iterate through the inflow-times repeatedly.
	      For example: **TI1 TI2 TI3 TI1 TI2 TI3 TI1 TI2 TI3**

**Numbers of repeats in the data**
	      
For multi inflow-time data, ``asl_file`` will automatically calcuate the number of repeats of each inflow-time present in assuming that theere is a same numer of each. For an acquisition where the number of repeats at each inflow time has been varies you can use the ``--rpts=<list>`` option to specify, as a comma separated list, the number of repeats of each inflow-time. Note this is only value when using ``--ibf=tis``.

**Brain mask (optional)**

``--mask=<image>`` Optionally a mask in which the processing is to be performed can be supplied. For most operations a mask is not essential, although will result in faster processing.

Output Options
-----------------

A filename for the output volume is specified by the ``--out=<filename>`` option. For multi inflow-time data the 'block format' for the output data can be specified (see above) using the ``--obf`` option, by default this matches the value of ``--ibf``.

Pre-output Operations
-------------------------

A number of operations can be applied to the data prior to output (these cannot be combined).

**Label-control (pairwise) subtraction**

``--diff`` Do a pairwise subtraction of odd volumes from even volumes, this will compute the difference data is the input image contains label-control pairs. For *N* volumes in the input image there will be *N/2* in the output image.

``--surdiff`` Do a pairwise subtraction of every sequential pair of volumes. This also produces label-control difference data, but performs subtraction of even from odd volumes as well as odd from even volumes (correcting for the sign difference in label-control subtraction that would ensue). For *N* volumes in the input image there will be *N-1* in the output image.

**Splitting label-control pairs**

``--spairs`` Split pairs within the data, i.e. split label and control images. The output from each output option (see below) will create two (rather than one) files with _odd and _even appended to the name given to the output option. These contain the result of the output operation odd and even volumes respectively.

**Partial volume correction**

Partial volume correction using the Linear Regression method can be performed by specifiying the following (requires ``--mask``):

``--pvgm=<image>`` An image of the partial volume of grey matter within every voxel within the mask (at the same resolution as the input data).

``--pvwm=<image>`` An image of the partial volume of white matter within every voxel within the mask (at the same resolution as the input data).

``--kernel`` the size of the kernel to be used, must be an odd number between 3 and 9, default 5. Note that ``asl_file`` uses a simple 2D (in plane) kernel.

**Edge correction**

To correct for edge effects in voxelwise calibration (a form of partial volume effect at the edge of the brain), ``asl_file`` can perform simple erosion and extrapolation on a calibration image if the option ``--extrapolate`` is specified. It is possible to control the neighbour size for extrapolation using the ``--neighbour=<value>`` option.


Output Operations
-------------------------

Apart from outputting the data subject to rearrangement of the internal structure using the output options or pre-output operations, further outputs can be generated after the other operations have been performed. You can supply muliple output options at the same time.

``--mean=<filename>`` Take the mean over the volumes, e.g. for the creation of the mean difference image from label-control pairs using the ``--diff`` option. For multi-delay data the mean is taken within each inflow-time, thus the final image will contain the same number of volumes as inflow-times specified by the ``--nti`` option.

``--split=<filenameroot>`` For multi inflow-time data split the data into separate files for each inflow time.

**Extracting epoch of data**

``--epoch=<filenameroot>`` Outputs as separate images the mean within individual epochs of the data.

 Parameters of the epochs are defined by
 
 ``--elen=<value>`` The length of each epoch in the specified epoch units.
 
 ``--eol=<value>`` The amount of overlap between epochs in the specified epoch units.
 
 ``--eunit=<...>`` The units to be used for the creation of the epochs.
 
   ``--eunit=rpt`` (default) Epochs are calculated with the unit of calculation being the number of repeats, this would always be appropriate for single inflow-time data. For multi inflow-time data the mean would be taken within each inflow-time in each epoch, thus each image would contain the same number of volumes as inflow-times specified by the  ``--nti`` option.
   
   ``--eunit=tis`` Specific to multi-inflow time data (and a very advanced option). This permits the creation of epochs from the raw time series such that each epoch will contain the specified number of volumes from the input data given by --elen, this could be a mixture of inflow-times (and repeats thereof) depending upon the ordering in the data.
