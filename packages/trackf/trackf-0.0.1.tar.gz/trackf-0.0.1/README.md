# trackf
## Description
trackf package performs an analysis of the state of polymer chain extension 
and chain breakage in elongational flow on the data from the LAMMPS parallel
simulations. This package will include 5 functions that will perform the following tasks,
1) Track the location and the Hencky strain (time frame) at which the chain breaks
2) Count the number of monomers in the chains and calculate fracture sites
3) Output a graph showing the distribution of the location of chain fracture and a histogram
4) Output the result as a csv file wtih headings

## Installation

Use "pip install" to install track_fracture.

```bash
pip install trackf
```

## Usage

```python
from trackf import ctrack

# returns fracture site
ctrack.getsite(fname,M)

# returns information about breakage
ctrack.getbreak(fname,M)

# returns fracture sites plot as a 2D-density plot
ctrack.plotdensity(fname,M)
```
<img src="./example_results/density_plot.svg"/>

```python
# returns a histogram plot of total fracture site distribution
ctrack.histogram(fname,M)
```
<img src="./example_results/hist_plot.svg"/>

```python
# save results from function (func i.e. getbreak() and/or getsite()) to csv file in fpath location
ctrack.file_to_csv(func,fpath)
```
Or you might import this package using wildcard (*). This way, you could execute the command
without having to include ctrack.

```python
from trackf.ctrack import *
getsite(fname,M)
```

For more examples on how to use this package, see *example.ipynb*

## License
GPL


## Trackf Project Details
This package will be written for Kremer-Grest bead-spring chains which are modelled using quartic potential 
in LAMMPS parallel MD with periodic boundary conditions. The non-equilibrium molecular
dynamics (NEMD) is employed to simulate a system under diagonal flow field which composed of uniaxial
and bi-axial flow. This fix is an integration of the Generalized Kraynik Reinelt (GRK) boundary
conditions and the SLLOD equations of motion for general homogeneous flow. 

Requirement of the output data from LAMMPS:
1) Positions of monomers (in Cartesian coordinate system)
2) Potential energy of monomers
4) Molecule Identifier
5) Atom Identifier
6) Time
7) The elongational flow rate

### Example dump output line in LAMMPS script:
    compute     be all pe/atom bond
    dump    	1 all netcdf ${dint} dump_draw.nc id mol x y z c_be
