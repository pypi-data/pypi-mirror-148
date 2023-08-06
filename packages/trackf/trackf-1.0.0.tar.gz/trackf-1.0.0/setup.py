"""Setup for trackf package."""
from setuptools import setup

setup(
    name="trackf",
    version="1.0.0",
    description="tracking polymer chain breakage",
    maintainer="Nattavipa Chongvimansin",
    maintainer_email="nchongvi@andrew.cmu.edu",
    license="GPL",
    platforms=["linux"],
    packages=["trackf"],
    scripts=["trackf/ctrack.py"],
    setup_requires=[],
    data_files=["LICENSE"],
    install_requires=["numpy", "netCDF4", "matplotlib", "scipy"],
    long_description="""
A module for tracking the location, molecule identifiers,
and timeframe of breakage.
===============================================
trackf package performs an analysis of the state of polymer chain
extension and chain breakage in elongational flow on the data from
the LAMMPS parallel simulations.
      """,
)
