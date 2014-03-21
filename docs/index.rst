.. VirAmp documentation master file, created by
   sphinx-quickstart on Mon Mar 17 10:38:15 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to VirAmp's documentation!
==================================

Viramp is a galaxy-based system for fast virus genome assembly and variation discovery.

The Script/vamp directory contains all the scripts and galaxy tool config files, place the folder under galaxy-dist/tools.

Place the tool_config.xml in config under 'galaxy-dist'.

Proftpd configuration as in 'config/proftpd.conf'.

To get everything running, your will need the following softwares installed:

1. seqtk for quality trimming : https://github.com/lh3/seqtk
2. diginorm for error correction and coverage reduction: http://ged.msu.edu/angus/diginorm-2012/tutorial.html
3. velvet for de novo assembly: http://www.ebi.ac.uk/~zerbino/velvet/
4. AMOS for reference guided schaffolding: http://sourceforge.net/apps/mediawiki/amos/index.php?title=AMOS
5. Quast for assembly quality assessment: http://bioinf.spbau.ru/quast
6. MUMmer for genome comparison and variation discovery: http://mummer.sourceforge.net/
7. Circos for visualization: http://circos.ca/

**For running the whole assembling pipeline at once on command line, run quick_assemble.py:**:

    python quick_assemble.py -l read_1.fq -e read_2.fq -r refseq.fa -d out_dir

**For VIRAmp platform installation and usage:**

.. toctree::
	:maxdepth: 2

	ec2_import
	viramp_login
	viramp_intro

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

