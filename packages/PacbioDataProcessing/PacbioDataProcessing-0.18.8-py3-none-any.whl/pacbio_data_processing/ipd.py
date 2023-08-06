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

import subprocess
import functools
import logging
from concurrent import futures
from typing import Union, Optional
from collections.abc import Generator
from pathlib import Path

from .bam_utils import WorkUnitGenerator, MoleculeWorkUnit
from .constants import GFF_SUF


class UnknownErrorIpdSummary(Exception):
    ...


def ipd_summary(
        molecule: MoleculeWorkUnit,
        fasta: Union[str, Path],
        program: Union[str, Path],
        nprocs: int,
        mod_types_comma_sep: str,
        ipd_model: Union[str, Path],
        skip_if_present: bool
        ) -> MoleculeWorkUnit:
    """Lowest level interface to ``ipdSummary``: all calls to that
    program are expected to be done through this function.
    It runs ``ipdSummary`` with an input bam file like this::

      ipdSummary  blasr.pMA683.subreads.bam --reference pMA683.fa\
      --identify m6A --gff blasr.pMA683.subreads.476.bam.gff

    As a result of this, a gff file is created. This function sets an
    attribute in the target Molecule with the path to that file.

    TBD
    ---
    Missing features:

    * skip_if_present
    * logging
    * error handling
    * check output and raise error if != 0
    """
    molecule_id, molecule = molecule
    bam = molecule.src_bam_path
    output = bam.with_suffix(GFF_SUF)
    cmd = (
        program, bam, "--reference", fasta, "--identify", mod_types_comma_sep,
        "--numWorkers", str(nprocs), "--gff", output
    )
    if ipd_model:
        cmd = cmd + ("--ipdModel", ipd_model)
    subprocess.run(cmd)  # , check=True)
    molecule.gff_path = output
    return (molecule_id, molecule)


def old_ipd_summary(
        molecule, fasta, program, nprocs, mod_types_comma_sep,
        ipd_model, skip_if_present):
    out_name = molecule.with_suffix(molecule.suffix+GFF_SUF)
    exe = (
        program, molecule, "--reference", fasta, "--identify",
        mod_types_comma_sep, "--numWorkers", nprocs, "--gff", out_name
    )
    if ipd_model:
        exe = exe + ("--ipdModel", ipd_model)
    if skip_if_present and out_name.is_file():
        logging.debug(f"Modification file '{out_name}' already present!")
    else:
        while True:
            try:
                proc = subprocess.run(exe)
                if proc.returncode != 0:
                    raise UnknownErrorIpdSummary(
                        f"returncode: {proc.returncode}")
                # time.sleep(0.1)
                # logging.debug((
                #     (program, molecule, "--reference", fasta, "--identify",
                #      mod_types_comma_sep, "--numWorkers", nprocs,
                #      "--gff", str(out_name))
                # ))
            except Exception as e:
                msg = str(e)
                logging.error(f"[{program}][{out_name}] {msg}")
            else:
                logging.info(f"Modification file '{out_name}' generated")
                break
    return out_name


def multi_ipd_summary_direct(
        molecules: WorkUnitGenerator,
        fasta: Union[str, Path],
        program: Union[str, Path],
        num_ipds: int,
        nprocs_per_ipd: int,
        modification_types: str,
        ipd_model: Optional[str]=None,
        skip_if_present: bool=False
        ) -> Generator[Path, None, None]:
    """Generator that yields gff files as they are produced.
    Serial implementation (one file produced after the other).
    """
    mod_types_comma_sep = ",".join(modification_types)
    for molecule in molecules:
        yield ipd_summary(
            molecule, fasta=fasta, program=program, nprocs=nprocs_per_ipd,
            mod_types_comma_sep=mod_types_comma_sep, ipd_model=ipd_model,
            skip_if_present=skip_if_present
        )


def multi_ipd_summary_threads(
        molecules: WorkUnitGenerator,
        fasta: Union[str, Path],
        program: Union[str, Path],
        num_ipds: int,
        nprocs_per_ipd: int,
        modification_types: str,
        ipd_model: Optional[str]=None,
        skip_if_present: bool=False
        ) -> Generator[Path, None, None]:
    """Generator that yields gff files as they are produced in parallel.
    Implementation drived by a pool of threads.
    """
    mod_types_comma_sep = ",".join(modification_types)
    partial_ipd_summary = functools.partial(
        ipd_summary, fasta=fasta, program=program, nprocs=nprocs_per_ipd,
        mod_types_comma_sep=mod_types_comma_sep, ipd_model=ipd_model,
        skip_if_present=skip_if_present,
    )
    exe = futures.ThreadPoolExecutor(max_workers=num_ipds)
    yield from exe.map(partial_ipd_summary, molecules)


multi_ipd_summary = multi_ipd_summary_threads
