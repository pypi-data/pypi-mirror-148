from itertools import chain

import clease
import mincepy
import minkipy
from pyos import psh

import dragonfruit.clease as mc


def workon(directory="test_project/", project_name=None):
    # Change the active project
    minkipy.workon(project_name)
    psh.cd(directory)


def initialize_project():
    mc.init_bulk(crystalstructure="fcc", a=3.2275, c=5.57)

    # Set up the VASP settings
    general_settings = mincepy.Dict(
        xc="PBE",
        encut=400,
        setups="recommended",
        prec="Accurate",
        nelm=300,
        lmaxmix=4,
        lasph=True,
        ncore=8,
        ispin=2,
        nelmin=4,
        sigma=0.05,
        ismear=0,
        algo="all",
        lreal="Auto",
        lorbit=12,
        gamma=True,
        kptdensity=3.5,  # Custom keyword for dragonfruit "submit_structures" method
    )
    mc.save_settings(general_settings, mc.paths.GENERAL_SETTINGS)

    group_settings = mc.get_settings(mc.paths.GROUP_SETTINGS)
    group_settings.update({"full": mincepy.Dict(isif=3, ibrion=2, nsw=999, ediffg=-0.02)})
    group_settings.save()


def submit_structures(structures, group):
    print(f"Submitting group: {group}")
    task_ids = mc.submit_workflow(structures, group)
    print("New task ids:")
    for tid in task_ids:
        print(tid)


if __name__ == "__main__":
    workon()

    initialize_project()

    concentration = clease.Concentration(basis_elements=[["Mg", "Zn", "Ca"]])

    initial_directory = "initial"
    endpoints = mc.new_endpoints(concentration, directory=initial_directory)
    random = mc.new_random_structures(
        num_to_generate=3,
        concentration=concentration,
        size=(2, 2, 2),
        directory=initial_directory,
    )

    structures = list(chain(endpoints, random))

    submit_structures(structures, "full")
