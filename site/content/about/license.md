---
title : "License"
description: "License"
draft: false
images: []
toc: true
layout: "single"
---

Chaste is released under an open source [BSD 3-Clause License](https://opensource.org/license/bsd-3-clause/).

This means that anyone is free to use Chaste for any purpose, to modify it, to redistribute a modified version, or to use it in closed-source and/or commercial projects. Please see [this guide](https://fossa.com/blog/open-source-software-licenses-101-bsd-3-clause-license/) for more information and comparison with other licenses.

## Third party packages

Chaste depends on many third-party packages to provide some of the core functionality. 
A full list of these, together with their licences, is given below.

In most cases, source code for these packages is not distributed with Chaste
(notable exceptions are triangle, Tetgen and CxxTest).  They must instead be
installed separately.  

The 'Used by' column indicates where these libraries are used:

- **Distributed:** source code that is distributed with the Chaste source  
- **Source:** required for building Chaste from source  
- **Tests:** only required for testing Chaste  
- **Cardiac:** only really needed if you're building the cardiac-specific source  
- **Optional:** may be used by Chaste if installed, but not essential  

| Library/package   | Licence URL                                                                                                                                             | Local copy of licence                                                                                                                                                                                                      | Used by                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| Boost             | [boost.org](http://www.boost.org/users/license.html)                                                                                                    | [Boost.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/Boost.txt)                                                                                                                               | Source                             |
| CodeSynthesis XSD | [xsd license](http://www.codesynthesis.com/products/xsd/license.xhtml), [FLOSSE](http://www.codesynthesis.com/projects/xsd/FLOSSE)                      | (GPL) [CodeSynthesis_Exception.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/CodeSynthesis_Exception.txt)                                                                                     | Source, Cardiac                    |
| CVODE (SUNDIALS)  | [sundials license](https://computing.llnl.gov/projects/sundials/license)                                                                                | (BSD) [CVODE.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/CVODE.txt)                                                                                                                         | Optional                           |
| CxxTest           | [LGPL](http://www.gnu.org/copyleft/lesser.html)                                                                                                         | (LGPL) [CxxTest.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/CxxTest.txt)                                                                                                                    | Tests, Distributed                 |
| HDF5              | [hdfgroup.org](http://www.hdfgroup.org/products/licenses.html)                                                                                          | [HDF5.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/HDF5.txt)                                                                                                                                 | Source                             |
| OpenSimplex       | [UNLICENSE](https://github.com/KdotJPG/OpenSimplex2/blob/master/_old/cpp/UNLICENSE)                                                                     | [UNLICENSE](https://github.com/Chaste/Chaste/blob/develop/mesh/src/3rdparty/opensimplex/UNLICENSE)                                                                                                                         | Source, Distributed                |
| (Par)METIS        | [metis faq](http://glaros.dtc.umn.edu/gkhome/metis/metis/faq?q=metis/metis/faq#distribute)                                                              | [METIS.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/METIS.txt), [manual](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/METIS_manual.pdf)                             | Source                             |
| MPICH             | [COPYRIGHT](https://github.com/pmodels/mpich/blob/main/COPYRIGHT), [ROMIO](https://www.anl.gov/mcs/romio-highperformance-portable-mpiio-implementation) | [mpich-license.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/mpich-license.txt), [romio-license.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/romio-license.txt) | Source (or other MPI like OpenMPI) |
| PETSc             | [petsc.org](https://petsc.org/release/install/license/)                                                                                                 | [PETSc.html](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/PETSc.html)                                                                                                                             | Source                             |
| Pocketfft         | [LICENSE.md](https://gitlab.mpcdf.mpg.de/mtr/pocketfft/-/blob/master/LICENSE.md)                                                                        | [LICENSE.md](https://github.com/Chaste/Chaste/blob/develop/mesh/src/3rdparty/pocketfft-src/LICENSE.md)                                                                                                                     | Source, Distributed                |
| Pyparsing         | [Pyparsing home](https://pypi.org/project/pyparsing/)                                                                                                   | (MIT) [pyparsing.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/pyparsing.txt)                                                                                                                 | Source, Cardiac, Distributed       |
| RDFLib            | [rdflib license](http://code.google.com/p/rdflib/source/browse/LICENSE)                                                                                 | (BSD) [RDFLib.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/RDFLib.txt)                                                                                                                       | Source, Cardiac                    |
| RNV               | [rnv license](http://ftp.davidashen.net/PreTI/RNV/license.txt)                                                                                          | (BSD) [rnv.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/rnv.txt)                                                                                                                             | Source, Cardiac                    |
| TetGen            | [tetgen.berlios.de](http://tetgen.berlios.de/)                                                                                                          | [TetGen](https://github.com/Chaste/Chaste/blob/develop/mesh/src/3rdparty/tetgen1.4.2/LICENSE)                                                                                                                              | Source, Distributed                |
| triangle          | [triangle](http://www.cs.cmu.edu/~quake/triangle.html)                                                                                                  | [Triangle.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/Triangle.txt)                                                                                                                         | Source, Distributed                |
| VTK               | [vtk.org license](https://vtk.org/about/#license)                                                                                                       | (BSD) [VTK.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/VTK.txt)                                                                                                                             | Optional                           |
| Xerces            | [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)                                                                                           | (Apache 2) [Xerces-Apache2.0.txt](https://github.com/Chaste/Chaste/blob/develop/docs/licencing/licences/Xerces-Apache2.0.txt)                                                                                              | Source, Cardiac                    |
