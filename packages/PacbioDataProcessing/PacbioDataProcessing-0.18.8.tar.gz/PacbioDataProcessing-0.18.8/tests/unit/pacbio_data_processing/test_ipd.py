#######################################################################
#
# Copyright (C) 2021 David Palao
#
# This file is part of PacBio data processing.
#
#  PacBioDataProcessing is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PacBio data processing is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PacBioDataProcessing. If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

import unittest
from unittest.mock import patch, call
from pathlib import Path

from pacbio_data_processing.ipd import (
    ipd_summary, multi_ipd_summary_direct, multi_ipd_summary_threads,
    multi_ipd_summary,
)
from pacbio_data_processing.bam_utils import Molecule
from pacbio_data_processing.constants import DEFAULT_IPDSUMMARY_PROGRAM


@patch("pacbio_data_processing.ipd.subprocess.run")
class IdpSummaryTestCase(unittest.TestCase):
    def test_calls_run(self, prun):
        for model in (None, "some"):
            ipd_summary(
                (4, Molecule(4, Path("/a/b.bam"))), Path("/tmp/x.fasta"),
                DEFAULT_IPDSUMMARY_PROGRAM, 7,
                "7/,ñ,=", model, False
            )
            signature = (
                DEFAULT_IPDSUMMARY_PROGRAM, Path("/a/b.bam"), "--reference",
                Path("/tmp/x.fasta"), "--identify", "7/,ñ,=", "--numWorkers",
                "7", "--gff", Path("/a/b.gff")
            )
            if model:
                signature = signature + ("--ipdModel", "some")
            prun.assert_called_once_with(signature)
            prun.reset_mock()

    def test_returns_tuple_with_molecule_having_path_to_gff(self, prun):
        in_params = (
            ((6, Molecule(6, Path("/tmp/ss.killme"))),)
            + tuple(None for _ in range(6))
        )
        mol_id, molecule = ipd_summary(*in_params)
        self.assertEqual(molecule.gff_path, Path("/tmp/ss.gff"))


@patch("pacbio_data_processing.ipd.ipd_summary")
class MultiIpdSummaryTestCase(unittest.TestCase):
    IMPLEMENTATIONS = (multi_ipd_summary_direct, multi_ipd_summary_threads)

    def setUp(self):
        self.molecules = [
            (i, Molecule(i, Path(f"{bam}.bam"))) for i, bam in enumerate("abc")
        ]
        self.args = (
            self.molecules, Path("/tmp/x.fasta"),
            DEFAULT_IPDSUMMARY_PROGRAM, 1, 1,
            ["7/", "ñ", "="], None, False
        )

    def test_calls_ipd_summary(self, pipd_summary):
        for imulti_ipd_summary in self.IMPLEMENTATIONS:
            expected_calls = [
                call(
                    m, fasta=Path("/tmp/x.fasta"),
                    program=DEFAULT_IPDSUMMARY_PROGRAM,
                    nprocs=1, mod_types_comma_sep="7/,ñ,=",
                    ipd_model=None, skip_if_present=False)
                for m in self.molecules
            ]
            list(imulti_ipd_summary(*self.args))
            pipd_summary.assert_has_calls(expected_calls, any_order=True)
            pipd_summary.reset_mock()

    def test_returns_an_iterable(self, pipd_summary):
        for imulti_ipd_summary in self.IMPLEMENTATIONS:
            pipd_summary.side_effect = [8 for _ in self.molecules]
            result = imulti_ipd_summary(*self.args)
            self.assertEqual(list(result), [8 for _ in self.molecules])

    def test_default_implementation(self, pipd_summary):
        self.assertEqual(multi_ipd_summary, multi_ipd_summary_threads)
