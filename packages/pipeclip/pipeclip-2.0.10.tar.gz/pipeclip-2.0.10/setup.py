# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipeclip']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'pybedtools>=0.9.0,<0.10.0',
 'pysam>=0.19.0,<0.20.0',
 'rpy2>=3.5.1,<4.0.0']

entry_points = \
{'console_scripts': ['pipeclip = pipeclip.main:runPipeClip']}

setup_kwargs = {
    'name': 'pipeclip',
    'version': '2.0.10',
    'description': 'PIPELINE FOR CLIP SEQ DATA',
    'long_description': '# PIPE-CLIP\n\n[![Pypi Releases](https://img.shields.io/pypi/v/pipeclip.svg)](https://pypi.python.org/pypi/pipeclip)\n[![Downloads](https://pepy.tech/badge/pipeclip)](https://pepy.tech/project/pipeclip)\n\nPipeline for CLIP-seq Analysis.\nThis is a fork version (2.0.x) of [PIPE-CLIP](https://github.com/QBRC/PIPE-CLIP).\n\n## Requirement:\n\n- Python >=3.6;\n- Python packages: `pysam`, `pybedtools` and `rpy2`. (Python packages will be installed automaticallly)\n\n- R >=3.0;\n- R packages: `MASS`, `VGAM` and their dependencies. (R packages will be installed automatically)\n\n- Perl >=5.0\n- Other packages: `HOMER` (annotatePeaks.pl) and annotation files\n  - Make sure HOMER are in your PATH. You can test this by type "annotatePeaks.pl" from anywhere and you should get help information of this command.\n\n## How to install:\n\n```bash\npip install pipeclip\n```\n\n## How to use:\n\n```bash\npipeclip -i input.bam -o output_prefix -c CLIP_type -l minimum_matchlength -m maximum_mismatchcount -r Remove_PCR_duplicate -M FDR_for_mutations -C FDR_for_clusters -s species\n```\n\n- `-i` input BAM\n- `-t` control BAM\n- `-o` output prefix\n- `-c` CLIP type,[0,1,2,3] (0)HITS-CLIP; (1)PAR-4SU; (2)PAR-6SG; (3)iCLIP\n- `-r` method to remove PCR duplicate,[0,1,2] (0)No removal; (1)Remove by read start; (2)Remove by sequence\n- `-l` minimum match length\n- `-m` maximum mismatch count\n- `-M` FDR to get significant mutations\n- `-C` FDR to get enriched clusters\n- `-s` species. (species might be hg19, mm10, mm9.) Leave blank to skip annotation step.\n\n## Footnote\n\n> Cite:\n>\n> - Chen, B., Yun, J., Kim, M.S. et al. PIPE-CLIP: a comprehensive online tool for CLIP-seq data analysis. Genome Biol 15, R18 (2014). https://doi.org/10.1186/gb-2014-15-1-r18\n',
    'author': 'Chang Ye',
    'author_email': 'yech1990@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/y9c/PIPE-CLIP',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
