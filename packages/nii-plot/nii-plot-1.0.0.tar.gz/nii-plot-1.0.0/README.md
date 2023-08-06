# nii-plot

Plot mean NIfTI timeseries

[![PyPI Version](https://img.shields.io/pypi/v/nii-plot.svg)](https://pypi.org/project/nii-plot/)

## Installation

```bash
pip install nii-plot
```

## Motivation

When dealing with volumetric timeseries data it can be useful to view a high-level aggregate view of the timeseries.

This package provides a way to easily visualize 4D NIfTI images by plotting the volume-wise mean timeseries.

For example, a command like:

```bash
nii-plot -i '1:' -t 'Multi-delay PCASL' /path/to/nii/file.nii.gz
```

might yield something like:

![Line plot example](https://raw.githubusercontent.com/andrewrosss/nii-plot/main/assets/example-line.png "Line plot example")

## Usage

`nii-plot` exposes a CLI: `nii-plot`

```text
$ nii-plot --help
usage: nii-plot [-h] [-p PERCENTILE | -m MASK] [-i INDEX_SPEC]
                [-s | -q | -l] [-t TITLE] [-x X_LABEL] [-y Y_LABEL]
                [-v] [-D]
                path

positional arguments:
  path                  The NIfTI file

optional arguments:
  -h, --help            show this help message and exit
  -p PERCENTILE, --percentile PERCENTILE
                        Percentile to use to threshold the data.
                        Value in the image above that percentile
                        will be used in computing the volume-wise
                        means. (default: 50.0)
  -m MASK, --mask MASK  Mask NIfTI image. Only non-zero voxels in
                        this image are included in the mean
                        computation. Must be the same (spatial)
                        shape as the input file.
  -i INDEX_SPEC, --index-spec INDEX_SPEC
                        Volume indicies to include in the plot. Can
                        use numpy-like slicing (start:stop[:step]),
                        for example, to plot the first volume, then
                        the 10th and 11th volumes, then from the
                        16th to the end, we could write:
                        '0,9:11,15:'. (default: '::')
  -s, --scatter         Plot the mean time series as a scatter plot
  -q, --paired-scatter  Plot a paired scatter plot (useful for ASL
                        data)
  -l, --line            Plot the mean time series as a line chart
  -t TITLE, --title TITLE
                        Plot title
  -x X_LABEL, --x-label X_LABEL
                        X-axis label
  -y Y_LABEL, --y-label Y_LABEL
                        Y-axis label
  -v, --version         show program's version number and exit
  -D, --debug           run program in debug mode
```

## Supplying a mask

By default, `nii-plot` will threshold the input image, **excluding** from the mean computation **all voxels with values falling below the 50th percentile**.

This choice of percentile value at which to threshold may not be desirable, hence the value can be changed via the `-p`/`--percentile` option. The argument to this option should be an int or float between `0` and `100`. To effectively "turn off" thresholding you can specify: `--percentile=0`.

If you would prefer that the mean computation happen only across voxels in a specific mask, then you can use the `-m`/`--mask` option (mutually exclusive to `-p`/`--percentile`). In this case the volume-wise mean computation will **only include voxels which correspond to voxels in the mask image whose value is greater than 0.**

## Selecting which volumes to plot

You can choose which volumes are plotted by `nii-plot` by supplying an **_index spec_**.

An index spec is a comma-separated list of strings where each entry in the list is either an integer (i.e. a volume index) or a numpy-style slice expression (`start:stop[:step]`).

For example, to plot the 1st volume, the 10th and 11th volumes, and the 16th volume to the end of the timeseries, we could write: `0,9:11,15:`, i.e. this is a comma-separated list of 3 values: `0`, `9:11`, and `15:`. `0` means include the `0th` volume, `9:11` means include all volumes from index `9` (inclusive) to index `11` (exclusive), `15:` means include all volumes from index `15` (inclusive) to the end of the timeseries.

> IMPORTANT: volume indexing is **_0-based_**

## Plot type

By default, `nii-plot` will produce a line plot (as shown above). You can change to a scatter plot using the `-s`/`--scatter` flag.

There is another plot type which is useful when visualizing ASL data, which is the **_paired-scatter_** plot (`-q`/`--paired-scatter`), which looks like:

![Paired-scatter plot example](https://raw.githubusercontent.com/andrewrosss/nii-plot/main/assets/example-paired-scatter.png "Paired-scatter plot example")

## Contributing

1. Have or install a recent version of `poetry` (version >= 1.1)
1. Fork the repo
1. Setup a virtual environment (however you prefer)
1. Run `poetry install`
1. Run `pre-commit install`
1. Add your changes (adding/updating tests is always nice too)
1. Commit your changes + push to your fork
1. Open a PR
