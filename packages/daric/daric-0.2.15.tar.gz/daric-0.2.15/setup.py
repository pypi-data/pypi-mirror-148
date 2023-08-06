# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daric', 'daric.data', 'daric.lib']

package_data = \
{'': ['*']}

install_requires = \
['HTSeq>=0.12.4,<0.13.0',
 'hmmlearn>=0.2.6,<0.3.0',
 'matplotlib==3.3.4',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pyBigWig>=0.3.18,<0.4.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.6.2,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['daric = daric.main:app']}

setup_kwargs = {
    'name': 'daric',
    'version': '0.2.15',
    'description': 'DARIC, a computational framework to find quantitatively differential compartments from Hi-C data',
    'long_description': '<div align="center">\n\n  <img src="img/daric_logo.png" alt="logo" width="300" height="auto" />\n  <h1></h1>\n  <p>\n    A computational framework to find <span style="color:red"> ***quantitatively***</span> differential compartments between Hi-C datasets\n  </p>\n\n[![Downloads](https://pepy.tech/badge/daric)](https://pepy.tech/project/daric)\n[![version](https://img.shields.io/badge/daric-v0.2.11-brightgreen)](https://img.shields.io/badge/daric-v0.2.11-brightgreen)\n\n<div align="left">\n\n`DARIC`, or Differential Analysis for genomic Regions\' Interaction with Compartments, is a computational framework to identify the quantitatively differential compartments from Hi-C-like data. For more details about the design and implementation of the framework, please check our preprint here.\n\n#Installation\n1. Install with `pip`.\n\t+ `$ pip install daric`\n\t+ To test the installation, please type `$ daric --help` in shell to see if help messages pop out.\n2. Download the `daric` package from github and install locally.\n\n# Usage\n`DARIC` is composed of three commands: `calculate`, `normalize`, and `runhmm`. \n\n## 1. Calculation of PIS\n---\nPIS, or Preferential Interaction Score, is a metric that we used to evaluate the relative interaction strength between the A and B compartments. `calculate` is the command to calculate the PIS:\n\n\n\n```\nUsage: daric calculate [OPTIONS]\n\nOptions:\n  -n, --name TEXT     sample names used for output  [required]\n  -p, --pc1 TEXT      the PC1 bigwig file for compartments  [required]\n  -m, --hic TEXT      the directory with the o/e interaction matrice in sparse format. Note that it has to be the output from juicer dump.  [required]\n  -r, --reso INTEGER  the genomic resolution (in bp) for compartment bins and hic file  [required]\n  -s, --species TEXT  species (mm9, mm10, hg19, hg38)  [required]\n  -o, --outdir TEXT   path for output directory  [default: ./]\n  --help              Show this message and exit.\n```\n## 2. Normalization of two PIS tracks\n---\nWe borrowed the idea of MAnorm, a normalization method designed for normalizing ChIP-seq datasets, to normalize the PIS data. `normalize` is the command for this task:\n\n```\nUsage: daric normalize [OPTIONS]\n\nOptions:\n  -m, --sample1 TEXT      name of sample1, e.g. name of the cell-type\n                          [required]\n\n  -n, --sample2 TEXT      name of sample2  [required]\n  -p, --sample1_PIS TEXT  the PIS track(s) for sample1. Multiple files, like\n                          replicates, can be separated by comma without space.\n                          [required]\n  -q, --sample2_PIS TEXT  the PIS track(s) for sample2. Multiple files, like\n                          replicates, can be separated by comma without space.\n                          [required]\n  -f, --fraction FLOAT    A value between 0 and 1. Genomic regions whose\n                          residual PIS locate in the top and bottom XX\n                          fraction are excluded in building the MAnorm model\n                          to infer the systematic scaling differences between\n                          the two samples.  [default: 0.15]\n\n  -r, --reso INTEGER      an integer representing the genomic resolution for\n                          compartment bins in the PIS track, in bp  [required]\n\n  -s, --species TEXT      species (mm9, mm10, hg19, hg38)  [required]\n  -o, --outdir TEXT       output directory  [default: ./]\n  --help                  Show this message and exit.\n```\n\n## 3. Identification of differential comparments\n`runhmm` is the command to identify the quantitatively differential compartments and perform statistical analyses. \n\n```\nUsage: daric runhmm [OPTIONS]\n\nOptions:\n  -f, --deltaPIS TEXT  the delta scores for different comparisons. Multiple\n                       files should be separated by comma  [required]\n\n  -r, --reso INTEGER   an integer representing the genomic resolution for\n                       compartment bins in the PIS track, in bp  [required]\n\n  -s, --species TEXT   species (mm9, mm10, hg19, hg38)  [required]\n  -o, --outdir TEXT    output directory  [default: ./]\n  --help               Show this message and exit.\n\n```\n',
    'author': 'Yan Kai',
    'author_email': 'smilekai@gwmail.gwu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
