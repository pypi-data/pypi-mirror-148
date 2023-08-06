# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['nii_info']
install_requires = \
['nibabel>=3.0.0,<4.0.0']

entry_points = \
{'console_scripts': ['nii = nii_info:cli']}

setup_kwargs = {
    'name': 'nii-info',
    'version': '1.0.0',
    'description': 'Display NIfTI image information in a tabular format',
    'long_description': '# nii-info\n\nDisplay NIfTI image information in a tabular format\n\n[![PyPI Version](https://img.shields.io/pypi/v/nii-info.svg)](https://pypi.org/project/nii-info/)\n\n## Installation\n\n```bash\npip install nii-info\n```\n\n## Motivation\n\nThis package attempts to provide a quick and easy way to get a high-level overview of a collection of NIfTI images.\n\nOften when dealing with a collection of NIfTI images the metadata describing those images is embeded across multiple files, specifically the nii images themselves, as well as potential JOSN sidecar files.\n\nOf course, one can crack open a NIfTI file to inspect the header, or load a JSON sidecar into an editor to view its contents. However this quickly becomes tedious when one is dealing with many files and many fields of interest.\n\n`nii-info` collects the values of fields of interest across a set of NIfTI files and aggregates them in a tablular format.\n\n## Usage\n\n`nii-info` exposes a CLI: `nii`\n\n```text\n$ nii --help\nusage: nii [-h] [-o OUT_TSV] [-f FIELDS] [-v] [-D]\n           path [path ...]\n\nDisplay NIfTI image information in a tabular format\n\n...\n\npositional arguments:\n  path                  nifti files or directories\n                        containing nifti files,\n                        directories are searched\n                        recursively\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -o OUT_TSV, --out-tsv OUT_TSV\n                        file to write info to. (default:\n                        stdout)\n  -f FIELDS, --fields FIELDS\n                        Fields to include in the table.\n  -v, --version         show program\'s version number and\n                        exit\n  -D, --debug           run program in debug mode\n```\n\nThe `nii` CLI accepts a list of files and/or directories. Directories are searched recursively for `*.nii` and `*.nii.gz` files.\n\nSimple usage might look something like:\n\n```bash\nnii /path/to/nii/file1.nii.gz /path/to/nii/file2.nii.gz /path/to/nii/dir/\n```\n\n## Modifying Fields/Columns\n\nThis application enables the user to modify which JSON sidecar & NIfTI header fields are included in the generated output via the `-f`/`--fields` option.\n\nThe `-f` option can be passed multiple times and uses a special syntax.\n\nThe argument for the `-f` option should be string of comma-separated values, where each value contains the "location", sidecar or nii header "key", and optional "label".\n\nFor example, to add the `FlipAngle` and `InversionTime` fields from the sidecars as well as the `datatype` and `descrip` fields from the NIfTI headers to the default set of outputs, the command could look something like:\n\n```bash\nnii \\\n    -f \'sidecar:FlipAngle,sidecar:InversionTime\' \\\n    -f \'header:datatype,header:descrip:Header Description\' \\\n    /path/to/nii/dir/\n```\n\nIn the above example, `sidecar:FlipAngle` tells the application to extract the `FlipAngle` field from each image\'s sidecar.\n\nAdditionally, `header:descrip:Header Description` tells the application to extract the `descrip` field from each image\'s NIfTI header and use the label `Header Descrption` as the column heading.\n\n## Contributing\n\n1. Have or install a recent version of `poetry` (version >= 1.1)\n1. Fork the repo\n1. Setup a virtual environment (however you prefer)\n1. Run `poetry install`\n1. Run `pre-commit install`\n1. Add your changes (adding/updating tests is always nice too)\n1. Commit your changes + push to your fork\n1. Open a PR\n',
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrewrosss/nii-info',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
