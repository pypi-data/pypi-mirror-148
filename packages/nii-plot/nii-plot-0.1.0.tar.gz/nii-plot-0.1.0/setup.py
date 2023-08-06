# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['nii_plot']
install_requires = \
['matplotlib>=3.0.0,<4.0.0', 'nibabel>=3.0.0,<4.0.0']

entry_points = \
{'console_scripts': ['nii-plot = nii_plot:cli']}

setup_kwargs = {
    'name': 'nii-plot',
    'version': '0.1.0',
    'description': 'Plot mean NIfTI timeseries',
    'long_description': '# nii-plot\n\nPlot mean NIfTI timeseries\n\n[![PyPI Version](https://img.shields.io/pypi/v/nii-plot.svg)](https://pypi.org/project/nii-plot/)\n\n## Installation\n\n```bash\npip install nii-plot\n```\n\n## Motivation\n\nWhen dealing with volumetric timeseries data it can be useful to view a high-level aggregate view of the timeseries.\n\nThis package provides a way to easily visualize 4D NIfTI images by plotting the volume-wise mean timeseries.\n\nFor example, a command like:\n\n```bash\nnii-plot -l -i \'1:\' -t \'Multi-delay PCASL\' /path/to/nii/file.nii.gz\n```\n\nmight yield something like:\n\n![Line plot example](https://raw.githubusercontent.com/andrewrosss/nii-plot/main/assets/example-line.png "Line plot example")\n\n## Usage\n\n`nii-plot` exposes a CLI: `nii-plot`\n\n```text\n$ nii-plot --help\nusage: nii-plot [-h] [-p PERCENTILE | -m MASK] [-i INDEX_SPEC]\n                [-s | -q | -l] [-t TITLE] [-x X_LABEL] [-y Y_LABEL]\n                [-v] [-D]\n                path\n\npositional arguments:\n  path                  The NIfTI file\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p PERCENTILE, --percentile PERCENTILE\n                        Percentile to use to threshold the data.\n                        Value in the image above that percentile\n                        will be used in computing the volume-wise\n                        means. (default: 50.0)\n  -m MASK, --mask MASK  Mask NIfTI image. Only non-zero voxels in\n                        this image are included in the mean\n                        computation. Must be the same (spatial)\n                        shape as the input file.\n  -i INDEX_SPEC, --index-spec INDEX_SPEC\n                        Volume indicies to include in the plot. Can\n                        use numpy-like slicing (start:stop[:step]),\n                        for example, to plot the first volume, then\n                        the 10th and 11th volumes, then from the\n                        16th to the end, we could write:\n                        \'0,9:11,15:\'. (default: \'::\')\n  -s, --scatter         Plot the mean time series as a scatter plot\n  -q, --paired-scatter  Plot a paired scatter plot (useful for ASL\n                        data)\n  -l, --line            Plot the mean time series as a line chart\n  -t TITLE, --title TITLE\n                        Plot title\n  -x X_LABEL, --x-label X_LABEL\n                        X-axis label\n  -y Y_LABEL, --y-label Y_LABEL\n                        Y-axis label\n  -v, --version         show program\'s version number and exit\n  -D, --debug           run program in debug mode\n```\n\n## Supplying a mask\n\nBy default, `nii-plot` will threshold the input image, **excluding** from the mean computation **all voxels with values falling below the 50th percentile**.\n\nThis choice of percentile value at which to threshold may not be desirable, hence the value can be changed via the `-p`/`--percentile` option. The argument to this option should be an int or float between `0` and `100`. To effectively "turn off" thresholding you can specify: `--percentile=0`.\n\nIf you would prefer that the mean computation happen only across voxels in a specific mask, then you can use the `-m`/`--mask` option (mutually exclusive to `-p`/`--percentile`). In this case the volume-wise mean computation will **only include voxels which correspond to voxels in the mask image whose value is greater than 0.**\n\n## Selecting which volumes to plot\n\nYou can choose which volumes are plotted by `nii-plot` by supplying an **_index spec_**.\n\nAn index spec is a comma-separated list of strings where each entry in the list is either an integer (i.e. a volume index) or a numpy-style slice expression (`start:stop[:step]`).\n\nFor example, to plot the 1st volume, the 10th and 11th volumes, and the 16th volume to the end of the timeseries, we could write: `0,9:11,15:`, i.e. this is a comma-separated list of 3 values: `0`, `9:11`, and `15:`. `0` means include the `0th` volume, `9:11` means include all volumes from index `9` (inclusive) to index `11` (exclusive), `15:` means include all volumes from index `15` (inclusive) to the end of the timeseries.\n\n> IMPORTANT: volume indexing is **_0-based_**\n\n## Plot type\n\nBy default, `nii-plot` will produce a line plot (as shown above). You can change to a scatter plot using the `-s`/`--scatter` flag.\n\nThere is another plot type which is useful when visualizing ASL data, which is the **_paired-scatter_** plot (`-q`/`--paired-scatter`), which looks like:\n\n![Paired-scatter plot example](https://raw.githubusercontent.com/andrewrosss/nii-plot/main/assets/example-paired-scatter.png "Paired-scatter plot example")\n\n## Contributing\n\n1. Have or install a recent version of `poetry` (version >= 1.1)\n1. Fork the repo\n1. Setup a virtual environment (however you prefer)\n1. Run `poetry install`\n1. Run `pre-commit install`\n1. Add your changes (adding/updating tests is always nice too)\n1. Commit your changes + push to your fork\n1. Open a PR\n',
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrewrosss/nii-plot',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
