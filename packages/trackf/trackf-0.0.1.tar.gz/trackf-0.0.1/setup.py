from setuptools import setup

setup(
    name="trackf",
    version="0.0.1",
    description="tracking polymer chain breakage",
    maintainer="Nattavipa Chongvimansin",
    maintainer_email="nchongvi@andrew.cmu.edu",
    license="GPL",
    platforms=["linux"],
    packages=["trackf"],
    scripts=["trackf/ctrack.py", "trackf/ctrack_t.py"],
    setup_requires=[],
    data_files=["LICENSE"],
    install_requires=["numpy", "netCDF4", "matplotlib", "scipy",
                    "csv", "warnings"],
    long_description="""
A module for tracking the location, molecule identifiers,
and timeframe of breakage.
==============
Handy scripts for the tracking chain breakage project.
      """,
)
