from __future__ import annotations

import argparse
import re
from enum import Enum
from pathlib import Path
from typing import Iterable
from typing import Iterator
from typing import NamedTuple
from typing import NoReturn
from typing import Sequence
from typing import TypeVar

import nibabel as nib
import numpy as np
from matplotlib import pyplot as plt


__version__ = "0.1.0"


class PlotType(Enum):
    LINE = "line"
    SCATTER = "scatter"
    PAIRED_SCATTER = "paired_scatter"


class Defaults:
    plot_type = PlotType.LINE
    percentile = 50.0
    index_spec = "::"
    title = None
    x_label = "Volume Index"
    y_label = None
    debug = False


def cli(args: Sequence[str] | None = None) -> NoReturn:
    raise SystemExit(main(args))


def main(args: Sequence[str] | None = None) -> int | str:
    parser = create_parser()
    ns = parser.parse_args(args)
    debug: bool = ns.debug

    try:
        return ns.handler(ns)
    except Exception as e:
        if debug:
            raise
        else:
            return str(e)


def create_parser(
    parser: argparse.ArgumentParser | None = None,
) -> argparse.ArgumentParser:
    parser = parser or argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The NIfTI file")
    mask_group = parser.add_mutually_exclusive_group()
    mask_group.add_argument(
        "-p",
        "--percentile",
        type=float,
        default=Defaults.percentile,
        help="Percentile to use to threshold the data. Value in the image "
        "above that percentile will be used in computing the volume-wise "
        "means. (default: %(default)s)",
    )
    mask_group.add_argument(
        "-m",
        "--mask",
        type=Path,
        help="Mask NIfTI image. Only non-zero voxels in this image are "
        "included in the mean computation. Must be the same (spatial) shape "
        "as the input file.",
    )
    parser.add_argument(
        "-i",
        "--index-spec",
        type=str,
        default=Defaults.index_spec,
        help="Volume indicies to include in the plot. Can use numpy-like "
        "slicing (start:stop[:step]), for example, to plot the first "
        "volume, then the 10th and 11th volumes, then from the 16th to "
        "the end, we could write: '0,9:11,15:'. (default: %(default)r)",
    )
    plot_type_group = parser.add_mutually_exclusive_group()
    plot_type_group.add_argument(
        "-s",
        "--scatter",
        default=Defaults.plot_type,
        dest="plot_type",
        action="store_const",
        const=PlotType.SCATTER,
        help="Plot the mean time series as a scatter plot",
    )
    plot_type_group.add_argument(
        "-q",
        "--paired-scatter",
        dest="plot_type",
        action="store_const",
        const=PlotType.PAIRED_SCATTER,
        help="Plot a paired scatter plot (useful for ASL data)",
    )
    plot_type_group.add_argument(
        "-l",
        "--line",
        dest="plot_type",
        action="store_const",
        const=PlotType.LINE,
        help="Plot the mean time series as a line chart",
    )
    parser.add_argument("-t", "--title", default=Defaults.title, help="Plot title")
    parser.add_argument(
        "-x",
        "--x-label",
        default=Defaults.x_label,
        help="X-axis label",
    )
    parser.add_argument(
        "-y",
        "--y-label",
        default=Defaults.y_label,
        help="Y-axis label",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(
        "-D",
        "--debug",
        action="store_true",
        default=Defaults.debug,
        help="run program in debug mode",
    )

    parser.set_defaults(handler=handler)

    return parser


def handler(ns: argparse.Namespace) -> int:
    in_file: Path = ns.path
    mask_file: Path | None = ns.mask
    percentile: float = ns.percentile
    index_spec: str = ns.index_spec
    plot_type: PlotType = ns.plot_type
    title: str | None = ns.title
    x_label: str | None = ns.x_label
    y_label: str | None = ns.y_label

    img = nib.load(in_file)
    if mask_file is None:
        mask_img = compute_mask(img, percentile)
    else:
        mask_img = nib.load(mask_file)
    nvols = _get_nvols(img)
    indices = parse_index_spec(index_spec, nvols)
    means = compute_means(img, mask_img, indices)
    fig, ax = plot(
        means,
        plot_type=plot_type,
        title=title,
        x_label=x_label,
        y_label=y_label,
    )
    plt.show()

    return 0


def compute_mask(
    img: nib.Nifti1Image, percentile: float = Defaults.percentile
) -> nib.Nifti1Image:
    data = img.get_fdata()
    if img.ndim == 4:
        data = data.mean(axis=-1)
    thresh = np.percentile(data, percentile)
    mask = np.zeros(data.shape, dtype=int)
    mask[data > thresh] = 1
    mask_img = nib.Nifti1Image(mask, img.affine, img.header)
    return mask_img


def compute_means(
    img: nib.Nifti1Image, mask_img: nib.Nifti1Image, indices: list[int] | None = None
) -> list[tuple[int, float]]:
    data = img.get_fdata()
    if data.ndim == 3:
        data = np.expand_dims(data, axis=-1)

    mask = mask_img.get_fdata()

    if indices == None:
        indices = list(range(_get_nvols(img)))

    means = data[mask > 0, :][..., indices].mean(axis=0)  # type: ignore
    return list(zip(indices, means))


def _get_nvols(img: nib.Nifti1Image) -> int:
    return img.header["dim"][4]  # type: ignore


def plot(
    xy: list[tuple[int, float]],
    *,
    plot_type: PlotType = PlotType.LINE,
    title: str | None = Defaults.title,
    x_label: str | None = Defaults.x_label,
    y_label: str | None = Defaults.y_label,
):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(linestyle="--", linewidth=0.5)

    if plot_type == PlotType.LINE:
        x = [_x for _x, _ in xy]
        y = [_y for _, _y in xy]
        ax.plot(x, y)
    elif plot_type == PlotType.SCATTER:
        x = [_x for _x, _ in xy]
        y = [_y for _, _y in xy]
        ax.scatter(x, y, s=12)
    elif plot_type == PlotType.PAIRED_SCATTER:
        for p1, p2 in pairwise(xy):
            if p2 is not None:
                x1, y1 = p1
                x2, y2 = p2
                ax.plot([x1, x2], [y1, y2 ], c="C0")  # line connecting p1 and p2
                ax.scatter([x1, x2], [y1, y2], s=12, c="C0")  # scatter points p1 and p2
            else:
                # just the point (xy is odd length, i.e. this is the last point)
                x, y = p1
                ax.scatter([x], [y], s=12, c="C0")
    else:
        raise ValueError(f"Unexpected plot type: {plot_type!r}")

    return fig, ax


digit_regex = re.compile(r"^\d+$")
interval_regex = re.compile(
    r"^(?P<start>\-?\d*)\:(?P<stop>\-?\d*)(:(?P<step>\-?\d*))?$"
)


def parse_index_spec(idx_s: str, length: int) -> list[int]:
    """Parse and index specificaition string into a list of matching indices

    Examples:
        >>> length = 10
        >>> parse_index_spec('0', length)
        [0]
        >>> parse_index_spec(':5', length)
        [0, 1, 2, 3, 4]
        >>> parse_index_spec('::2', length)
        [0, 2, 4, 6, 8]
        >>> parse_index_spec('0,2:', length)
        [0, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> parse_index_spec('9,1,6:2:-1', length)
        [9, 1, 6, 5, 4, 3]
        >>> parse_index_spec(':3,7:', length)
        [0, 1, 2, 7, 8, 9]
    """
    indices: list[int] = []
    parts = idx_s.split(",")
    for interval_s in parts:
        slice_params = parse_interval(interval_s)
        indices.extend(range(length)[slice(*slice_params)])
    return indices


def parse_interval(interval_s: str) -> SliceParams:
    interval_s = interval_s.strip()
    _match = digit_regex.match(interval_s)
    if _match is not None:
        idx = int(_match.string)
        return SliceParams(idx, idx + 1, None)

    _match = interval_regex.match(interval_s)
    if _match is not None:
        groupdict = _match.groupdict()
        start = _coerce(groupdict["start"])
        stop = _coerce(groupdict["stop"])
        step = _coerce(groupdict["step"])
        return SliceParams(start, stop, step)

    raise SyntaxError(f"Failed to parse index specification: {interval_s!r}")


class SliceParams(NamedTuple):
    start: int | None
    stop: int | None
    step: int | None


def _coerce(s: str | None) -> int | None:
    if s is None or not s.strip():
        return None
    else:
        return int(s)


T = TypeVar("T")


def pairwise(iterable: Iterable[T]) -> Iterator[tuple[T, T | None]]:
    it = iter(iterable)
    for a in it:
        b = next(it, None)
        yield a, b


if __name__ == "__main__":
    cli()
