# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipeclip', 'pipeclip.lib']

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
    'version': '2.0.1',
    'description': 'PIPELINE FOR CLIP SEQ DATA',
    'long_description': '# PIPE-CLIP\n\nPipeline for CLIP-seq Analysis.\nThis is a fork version (2.0.0) of [PIPE-CLIP](https://github.com/QBRC/PIPE-CLIP).\n\n## Requirement:\n\n- Python >=3.6;\n- R >=3.0\n- Perl >=5.0\n- Python packages: `pysam`, `pybedtools` and `ghmm`;\n- R packages: `MASS`, `VGAM` and their dependencies.\n- Other packages: `HOMER` (annotatePeaks.pl) and annotation files\n  - Make sure HOMER are in your PATH. You can test this by type "annotatePeaks.pl" from anywhere and you should get help information of this command.\n\n## How to use:\n\n- After unzip the package, you cd into the program folder and run PIPE-CLIP by typing:\n\n```bash\npython pipeclip.py -i input.bam -o output_prefix -c CLIP_type -l minimum_matchlength -m maximum_mismatchcount  -r Remove_PCR_duplicate -M FDR_for_mutations -C FDR_for_clusters -s species\n```\n\n- `-i` input BAM\n- `-o` output prefix\n- `-c` CLIP type,[0,1,2,3] (0)HITS-CLIP; (1)PAR-4SU; (2)PAR-6SG; (3)iCLIP\n- `-l` minimum match length\n- `-m` maximum mismatch count\n- `-r` method to remove PCR duplicate,[0,1,2] (0)No removal; (1)Remove by read start; (2)Remove by sequence\n- `-M` FDR to get significant mutations\n- `-C` FDR to get enriched clusters\n- `-s` species. (species might be hg19, mm10, mm9.)\n\n## Footnote\n\n- Contact: Zhiqun.Xie@UTSouthwestern.edu\n- Publication: http://genomebiology.com/2014/15/1/R18\n- Google Code site: https://code.google.com/p/pipe-clip/\n',
    'author': 'Chang Ye',
    'author_email': 'yech1990@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
