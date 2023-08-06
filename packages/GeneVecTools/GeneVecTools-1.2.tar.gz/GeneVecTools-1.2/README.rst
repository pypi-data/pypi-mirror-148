

GeneVecTools
===============
Reading in Variety of Genetic File Types

Vector Embedding Algorithms

Byte Array Encoders

Clustering and Preprocessing Steps for Compression

Similarity Search Tools for FASTA/FASTQ files

Installing

Tester files: https://drive.google.com/drive/folders/1MGkz1QyjGcEF8q8RDWTZXR7Z2k0K1VLC?usp=sharing
============

.. code-block:: bash

    pip install GeneVecTools

Usage
=====

.. code-block:: bash

    >>> from GeneVecTools import SimSearch
    >>> dir = "/Users/danielum/Documents/MSCS/Spring_2022/COMS_E6901/VG/VG/sample/fastq/small_cDNA_Sequences_pbmc_1k_v2_S1_L002_R2_001.fastq"
    >>> VECSS = SimSearch.VecSS(dir)
    >>> sequences = VECSS.readq()
    >>> print(VECSS.unembed(VECSS.embed(VECSS.s)) == VECSS.s)
   'True'
