COPO submissions (DToL, ERGA)
=========================

Download old filelist if a submission exists. Create new filelist (either just the new files or all files; can use the 
one produced by ST download filelist button or simple ls command).
Use python scripts/filelist_to_filelist_nojson.py <old_filelist> <new_filelist> > new_submission_filelist.tsv

This script checks the files in the new_filelist, if they're new it gets relevant metadata from BioSamples and creates a 
submission filelist including the files and metadata in the old_filelist.

Darwin Tree of Life sample images
=================================

This repository contains code and notes related to hosting sample-associated images for the Darwin Tree of Life, and wider biodiversity projects.

Process
-------

1. Populate individual GAL collections (?). NHM at least.
2. Extract from these images, so that these are named by biosamples ID.
3. Use this to construct a new submission.

After 2., we have a directory like this:

    SAMEA111458765_1.jpg
    SAMEA111458765_2.jpg
    SAMEA111458765_3.jpg
    SAMEA111458765_4.jpg
    SAMEA111458769_1.jpg
    SAMEA111458769_2.jpg

Code
----

TODO
----

Fix ordering of multiple samples for a single thing.

Notes
-----

https://www.ebi.ac.uk/biostudies/files/S-BIAD588/C9K02TWY%20-%20Imported%20to%20EMu/NHMUK%20013696854%20(1).JPG

https://www.ebi.ac.uk/biosamples/samples/SAMEA111458349

Fields:

BioSamples ID
GAL_sample_id
collecting institution
geographic location (country and/or sea)
geographic location (latitude)
geographic location (longitude)
geographic location (region and locality)
organism
organism part
sample collection device or method

Warning: Not all BioSamples records have all of these fields (e.g. see SAMEA14448162)

Principles
----------

Pull everything from Biosamples record?

Comments/queries
----------------

What about:

cp C9K02U9Z and C9X0CNI7 - Imported to EMu/014425714 (2).JPG NHMUK014425714_1.jpg
cp C9K02U9Z and C9X0CNI7 - Imported to EMu/014425714 (3).JPG NHMUK014425714_2.jpg
cp C9K02U9Z and C9X0CNI7 - Imported to EMu/014425714.JPG NHMUK014425714_3.jpg
cp C9K02U9Z and C9X0CNI7 - Imported to EMu/014425714_dorsal.JPG NHMUK014425714_4.jpg
cp C9K02U9Z and C9X0CNI7 - Imported to EMu/014425714_lateral.JPG NHMUK014425714_5.jpg
cp C9K02U9Z and C9X0CNI7 - Imported to EMu/014425714_ventral.JPG NHMUK014425714_6.jpg
cp C9K02U9Z and C9X0CNI7 - Imported to EMu/014425714_ventral_2.JPG NHMUK014425714_7.jpg