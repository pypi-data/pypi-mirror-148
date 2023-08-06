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

from pytest import fixture
import numpy as n

import apav as ap
import apav.analysis.massspectrum as ms
from apav.utils.helpers import data_path

@fixture()
def fake_precip_roi() -> ap.Roi:
    """
    An roi with a fake spherical precipitate.

    Precipitate is a sphere at 0, 0, 0 with radius 5 about a total size of ~20x20x20nm (i.e. +- 10nm) with
    total number of counts = 150,000. All coordinates have a gaussian noise of sigma=0.4 applied

    The precipitate is composed of 25% atoms with mass/charge = 10 and 75% atoms = mass/charge = 3
    The matrix is composed of 75% atoms with mass/charge = 10 and 25% atoms = mass/charge = 3

    The positions are generated at random so tests for closeness should work but not tests for exactness
    """
    N = 150000
    all_x = n.random.uniform(-10, 10, 100000)
    all_y = n.random.uniform(-10, 10, 100000)
    all_z = n.random.uniform(-10, 10, 100000)
    idx = n.sqrt(all_x ** 2 + all_y ** 2 + all_z ** 2) < 5
    in_x = all_x[idx]
    in_y = all_y[idx]
    in_z = all_z[idx]
    out_x = all_x[~idx]
    out_y = all_y[~idx]
    out_z = all_z[~idx]
    m_x = n.concatenate([in_x[:in_x.size // 4], out_x[:(out_x.size // 4) * 3]])
    m_y = n.concatenate([in_y[:in_y.size // 4], out_y[:(out_y.size // 4) * 3]])
    m_z = n.concatenate([in_z[:in_z.size // 4], out_z[:(out_z.size // 4) * 3]])
    p_x = n.concatenate([in_x[in_x.size // 4:], out_x[(out_x.size // 4) * 3:]])
    p_y = n.concatenate([in_y[in_y.size // 4:], out_y[(out_y.size // 4) * 3:]])
    p_z = n.concatenate([in_z[in_z.size // 4:], out_z[(out_z.size // 4) * 3:]])
    s = 0.4
    p_x += n.random.normal(0, s, p_x.size)
    p_y += n.random.normal(0, s, p_y.size)
    p_z += n.random.normal(0, s, p_z.size)
    m_x += n.random.normal(0, s, m_x.size)
    m_y += n.random.normal(0, s, m_y.size)
    m_z += n.random.normal(0, s, m_z.size)

    xyz = n.array([
        n.concatenate([p_x, m_x]),
        n.concatenate([p_y, m_y]),
        n.concatenate([p_z, m_z])
    ]
    ).T

    print(xyz.shape)
    mass = n.concatenate([n.tile(3, p_x.size), n.tile(10, m_x.size)])

    roi = ap.Roi(xyz, mass)

    return roi

@fixture()
def singles_roi() -> ap.Roi:
    """
    Fixture roi containing only single multiplicity ions
    """
    ipp = n.array([1, 1, 1, 1, 1, 1, 1])
    mass = n.array([1, 1.1, 3, 5.6, 12, 3.4, 3.5])
    xyz = n.array([[1, 0, 0],
                   [1, 1, 0],
                   [4, 2, 1],
                   [4, 7, 1],
                   [4, 7, 9],
                   [8, 2, 4],
                   [9, 4, 3]])

    roi = ap.Roi(xyz, mass)
    roi.misc["ipp"] = ipp
    return roi


@fixture()
def doubles_roi() -> ap.Roi:
    """
    Roi fixture containing single and double multiplicity ions
    """
    ipp = n.array([2, 0, 1, 2, 0, 2, 0])
    mass = n.array([1, 1.1, 3, 5.6, 12, 3.4, 3.5])
    xyz = n.array([[1, 0, 0],
                   [1, 1, 0],
                   [4, 2, 1],
                   [4, 7, 1],
                   [4, 7, 9],
                   [8, 2, 4],
                   [9, 4, 3]])

    roi = ap.Roi(xyz, mass)
    roi.misc["ipp"] = ipp
    return roi


@fixture()
def triples_roi() -> ap.Roi:
    """
    Roi fixture containing single, double, and triple multiplicity ions
    """
    ipp = n.array([2, 0,   1, 3, 0, 0, 2,   0,  2,   0,   3, 0, 0])
    mass = n.array([1, 1.1, 3, 1, 2, 3, 5.6, 12, 3.4, 3.5, 4, 5, 6])
    det_x = n.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    det_y = n.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130])
    tof = n.array([3, 23, 120, 32, 34, 2, 430, 23, 54, 15, 76, 87, 13])
    xyz = n.array([[1, 0, 0],
                   [1, 1, 0],
                   [4, 2, 1],
                   [4, 7, 1],
                   [8, 2, 4],
                   [4, 7, 9],
                   [4, 2, 1],
                   [8, 2, 4],
                   [4, 7, 1],
                   [8, 2, 4],
                   [1, 1, 0],
                   [4, 2, 1],
                   [9, 4, 3]])

    roi = ap.Roi(xyz, mass)
    roi.misc["ipp"] = ipp
    roi.misc["det_x"] = det_x
    roi.misc["det_y"] = det_y
    roi.misc["tof"] = tof
    return roi


@fixture()
def triples_range() -> ap.RangeCollection:
    """
    Synthetic RangeCollection fixture for use with triples_roi
    """
    retn = ap.RangeCollection()
    retn.add(ap.Range("A", (6, 13)))
    retn.add(ap.Range("A2", (0, 3)))
    retn.add(ap.Range("B", (3, 5)))
    retn.add(ap.Range("C", (40, 50)))
    return retn


@fixture(scope="module")
def si_roi() -> ap.Roi:
    roi = ap.Roi.from_epos(data_path("Si.epos"))
    return roi


@fixture(scope="module")
def si_range():
    rng = ap.RangeCollection.from_rrng(data_path("Si.RRNG"))
    return rng


@fixture(scope="module")
def si_ranged_ms(si_range, si_roi):
    mass = ms.RangedMassSpectrum(si_roi, si_range)
    return mass


@fixture()
def si_ranged_ms_plot(si_ranged_ms):
    plot = si_ranged_ms.plot()
    return plot
