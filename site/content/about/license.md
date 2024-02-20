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
<dl>
<dt>Distributed:</dt><dd> source code that is distributed with the Chaste source</dd>
<dt>Source:</dt><dd> required for building Chaste from source</dd>
<dt>Tests:</dt><dd> only required for testing Chaste</dd>
<dt>Cardiac:</dt><dd> only really needed if you're building the cardiac-specific source</dd>
<dt>Optional:</dt><dd> may be used by Chaste if installed, but not essential</dd>
</dl>

<table border="1">
<tr>
  <th> Library/package </th>
  <th> Licence URL </th>
  <th> Local copy of licence </th>
  <th> Used by </th>
</tr>

<tr>
  <td> Boost </td>
  <td> <a href="http://www.boost.org/users/license.html">http://www.boost.org/users/license.html</a> </td>
  <td> <a href="licences/Boost.txt"> Boost.txt </a> </td>
  <td> Source </td>
</tr>

<tr>
  <td> CodeSynthesis XSD </td>
  <td> <a href="http://www.codesynthesis.com/products/xsd/license.xhtml">http://www.codesynthesis.com/products/xsd/license.xhtml</a>,
       <a href="http://www.codesynthesis.com/projects/xsd/FLOSSE">http://www.codesynthesis.com/projects/xsd/FLOSSE</a> </td>
  <td> (GPL) <a href="licences/CodeSynthesis_Exception.txt">CodeSynthesis_Exception.txt</a> </td>
  <td> Source, Cardiac </td>
</tr>

<tr>
  <td>CVODE (part of SUNDIALS)</td>
  <td><a href="https://computing.llnl.gov/projects/sundials/license">https://computing.llnl.gov/projects/sundials/license</a></td>
  <td> (BSD) <a href="licences/CVODE.txt">CVODE.txt</a></td>
  <td> Optional </td>
</tr>

<tr>
  <td> CxxTest </td>
  <td> LGPL: <a href="http://www.gnu.org/copyleft/lesser.html">http://www.gnu.org/copyleft/lesser.html</a> </td>
  <td>(LGPL) <a href="licences/CxxTest.txt">CxxTest.txt</a> </td>
  <td> Tests, Distributed </td>
</tr>

<tr>
  <td> HDF5 </td>
  <td> <a href="http://www.hdfgroup.org/products/licenses.html">http://www.hdfgroup.org/products/licenses.html</a> </td>
  <td> <a href="licences/HDF5.txt"> HDF5.txt </a> </td>
  <td> Source </td>
</tr>

<tr>
  <td> (Par)METIS </td>
  <td> <a href="http://glaros.dtc.umn.edu/gkhome/metis/metis/faq?q=metis/metis/faq#distribute">http://glaros.dtc.umn.edu/gkhome/metis/metis/faq?q=metis/metis/faq#distribute</a> </td>
  <td><a href="licences/METIS.txt"> METIS.txt</a>,
      <a href="licences/METIS_manual.pdf"> METIS manual </a></td>
  <td> Source </td>
</tr>

<tr>
  <td> MPICH </td>
  <td> <a href="https://github.com/pmodels/mpich/blob/main/COPYRIGHT">https://github.com/pmodels/mpich/blob/main/COPYRIGHT</a>,
       <a href="http://www.mcs.anl.gov/research/projects/mpi/mpich1/romio-license.txt">http://www.mcs.anl.gov/research/projects/mpi/mpich1/romio-license.txt</a> </td>
  <td><a href="licences/mpich-license.txt">mpich-license.txt</a>
      <a href="licences/romio-license.txt">romio-license.txt</a></td>
  <td> Source (although note that other MPI implementations may be used instead, e.g. OpenMPI) </td>
</tr>

<tr>
  <td> PETSc </td>
  <td><a href="http://www.mcs.anl.gov/petsc/petsc-as/documentation/copyright.html">http://www.mcs.anl.gov/petsc/petsc-as/documentation/copyright.html</a></td>
  <td><a href="licences/PETSc.html">PETSc.html</a> </td>
  <td> Source </td>
</tr>

<tr>
  <td>Pyparsing</td>
  <td><a href="https://pypi.org/project/pyparsing/">Pyparsing home page</a></td>
  <td> (MIT) <a href="licences/pyparsing.txt">pyparsing.txt</a></td>
  <td> Source, Cardiac, Distributed </td>
</tr>

<tr>
  <td> RDFLib </td>
  <td><a href="http://code.google.com/p/rdflib/source/browse/LICENSE">http://code.google.com/p/rdflib/source/browse/LICENSE</a></td>
  <td> (BSD) <a href="licences/RDFLib.txt">RDFLib.txt</a></td>
  <td> Source, Cardiac </td>
</tr>

<tr>
  <td> RNV </td>
  <td><a href="http://ftp.davidashen.net/PreTI/RNV/license.txt">http://ftp.davidashen.net/PreTI/RNV/license.txt</a></td>
  <td> (BSD) <a href="licences/rnv.txt">rnv.txt</a></td>
  <td> Source, Cardiac </td>
</tr>

<tr>
  <td> TetGen </td>
  <td><a href="http://tetgen.berlios.de/">http://tetgen.berlios.de/</a></td>
  <td><a href="https://github.com/Chaste/Chaste/blob/develop/mesh/src/3rdparty/tetgen1.4.2/LICENSE">TetGen</a></td>
  <td> Source, Distributed </td>
</tr>

<tr>
  <td> triangle </td>
  <td><a href="http://www.cs.cmu.edu/~quake/triangle.html">http://www.cs.cmu.edu/~quake/triangle.html</a></td>
  <td><a href="licences/Triangle.txt">Triangle.txt</a></td>
  <td> Source, Distributed </td>
</tr>

<tr>
  <td> VTK </td>
  <td> <a href="http://www.vtk.org/VTK/project/license.html">http://www.vtk.org/VTK/project/license.html</a></td>
  <td> (BSD) <a href="licences/VTK.txt">VTK.txt</a> </td>
  <td> Optional </td>
</tr>

<tr>
  <td> Xerces </td>
  <td><a href="http://www.apache.org/licenses/LICENSE-2.0.html">http://www.apache.org/licenses/LICENSE-2.0.html</a></td>
  <td> (Apache 2) <a href="licences/Xerces-Apache2.0.txt">Xerces-Apache2.0.txt</a></td>
  <td> Source, Cardiac </td>
</tr>

</table>
