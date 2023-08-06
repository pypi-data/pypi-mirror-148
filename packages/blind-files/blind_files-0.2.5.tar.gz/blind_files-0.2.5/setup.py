# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blind_files']

package_data = \
{'': ['*'], 'blind_files': ['data/*']}

install_requires = \
['click>=8.1.2,<9.0.0', 'pyahocorasick>=1.4.4,<2.0.0']

entry_points = \
{'console_scripts': ['blind-files = blind_files.cli:main']}

setup_kwargs = {
    'name': 'blind-files',
    'version': '0.2.5',
    'description': 'Relabel files in order to work on them blind',
    'long_description': 'Blind files\n===========\n\nGenerates a mapping from file names to blind but memorable file names.  This\nscript assumes that you have a directory that contains files and / or\nsubdirectories with samples from an experiment.  The names of these files and\ndirectories reveal which group the samples belong to, but the contents of the\nfiles do not.\n\nThe script will move these files to a new directory, renaming them so that the\nnew file names do not reveal which group the samples belong to.  It will also\ngenerate a mapping file to indicate how the new files map to the original\nfiles.\n\nInstalling\n----------\n\nRun `pip3 install blind_files`.\n\nRunning\n-------\n\nThis script takes an input dir, and generates a directory containing a script,\n`blind.sh`, that can be used to blind the files in the input dir.  It also\ngenerates a mapping csv, `mapping.csv`, that can be used after the user has\ndone the analysis to see how the original names map to blinded names.\n\nThe script has two modes of operation:\n\n### Using a delimiter\nIn the first mode of operation, you can specify a delimiter to use such that\nall the text before the delimiter in each file name will be replaced.  For\nexample:\n\n```sh\nblind_files \\\n   --mode delimiter \\\n   --delimiter _foo \\\n   --input-dir input_dir \\\n   --output-dir output_dir \\\n   --mapping-dir mapping_dir\n```\n\nIn this case, if `input_dir` contains the following files:\n\n```\nsample_1_foo.txt\nsample_1_foo-bar.csv\nsample_2_foo.txt\nhello.txt\n```\n\nThen after running `mapping_dir/blind.sh`, `output_dir` will contain\n\n```\ngolf_elbow_foo.txt\ngolf_elbow_foo-bar.csv\nco-producer_reputation_foo.txt\nhello.txt\n```\n\nIn `mapping_dir` you will also find a file `mapping.csv` with the contents:\n\n```\noriginal,blinded\nsample_1,golf_elbow\nsample_2,co-producer_reputation\n```\n\n#### Limitations\nThis will only replace names at the top level of the input directory.  If you\nhave a more complex nested directory structure, where the identifer names may\nbe buried in the directory tree, use identifier list approach described below.\n\n### Using a list of identifiers\nIn the second mode of operation, you can specify list of identifiers that\nshould be blinded whenever they are encountered in the input directory tree.\nFor example, if `identifiers.txt` contains the following:\n\n```\ngroup_a_1\ngroup_b_1\n```\n\nthen running\n\n```sh\nblind_files \\\n   --mode identifiers \\\n   --identifiers identifiers.txt \\\n   --input-dir input_dir \\\n   --output-dir output_dir \\\n   --mapping-dir mapping_dir\n```\n\nIn this case, if `input_dir` contains the following files:\n\n```\ngroup_a_1/group_a_1/foo.txt\ngroup_b_1/group_b_1/foo.txt\nhello.txt\n```\n\nThen after running `mapping_dir/blind.sh`, `output_dir` will contain\n\n```\nhead_bottle/head_bottle/foo.txt\neponym_curtain/eponym_curtain/foo.txt\nhello.txt\n```\n\nIn `mapping_dir` you will also find a file `mapping.csv` with the contents:\n\n```\noriginal,blinded\ngroup_a_1,head_bottle\ngroup_b_1,eponym_curtain\n```\n\n#### Limitations\nNo identifier can be a substring of any other identifier.  For example, it is\nnot allowed to have identifiers `sample_1` and `sample_11`.  However,\n`sample_01` and `sample_11` would be fine.\n\nGeneral limitations\n-------------------\n- This script should work on any platform, but has only been tested on Mac OS.\n- This script should handle symlinks by simply moving the symlink, without\n  following it, but this behavior has not been tested.\n\nCredits\n-------\nThis package was created with\n[Cookiecutter](https://github.com/audreyr/cookiecutter-pypackage).\n\nnounlist from [here](http://www.desiquintans.com/downloads/nounlist/nounlist.txt).\n',
    'author': 'Pokey Rule',
    'author_email': '755842+pokey@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
