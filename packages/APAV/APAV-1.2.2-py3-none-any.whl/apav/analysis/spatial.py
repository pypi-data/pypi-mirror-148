"""
This file is part of APAV.

APAV is a python package for performing analysis and visualization on
atom probe tomography data sets.

Copyright (C) 2018 Jesse Smith

APAV is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

APAV is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with APAV.  If not, see <http://www.gnu.org/licenses/>.
"""

from apav.analysis.base import AnalysisBase
from apav.utils import validate
from apav.utils.hinting import *
from apav import Roi, RangeCollection, Ion
from apav.core.histogram import histogram2d_binwidth
from apav.core.multipleevent import get_mass_indices
from scipy.ndimage import gaussian_filter
import numpy as n
import numba as nb
import multiprocessing as mp


@nb.jit(nopython=True, nogil=True)
def pass1(X: n.ndarray, Y: n.ndarray, Z: n.ndarray, pos: n.ndarray, stddev3: Real):
    """
    Numba accelerated function for computing first pass delocalization based on a gaussian transfer function
    :param X: voxel centers array in x axis
    :param Y: voxel centers array in y axis
    :param Z: voxel centers array in z axis
    :param pos: Array of positions
    :param stddev3: Third standard deviation of gaussian
    """
    bin_width = X[1, 0, 0] - X[0, 0, 0]
    r = bin_width/2

    kernel_dim = 3  # 3x3 px
    XYZ_min = n.array((X.min(), Y.min(), Z.min()))
    XYZ_max = n.array((X.max(), Y.max(), Z.max()))

    # Kernel dimensions must be odd
    assert kernel_dim % 2 == 1
    k_half = (kernel_dim - 1) // 2

    retn = n.zeros((X.size, Y.size, Z.size))

    s = stddev3/3

    kernel = n.array(())
    idx = n.array(())
    for xyz in pos:
        idx = ((xyz - (XYZ_min - r)) // bin_width)  # The central containing voxel index

        xid0 = int(max(idx[0] - k_half, 0))
        xid1 = int(min(idx[0] + k_half + 1, X.size))
        yid0 = int(max(idx[1] - k_half, 0))
        yid1 = int(min(idx[1] + k_half + 1, Y.size))
        zid0 = int(max(idx[2] - k_half, 0))
        zid1 = int(min(idx[2] + k_half + 1, Z.size))

        kernel = n.exp(-((X[xid0:xid1, :, :] - xyz[0]) ** 2 + (Y[:, yid0:yid1, :] - xyz[1]) ** 2 + (
                    Z[:, :, zid0:zid1] - xyz[2]) ** 2) / (2 * s ** 2))

        # Normalize kernel to unity
        kernel /= kernel.sum()

        retn[xid0: xid1, yid0: yid1, zid0: zid1] += kernel

    return retn


class RangedGrid(AnalysisBase):
    """
    Compute the ionic and elemental composition spatially distributed among a structured grid
    """
    def __init__(self,
                 roi: Roi,
                 ranges: RangeCollection,
                 bin_width: Real = 1,
                 first_pass: bool = True,
                 delocalization: Union[Real, Sequence[Real]] = n.array([3, 3, 1.5]),
                 gauss_trunc: Real = 4
                 ):
        """
        :param roi: Parent the RangedGrid is competed on
        :param ranges: RangeCollection defining the ranges
        :param bin_width: symmetric bin width size
        :param first_pass: Whether the first pass delocalization is computed using a gaussian transfer function.
        :param delocalization: The delocalization distances (as 3 standard deviations of a normal distribution)
        :param gauss_trunc: Number of standard deviations to truncate the gaussian kernel for second pass delocalization
        """
        super().__init__(roi)
        self._ranges = validate.is_type(ranges, RangeCollection)

        self._voxel = validate.positive_nonzero_number(bin_width)
        self._delocalization = delocalization

        if hasattr(delocalization, "__iter__") and not isinstance(delocalization, ndarray):
            self._delocalization = n.array(delocalization)

        if not hasattr(delocalization, "__iter__"):
            self._delocalization = n.array([delocalization]*3)

        if not all(i > 0 for i in self._delocalization):
            raise ValueError("Delocalization distances must be positive and non-zero")

        self._gauss_trunc = validate.positive_nonzero_number(gauss_trunc)

        self._X = ndarray([])
        self._Y = ndarray([])
        self._Z = ndarray([])
        self._ion_counts = {}
        self._elem_frac = {}
        self._elem_counts = {}
        self._elem_cum_counts = None
        self._first_pass = first_pass

        self._calculate()

    @property
    def ranges(self) -> RangeCollection:
        """
        The ranges use for ranging the mass spectrum
        :return:
        """
        return self._ranges

    @property
    def first_pass(self) -> bool:
        """
        Whether to compute first pass delocalization
        """
        return self._first_pass

    @property
    def centers(self) -> Tuple[ndarray, ndarray, ndarray]:
        """
        The centers positions of the structured grids

        For MxNxP voxels this returns 3 arrays of dimensions: Mx1x1, 1xNx1, 1x1xP
        """
        return self._X, self._Y, self._Z

    @property
    def bin_width(self) -> Real:
        """
        Bin width of the voxels
        """
        return self._voxel

    @property
    def delocalization(self) -> Union[Real, Sequence[Real]]:
        """
        Amount of smoothing used during the delocalization process
        """
        return self._delocalization

    @property
    def gauss_trunc(self) -> Real:
        """
        Where to truncate the gaussian kernel for second pass delocalization
        """
        return self._gauss_trunc

    @property
    def all_ionic_counts(self) -> Dict[Ion, ndarray]:
        """
        Get all ionic count grids in a dict
        """
        return self._ion_counts

    @property
    def all_elemental_frac(self) -> Dict[Element, ndarray]:
        """
        Get all elemental fraction grids as a dict
        """
        return self._elem_frac

    @property
    def all_elemental_frac_str(self) -> Dict[Ion, ndarray]:
        """
        Get all elemental fraction grids as a dictionary (using elemental symbols)
        """
        return {i.symbol: j for i, j in self._elem_frac.items()}

    @property
    def elemental_counts_total(self) -> Real:
        """
        The total (sum) of all elemental counts
        """
        return self._elem_cum_counts

    def ionic_counts(self, ion: Ion) -> ndarray:
        """
        Get a single ionic counts grid
        :param ion: The ion of the grid to return
        """
        if ion not in self.all_ionic_counts.keys():
            raise ValueError("Ion {} does not exist in the RangedGrid".format(ion.hill_formula))
        return self.all_ionic_counts[ion]

    def elemental_frac(self, element: Union[str, Element]) -> ndarray:
        """
        Get a single elemental fraction grid
        :param element: the elemental of the grid to return (Element or str)
        """
        if isinstance(element, str):
            el = None
            for i, j in self.all_elemental_frac.items():
                if i.symbol == element:
                    el = i
                    break
            return self.all_elemental_frac[el]
        elif isinstance(element, Element):
            return self.all_elemental_frac[element]
        else:
            raise TypeError("Expected elemental symbol string or Element type, got {} instead".format(type(element)))

    def _calculate(self):
        """
        Compute the ranged grids
        """
        dims = self.roi.dimensions
        n_voxels = n.ceil(dims / self.bin_width).ravel().astype(int)

        dx, dy, dz = self.roi.xyz_extents
        range_elems = self.ranges.elements()

        self._ion_counts = {i.ion: n.zeros(n_voxels) for i in self.ranges.ranges}

        r = self.bin_width/2
        X, Y, Z = n.ogrid[
            dx[0] + r: (dx[0] + r) + self.bin_width * (n_voxels[0]-1): (n_voxels[0]) * 1j,
            dy[0] + r: (dy[0] + r) + self.bin_width * (n_voxels[1]-1): (n_voxels[1]) * 1j,
            dz[0] + r: (dz[0] + r) + self.bin_width * (n_voxels[2]-1): (n_voxels[2]) * 1j,
        ]
        self._X = X
        self._Y = Y
        self._Z = Z

        if not self.first_pass:
            stddev = (self.delocalization / 3)
        else:
            pass1_3sigma = self.bin_width/2
            # stddev = (self.delocalization/3)/self.bin_width
            stddev = n.sqrt((self.delocalization / 3) ** 2 - n.tile(pass1_3sigma / 3, 3) ** 2)

        stddev_vox = stddev / self.bin_width

        init_counts = []
        final_counts = []

        def ranged_xyz(rng):
            low, up = rng.interval
            idx = n.argwhere((self.roi.mass >= low) & (self.roi.mass < up)).ravel()
            init_counts.append(idx.shape[0])
            return self.roi.xyz[idx].astype(float)

        N = len(self.ranges)
        nproc = min(N, mp.cpu_count())

        if self.first_pass:
            if self.roi.counts > 5e6:
                with mp.Pool(nproc) as _pool:
                    result = _pool.starmap(
                    pass1,
                    zip(
                        [X for _ in range(N)],
                        [Y for _ in range(N)],
                        [Z for _ in range(N)],
                        [ranged_xyz(i) for i in self.ranges],
                        [pass1_3sigma]*N
                    ),
                    )
            else:
                result = [pass1(X, Y, Z, ranged_xyz(i), pass1_3sigma) for i in self.ranges]
        else:
            result = []
            for i, rng in enumerate(self.ranges):
                coords = ranged_xyz(rng)
                counts, _ = n.histogramdd(coords, bins=n_voxels)
                result.append(counts)

        for i, data in zip(self.ranges, result):
            final_counts.append(n.sum(data))
            nan = n.count_nonzero(n.isnan(data))
            if nan > 0:
                raise ArithmeticError("NaNs encountered during first pass delocalization, try picking a different bin width")
            self._ion_counts[i.ion] += gaussian_filter(data,
                                                       sigma=stddev_vox,
                                                       # mode="constant",
                                                       truncate=self.gauss_trunc)

        self._elem_frac = {i: 0 for i in range_elems}
        self._elem_counts = {i: 0 for i in range_elems}
        elem_counts = self._elem_counts

        for ion, counts in self._ion_counts.items():
            for elem, mult in ion.comp_dict.items():
                elem_counts[elem] += mult * counts

        norm = sum(i for i in elem_counts.values())
        self._elem_cum_counts = norm
        for key in elem_counts.keys():
            ary = elem_counts[key]
            self._elem_frac[key] = n.divide(ary, norm, where=ary > 0)


class DensityHistogram(AnalysisBase):
    """
    Compute density histograms on an Roi
    """
    def __init__(self,
                 roi: Roi,
                 bin_width=0.3,
                 axis="z",
                 multiplicity="all"):
        """
        :param roi: region of interest
        :param bin_width: width of the bin size in Daltons
        :param axis: which axis the histogram should be computed on ("x", "y", or "z")
        :param multiplicity: the multiplicity order to compute histogram with
        """
        super().__init__(roi)
        self.bin_width = validate.positive_nonzero_number(bin_width)
        self._multiplicity = validate.multiplicity_any(multiplicity)
        if multiplicity != "all":
            roi.require_multihit_info()

        self._histogram = None
        self._histogram_extents = None
        self._axis = validate.choice(axis, ("x", "y", "z"))
        self._bin_vol = None
        self._calculate_histogram()

    @property
    def multiplicity(self):
        return self._multiplicity

    @property
    def bin_vol(self):
        return self._bin_vol

    @property
    def axis(self):
        return self._axis

    @property
    def histogram(self):
        return self._histogram

    @property
    def histogram_extents(self):
        return self._histogram_extents

    def _calculate_histogram(self):
        orient_map = {"x": 0, "y": 1, "z": 2}
        ax1, ax2 = (self.roi.xyz[:, val] for key, val in orient_map.items() if key != self.axis)
        ext_ax1, ext_ax2 = (self.roi.xyz_extents[val] for key, val in orient_map.items() if key != self.axis)
        ext = (ext_ax1, ext_ax2)

        if self.multiplicity == "all":
            self._histogram = histogram2d_binwidth(ax1, ax2, ext, self.bin_width)
        else:
            idx = get_mass_indices(self.roi.misc["ipp"], self.multiplicity)
            self._histogram = histogram2d_binwidth(ax1[idx], ax2[idx], ext, self.bin_width)

        self._histogram_extents = ext
