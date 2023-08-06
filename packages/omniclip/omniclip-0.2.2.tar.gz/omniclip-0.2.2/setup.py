# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omniCLIP', 'omniCLIP.data_parsing', 'omniCLIP.omni_stat']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.28,<0.30.0',
 'biopython>=1.79,<2.0',
 'gffutils>=0.10.1,<0.11.0',
 'h5py>=3.6.0,<4.0.0',
 'intervaltree>=3.1.0,<4.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pysam>=0.19.0,<0.20.0',
 'scipy>=1.8.0,<2.0.0',
 'sklearn>=0.0,<0.1',
 'statsmodels>=0.13.2,<0.14.0']

entry_points = \
{'console_scripts': ['omniCLIP = omniCLIP.omniCLIP:main']}

setup_kwargs = {
    'name': 'omniclip',
    'version': '0.2.2',
    'description': '',
    'long_description': '# omniCLIP\nomniCLIP is a Bayesian peak caller that can be applied to data from CLIP-Seq experiments to detect regulatory elements in RNAs.\n\n## Overview\n\n[Introduction](#introduction)\n\n[Dependencies](#dependencies)\n\n[Installation](#installation)\n\n[Usage](#usage)\n\n[Contributors](#contributors)\n\n[License](#license)\n\n\n## Introduction\nomniCLIP can call peaks for CLIP-Seq data data while accounting for confounding factors such as the gene expression and it automatically learns relevant diagnostic events from the data. Furtermore, it can leverage replicate information and model technical and biological variance.\n\n## Dependencies and Requirements\nomniCLIP requires Python (v.3.7) and the libraries described in the `environment.yml` file. All required dependencies can be installed using *conda* by executing the following in the main project directory :\n```\n$ conda env create -f environment.yml\n```\n\nThe environment then needs to be activated in order to run omniCLIP :\n```\n$ conda activate omniEnv\n```\n\n## Installation\n\n### Manual installation\nThe latest stable release in the ***master*** branch can be downloaded by executing:\n```\n$ git clone -b master https://github.com/simojoe/omniCLIP.git\n```\nAfter this the following command has to be executed:\n```\n$ python3 setup.py\n```\nThis compiles the Cython code for the viterbi algorithm.\n\n## Usage\nAn omniCLIP analysis is run into four different steps :\n- Generating the annotation database\n- Parsing the background RNA-seq files\n- Parsing the CLIP files\n- Running the omniCLIP algorithm\n\nThe following is an example of the commands. The commands in this example only show the **required** arguments for the analysis. The following files are necessary to run an analysis.\n\nFile name  | Description\n------------- | -------------\n$GFF_file | Genome annotation file\n$GENOME_dir | Directory containing FASTA files with each of the chromosomes sequence\n$BG_file[1,2,...] | BAM files for the background library. The alignments need to have the MD and NM tags.\n$CLIP_file[1,2,...] | BAM files for the CLIP library. The alignments need to have the MD and NM tags.\n\nThe following files will be created.\n\nFile name  | Description\n------------- | -------------\n$DB_file | SQL database of the genome annotation.\n$BG_dat | H5PY file of the parsed background library.\n$CLIP_dat | H5PY file of the parsed CLIP library.\n$OUT_dir | Directory containing the final results\n\n\n### 1. Generating the annotation database\n```\n$ python3 omniCLIP.py generateDB \\\n--gff-file $GFF_file --db-file $DB_file\n```\n\n### 2. Parsing the background RNA-seq files\n```\n$ python3 omniCLIP.py parsingBG \\\n--db-file $DB_file --genome-dir $GENOME_dir \\\n--bg-files $BG_file1 --bg-files $BG_file2 \\\n--out-file $BG_dat\n```\n\n### 3. Parsing the CLIP files\n```\n$ python3 omniCLIP.py parsingCLIP \\\n--db-file $DB_file --genome-dir $GENOME_dir \\\n--clip-files $CLIP_file1 --clip-files $CLIP_file2 \\\n--out-file $CLIP_dat\n```\n\n\n### 4. Running the omniCLIP algorithm\n```\n$ python3 omniCLIP.py run_omniCLIP \\\n--db-file $DB_file --bg-dat $BG_dat --clip-dat $CLIP_dat \\\n--out-dir $OUT_dir\n```\n\n### Optional arguments\nFor the full list of optional arguments of the different step, consult the help of the commands using :\n```\n$ python3 omniCLIP.py parsingBG --help\n```\n\n## Contributors\n\n\n\n## License\nGNU GPL license (v3)\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
