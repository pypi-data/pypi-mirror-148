<div align="center">

  <img src="img/daric_logo.png" alt="logo" width="300" height="auto" />
  <h1></h1>
  <p>
    A computational framework to find <span style="color:red"> ***quantitatively***</span> differential compartments between Hi-C datasets
  </p>

[![Downloads](https://pepy.tech/badge/daric)](https://pepy.tech/project/daric)
[![version](https://img.shields.io/badge/daric-v0.2.11-brightgreen)](https://img.shields.io/badge/daric-v0.2.11-brightgreen)

<div align="left">

`DARIC`, or Differential Analysis for genomic Regions' Interaction with Compartments, is a computational framework to identify the quantitatively differential compartments from Hi-C-like data. For more details about the design and implementation of the framework, please check our preprint here.

#Installation
1. Install with `pip`.
	+ `$ pip install daric`
	+ To test the installation, please type `$ daric --help` in shell to see if help messages pop out.
2. Download the `daric` package from github and install locally.

# Usage
`DARIC` is composed of three commands: `calculate`, `normalize`, and `runhmm`. 

## 1. Calculation of PIS
---
PIS, or Preferential Interaction Score, is a metric that we used to evaluate the relative interaction strength between the A and B compartments. `calculate` is the command to calculate the PIS:



```
Usage: daric calculate [OPTIONS]

Options:
  -n, --name TEXT     sample names used for output  [required]
  -p, --pc1 TEXT      the PC1 bigwig file for compartments  [required]
  -m, --hic TEXT      the directory with the o/e interaction matrice in sparse format. Note that it has to be the output from juicer dump.  [required]
  -r, --reso INTEGER  the genomic resolution (in bp) for compartment bins and hic file  [required]
  -s, --species TEXT  species (mm9, mm10, hg19, hg38)  [required]
  -o, --outdir TEXT   path for output directory  [default: ./]
  --help              Show this message and exit.
```
## 2. Normalization of two PIS tracks
---
We borrowed the idea of MAnorm, a normalization method designed for normalizing ChIP-seq datasets, to normalize the PIS data. `normalize` is the command for this task:

```
Usage: daric normalize [OPTIONS]

Options:
  -m, --sample1 TEXT      name of sample1, e.g. name of the cell-type
                          [required]

  -n, --sample2 TEXT      name of sample2  [required]
  -p, --sample1_PIS TEXT  the PIS track(s) for sample1. Multiple files, like
                          replicates, can be separated by comma without space.
                          [required]
  -q, --sample2_PIS TEXT  the PIS track(s) for sample2. Multiple files, like
                          replicates, can be separated by comma without space.
                          [required]
  -f, --fraction FLOAT    A value between 0 and 1. Genomic regions whose
                          residual PIS locate in the top and bottom XX
                          fraction are excluded in building the MAnorm model
                          to infer the systematic scaling differences between
                          the two samples.  [default: 0.15]

  -r, --reso INTEGER      an integer representing the genomic resolution for
                          compartment bins in the PIS track, in bp  [required]

  -s, --species TEXT      species (mm9, mm10, hg19, hg38)  [required]
  -o, --outdir TEXT       output directory  [default: ./]
  --help                  Show this message and exit.
```

## 3. Identification of differential comparments
`runhmm` is the command to identify the quantitatively differential compartments and perform statistical analyses. 

```
Usage: daric runhmm [OPTIONS]

Options:
  -f, --deltaPIS TEXT  the delta scores for different comparisons. Multiple
                       files should be separated by comma  [required]

  -r, --reso INTEGER   an integer representing the genomic resolution for
                       compartment bins in the PIS track, in bp  [required]

  -s, --species TEXT   species (mm9, mm10, hg19, hg38)  [required]
  -o, --outdir TEXT    output directory  [default: ./]
  --help               Show this message and exit.

```
