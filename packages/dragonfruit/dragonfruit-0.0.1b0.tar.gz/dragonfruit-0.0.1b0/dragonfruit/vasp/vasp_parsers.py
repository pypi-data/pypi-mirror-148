"""Module for doing some parsing of VASP files. Likely only to be used temporarily."""
from pathlib import Path, PurePath
from typing import Union
import re
import warnings
from xml.etree.ElementTree import ParseError as XmlParseError

import numpy as np
from ase import io
from ase.io import ParseError as AseParseError

from mincepy.builtins import File

__all__ = (
    "parse_scf",
    "read_is_crashed",
    "read_is_converged",
    "get_file",
    "is_outcar_corrupt",
    "is_xml_corrupt",
    "is_output_corrupt",
    "get_ok_output_files",
)

_pathtypes = Union[str, Path, File]


def get_file(vasppath: _pathtypes):
    if isinstance(vasppath, File):
        return vasppath
    if not isinstance(vasppath, PurePath):
        vasppath = Path(vasppath)

    if not vasppath.is_file():
        msg = f"I cannot find the file {vasppath}"
        raise IOError(msg)

    return vasppath


def open_file(file, mode="r"):
    """Allow for opening files with compression, such as gzip files"""
    if isinstance(file, File):
        return file.open(mode)
    return io.formats.open_with_compression(file, mode)


def parse_scf(outcar: _pathtypes):
    """Get the SCF energy. Based on Alexander's grad2 script."""
    outcar = get_file(outcar)

    scf_prev = 0.0
    scf_cur = 0.0

    re_scf_en = "free energy    TOTEN"
    re_energy = "free  energy"

    scf_energies = []
    with open_file(outcar) as file:
        for line in file:
            line = line.strip()

            if re_scf_en in line:
                parts = line.split()
                scf_prev = scf_cur
                scf_cur = float(parts[4])

            if re_energy in line:
                # End of SCF cycle
                scf_energies.append(abs(scf_cur - scf_prev))
    return np.array(scf_energies)


def read_is_crashed(outcar: _pathtypes) -> bool:
    """Check if VASP printed end timing statements in OUTCAR.
    Returns True if job is considered crashed, otherwise False"""
    outcar = get_file(outcar)

    with outcar.open() as file:
        for line in file:
            if "General timing and accounting" in line:
                return False
    return True


def read_is_converged(outcar: _pathtypes) -> bool:
    """Determine if VASP calculation converged based on messages ín the VASP OUTCAR"""
    # pylint: disable=too-many-branches
    outcar = get_file(outcar)

    nsw = None
    nelm = None
    ibrion = None

    with open_file(outcar) as file:
        # Parsing the header part of the OUTCAR
        for line in file:
            line = line.strip()
            # We're only looking for specific keys
            if nsw is None or nelm is None or ibrion is None:
                # Example line:
                # NSW    =    200    number of steps for IOM
                if "NSW" in line:
                    parts = line.split()
                    nsw = int(parts[2])
                elif "IBRION" in line:
                    # Example line:
                    # IBRION =      1    ionic relax: 0-MD 1-quasi-New 2-CG
                    parts = line.split()
                    ibrion = int(parts[2])
                elif "NELM" in line:
                    # Example line for NELM:
                    # NELM   =    100;   NELMIN=  2; NELMDL=  0     # of ELM steps
                    temp = re.findall(r"\d+", line)
                    nelm = list(map(int, temp))[0]
            else:
                # We have all the information we need from the header
                break  # We are done parsing the header

        # IBRION = 0 is MD, not a relaxation
        is_relaxation = ibrion in [1, 2, 3] and nsw > 0
        n_el = 0  # Electronic step
        n_ion = 0  # Ionic step
        conv_el = False  # Electronic convergence reached?
        # Ionic convergence? Only gets updated in dynamics
        # i.e., will not get updated in a singlepoint calculation
        # Instantiate as negation of is_relaxation, as the relaxation line is only printed
        # during dynamics, so we only expect it for relaxation schemes.
        conv_ion = not is_relaxation
        for line in file:
            line = line.strip()
            if "- Iteration" in line:
                # Extract current ionic and electronic step number
                # Example line:
                # ---- Iteration      1(   2)  -----------
                temp = re.findall(r"\d+", line)
                if len(temp) != 2:
                    # in VASP, they did some bad formatting, so if the counter goes above 1000,
                    # FORTRAN just writes ****, and this breaks parsing.
                    msg = (
                        "Did you use NELM or NSW > 1000? This will probably break"
                        " parsing of the OUTCAR, due to numerical formating in FORTRAN!\n"
                        "I did not find 2 values in the iteration counter. I'll just assume"
                        " the calculation converged, and hope everything is OK!"
                    )
                    warnings.warn(msg)
                    return True
                n_ion, n_el = list(map(int, temp))

            if "aborting loop because EDIFF is reached" in line:
                # Electronic accuracy reached - did we terminate because we reached NELM?
                # We only care about the last iteration, so we keep updating this.
                conv_el = n_el < nelm

            if "reached required accuracy" in line:
                # Ionic accuracy reached - did we terminate because we reached NSW?
                if n_ion >= nsw:
                    conv_ion = False
                else:
                    conv_ion = True
                break  # We're done, just break out

    converged = conv_el and conv_ion
    return converged


def is_xml_corrupt(filename="vasprun.xml") -> bool:
    """Helper function for determining if the XML file is readable"""
    file = Path(filename)

    try:
        io.read(file, format="vasp-xml")
    except (XmlParseError, IndexError, AttributeError, ValueError):
        # AttributeError: Typically if the vasprun.xml doesnt have a calculator
        # IndexError: Similar story
        # XmlParseError: Something went wrong in the XML parser
        # ValueError: Vasp wrote some garbage like: '**************** '
        #   so the error happenes because of the formatting of a line,
        #   it tried to convert a float.
        return True
    return False


def is_outcar_corrupt(filename="OUTCAR") -> bool:
    """Check we can read the last image from the OUTCAR.
    Note: We don't care about middle images being corrupt.
    """
    file = Path(filename)

    try:
        io.read(file, format="vasp-out", index=-1)
    except (IOError, ValueError, IndexError, AseParseError):
        # ValueError: Formatting of a line, it tried to convert a float.
        # IOError: Current ASE error which is raised in the reader. Should be changed in the future
        # IndexError: We didn't even write the lattice constant
        # AseParseError: Some error happened in ASE when parsing the OUTCAR
        return True
    return False


def is_output_corrupt(path=".", outcar_file="OUTCAR", xml_file="vasprun.xml") -> bool:
    """Check if both OUTCAR and XML files are corrupted"""
    path = Path(path)
    return is_outcar_corrupt(path / outcar_file) and is_xml_corrupt(path / xml_file)


def get_ok_output_files(path="."):
    """Check if the VASP files are corrupt. Checks the OUTCAR and vasprun.xml

    Returns the files which ASE was able to parse.
    """
    path = Path(path)
    ok_files = []
    for filename, is_corrupt in [("OUTCAR", is_outcar_corrupt), ("vasprun.xml", is_xml_corrupt)]:
        if not is_corrupt(path / filename):
            ok_files.append(filename)
    return ok_files
