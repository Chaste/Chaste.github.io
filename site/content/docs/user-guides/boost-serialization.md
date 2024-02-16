---
title: "Implementing Checkpointing for Classes with Boost Serialization"
description: "Implementing Checkpointing for Classes with Boost Serialization"
draft: false
images: []
toc: true
layout: "single"
---

In order to checkpoint and save/resume simulations, we use the
[Serialization](http://www.boost.org/libs/serialization/doc/index.html) library
from [Boost](http://www.boost.org/). This page contains some notes on how to use
this functionality well in Chaste.

{{< callout context="tip" title="See Also" icon="rocket" >}}

[Full Boost Serialization Documentation](http://www.boost.org/libs/serialization/doc/index.html)

{{< /callout >}}

## Header files

One important point to note is that **only** code which needs to **create**
archive objects should include the `*archive.hpp` headers. This allows the
serialization code in our classes to be (largely) independent of the type of
archive being written to/read from.

All header files of the form `<boost/archive/*archive.hpp>` are **required** to
precede the header file `<boost/serialization/export.hpp>`.

It is good practice therefore for tests of archiving to include first

```c++
#include "CheckpointArchiveTypes.hpp"
```

and then include Chaste classes. See [Derived Classes](#derived-classes) below
for details on how to use the export header.

The main header file that classes with serialization methods will need is

```c++
#include "ChasteSerialization.hpp"
```

Other headers are also needed for dealing with abstract and derived classes; see
[Class Hierarchies](#class-hierarchies) below.

For serializing vectors, add

```c++
#include <boost/serialization/vector.hpp>
```

Similar headers exist for other STL collections.

There are cases where Chaste code needs to create archives, for example to
provide `Save` and `Load` functionality for tissue simulations, or heart
simulation checkpointing. The easiest way to handle this is to create a separate
helper class (in its own source files) which does this. For examples see
[`cell_based/src/simulation/CellBasedSimulationArchiver.hpp`](https://github.com/Chaste/Chaste/blob/develop/cell_based/src/simulation/CellBasedSimulationArchiver.hpp)
and
[`heart/src/problem/CardiacSimulationArchiver.hpp`](https://github.com/Chaste/Chaste/blob/develop/heart/src/problem/CardiacSimulationArchiver.hpp).
This source file then needs to be included before any other Chaste headers (that
might include serialization headers).

Trying to have `Save` and `Load` functionality in different places will almost
certainly lead to problems such as:

```
heart/build/debug/src/problem/AbstractCardiacProblem.o:
    multiple definition of `boost::archive::detail::guid_initializer<SimpleStimulus>::instance'
heart/build/debug/bidomain/TestBidomainArchiveKSPRunner.o:
    first defined here
```

The cause of this is multiple definitions of the unique IDs needed to properly
serialize derived classes through a pointer (see below). If multiple .cpp files
include both an archive header (`<boost/archive/*archive.hpp>`) and
`<boost/serialization/export.hpp>`, either directly or indirectly, then each
corresponding object file (or library) will define the same unique ID, hence the
error. It is OK to have archive headers in multiple files, provided that the
export header follows in at most one case of files being linked together.

## Class hierarchies

Some extra work is needed to deal properly with serializing objects from a class
hierarchy.

### Abstract classes

While many compilers can automatically detect abstract classes, some do not, and
so need them to be indicated explicitly. Since the interface for doing this
changed in Boost 1.36, we have written a wrapper interface in
[`global/src/checkpointing/ClassIsAbstract.hpp`](https://github.com/Chaste/Chaste/blob/develop/global/src/checkpointing/ClassIsAbstract.hpp).
When writing an abstract base class (i.e. one with pure virtual methods),
include this header (`#include "ClassIsAbstract.hpp"`) and use the macro

```c++
CLASS_IS_ABSTRACT(class_name)
```

after the class definition, to indicate to the serialization library that it
should not try to instantiate the class, thus avoiding compiler errors on some
systems.

{{< callout context="caution" title="Caution" icon="alert-triangle" >}}

This macro should **_only_** be used for classes with **_pure virtual_**
methods. If they only have virtual methods with implementations, then the class
can actually be instantiated, and the macro should not be used. Including the
macro unnecessarily can lead to segfaults!

{{< /callout >}}

If the abstract class is templated, the above macro will not work. There are
convenience macros for common scenarios, or you may have to expand the
underlying definition manually. See
[`global/src/checkpointing/ClassIsAbstract.hpp`](https://github.com/Chaste/Chaste/blob/develop/global/src/checkpointing/ClassIsAbstract.hpp)
for details.

### Derived classes

Derived classes must make sure to serialize their base parts, by including
`<boost/serialization/base_object.hpp>` and using

```c++
archive & boost::serialization::base_object<base_class_name>(*this);
```

as the first instruction in their `serialize` method. See the
[Boost documentation](http://www.boost.org/libs/serialization/doc/serialization.html#base).

If serializing a derived class through a base class pointer or reference, the
library will need some help to know which class to instantiate when loading from
the archive. This is done by defining a globally unique identifier for the class
using the `BOOST_CLASS_EXPORT` macro from `<boost/serialization/export.hpp>`.
Due to changes in this macro between Boost versions, we provide wrapper macros
in
[`global/src/checkpointing/SerializationExportWrapper.hpp`](https://github.com/Chaste/Chaste/blob/develop/global/src/checkpointing/SerializationExportWrapper.hpp)
and
[`global/src/checkpointing/SerializationExportWrapperForCpp.hpp`](https://github.com/Chaste/Chaste/blob/develop/global/src/checkpointing/SerializationExportWrapperForCpp.hpp).

Chaste header files that declare derived classes should include something like
the following _after_ the class block in the .hpp file:

```c++
#include "SerializationExportWrapper.hpp"
CHASTE_CLASS_EXPORT(class_name)
```

The corresponding .cpp file must include something like the following after any
other includes (you can put it at the end of the file for consistency):

```c++
#include "SerializationExportWrapperForCpp.hpp"
CHASTE_CLASS_EXPORT(class_name)
```

Note that the name given to `CHASTE_CLASS_EXPORT` **must** match that used in
the .hpp file.

{{< callout context="note" title="Note" icon="info-circle" >}}

This macro is **not** needed for **abstract** base classes, only in
derived classes, since no instances of the base itself will be serialized.

For further information, see the Boost documentation:
- [Exporting Class Serialization](http://www.boost.org/libs/serialization/doc/special.html#export)
- [Pointers to Objects of Derived Classes](http://www.boost.org/libs/serialization/doc/serialization.html#derivedpointers)

{{< /callout >}}

With templated classes, this simple invocation doesn't work. A fully general
export macro approach
[seems impossible](http://lists.boost.org/boost-users/2005/05/11731.php). The
header [`global/src/checkpointing/SerializationExportWrapper.hpp`](https://github.com/Chaste/Chaste/blob/develop/global/src/checkpointing/SerializationExportWrapperForCpp.hpp)
provides macros for where a derived class is templated over dimension (either a
single dimension, or both element and space dimension, or including
`PROBLEM_DIM`). See [`mesh/src/common/TetrahedralMesh.hpp`](https://github.com/Chaste/Chaste/blob/develop/mesh/src/common/TetrahedralMesh.hpp) for an example of its use.

## Avoiding the need for special constructors

It is undesirable to have to write a special constructor for classes just for
the use of the archiving code. There are two ways around this.

One is to write separate functions `save_construct_data` and
`load_construct_data` for the class. These save or load the parameters needed
for an existing constructor. See
[`cell_based/src/cell/Cell.hpp`](https://github.com/Chaste/Chaste/blob/develop/cell_based/src/cell/Cell.hpp)
for an example. See also
[Non-Default Constructors](http://www.boost.org/libs/serialization/doc/serialization.html#constructors),
in the official Boost documentation.

Note that the example in the documentation seems to suggest that you can
directly access private member data from a `save_construct_data` function. This
is incorrect. You'll either need public accessor methods for the data you
require, or a public helper method to save the data to the archive.

The other method is to create a _private default constructor_ which does
nothing, as is done in [`heart/src/problem/Electrodes.hpp`](https://github.com/Chaste/Chaste/blob/develop/heart/src/problem/Electrodes.hpp). All the
work can then be done by the `serialize` method.

## Singleton classes

In order for singleton classes to remain singletons, they must be serialized
properly. The
[`SerializableSingleton`](https://github.com/Chaste/Chaste/blob/develop/global/src/checkpointing/SerializableSingleton.hpp)
class makes doing so easier, without requiring any special handling for the
first serialization of a singleton. Any singleton class which needs to be
serialized should inherit from this base, which provides both part of the
"singleton-ness" (by inheriting from `boost::noncopyable`), and also a method
`GetSerializationWrapper()`. Users of the singleton which wish to serialize it
should not do so directly. Instead, they should call `GetSerializationWrapper()`
and serialize the returned pointer. Doing so will ensure that only a single
global instance of the singleton is maintained when loading from an archive. For
more information see the
[documentation for SerializableSingleton](../../../doxygen-latest/classSerializableSingleton.html).

It is also advisable for singleton classes to `assert(mpInstance==NULL)` in
their constructor, in order to trap cases where serialization has not been
performed correctly.

## Loading archives created by older Chaste versions

As Chaste evolves, classes gain new data members, or members change, disappear,
etc. However, ideally each release of Chaste should still be able to load
checkpoints created by the previous release. In some cases this may not be
possible, e.g. a new object added that doesn't have a sensible default. However,
in cases where it is possible, Boost provides the functionality to handle this,
via the `version` parameter passed to serialization methods.

For each class in which the serialization changes, include the header
`ChasteSerializationVersion.hpp`. Within your serialize method, test the
`version` parameter and act accordingly. Finally, use the macro

```c++
BOOST_CLASS_VERSION(ClassName, VersionNumber)
```

after your class definition to specify the current version number -- increase it
by 1 each time there is a change in how the class is archived (it defaults to 0
if the macro is not given).

See [`heart/src/odes/AbstractCardiacCell.hpp`](https://github.com/Chaste/Chaste/blob/develop/heart/src/odes/AbstractCardiacCell.hpp) and the
[Boost Serialization tutorial](http://www.boost.org/doc/libs/1_37_0/libs/serialization/doc/tutorial.html#versioning)
for examples.

For templated classes, the macro will not work, and you have to expand its
definition yourself (See the Boost documentation on
[Class Serialization Traits](http://www.boost.org/doc/libs/1_37_0/libs/serialization/doc/traits.html#version)).
For example,

```c++
namespace boost {
namespace serialization {
/**
 * Specify a version number for archive backwards compatibility.
 *
 * This is how to do BOOST_CLASS_VERSION(AbstractCardiacPde, 1)
 * with a templated class.
 */
template <unsigned ELEMENT_DIM, unsigned SPACE_DIM>
struct version<AbstractCardiacPde<ELEMENT_DIM, SPACE_DIM> >
{
    CHASTE_VERSION_CONTENT(1);
};
} // namespace serialization
} // namespace boost
```

## Testing the archiving

- Always archive via a pointer (well, almost always).
- Always archive pretending it is the most abstract class possible (this tests that boost is registering classes properly - otherwise your `EXPORT` commands aren't tested).
- Write a test for each concrete class that can be archived, checking their unique methods and variables are archived properly.

A good way to test the archiving is along the following lines:

```c++
#include "CheckpointArchiveTypes.hpp"
#include "ArchiveLocationInfo.hpp"

void TestArchivingOfConcreteClass() throw(Exception)
{
    OutputFileHandler handler("archive", false);
    // The next two lines ensure that different processes read/write different archive files when running in parallel
    ArchiveLocationInfo::SetArchiveDirectory(handler.FindFile(""));
    std::string archive_filename = ArchiveLocationInfo::GetProcessUniqueFilePath("ConcreteClass.arch");

    // Create data structures to store variables to test for equality here

    // Save
    {
        AbstractClass* const p_abstract_class = new ConcreteClass();

        // Create an output file
        std::ofstream ofs(archive_filename.c_str());
        // And create a boost output archive that goes to this file
        boost::archive::text_oarchive output_arch(ofs);

        // Record values to test into data structures
        // If necessary you can use static_cast<ConcreteClass*>(p_abstract_class)
        // (if your abstract class doesn't contain the necessary variables and methods)

        output_arch << p_abstract_class;
        delete p_abstract_class;
    }

    // Load
    {
        AbstractClass* p_abstract_class_2;

        // Read from this input file
        std::ifstream ifs(archive_filename.c_str(), std::ios::binary);
        // And choose a boost input_archive object to translate this file
        boost::archive::text_iarchive input_arch(ifs);

        // restore from the archive
        input_arch >> p_abstract_class_2;

        // Check things in the data structures with TS_ASSERTS here.
        // If necessary you can use static_cast<ConcreteClass*>(p_abstract_class_2)
        // (if your abstract class doesn't contain the necessary variables and methods)

        delete p_abstract_class_2;
    }
}
```

Note that all archive files in the repository should be generated using the
oldest Boost version supported by Chaste to ensure compatibility with all of the
possible
[Boost versions supported by Chaste](../../installguides/dependency-versions).
You can generate these from the Chaste build directory by doing:

```sh
cmake --build . --target TestGenerateSteadyStateCrypt
ctest -R TestGenerateSteadyStateCrypt$
```

## Parallel archiving

When checkpointing a parallel simulation, there are two kinds of data that need
to be saved: replicated (same for every process) and distributed (different on
each process). We wish to write these to separate locations, so that the
replicated data is only written to disk once, and to make it easier to re-load
on a different number of processes (in which case the distributed data will need
to be re-distributed). However, the Boost Serialization library expects to be
writing to just one archive.

Two classes are provided to solve this problem:
[ProcessSpecificArchive](https://github.com/Chaste/Chaste/blob/develop/global/src/checkpointing/ProcessSpecificArchive.hpp)
and
[ArchiveOpener](https://github.com/Chaste/Chaste/blob/develop/global/src/checkpointing/ArchiveOpener.hpp).
The latter is for opening archives for reading or writing. All that all a user
needs to do is create an instance of this class, call `GetCommonArchive`, and
read from/write to the returned archive. When done, just destroy the instance
(e.g. by closing the scope).

The
[ProcessSpecificArchive](https://github.com/Chaste/Chaste/blob/develop/global/src/checkpointing/ProcessSpecificArchive.hpp)
class is for use by classes that need to save distributed data, and provides
access to a secondary archive in which to store it. When opening an archive in a
(potentially) parallel setting, using either the
[ArchiveOpener](https://github.com/Chaste/Chaste/blob/develop/global/src/checkpointing/ArchiveOpener.hpp)
or
[CardiacSimulationArchiver](https://github.com/Chaste/Chaste/blob/develop/heart/src/problem/CardiacSimulationArchiver.hpp),
the `Set` method will be called to specify the secondary archive. Classes which
need to save distributed data can then use the `Get` method to access and write
to/read from this archive.

Some classes (e.g. the meshes, `LinearSystem`, and `HeartConfig`) don't write
their data directly to the archive file, but instead write to separate files in
the same folder. They use the
[ArchiveLocationInfo](https://github.com/Chaste/Chaste/blob/develop/global/src/checkpointing/ArchiveLocationInfo.hpp)
class to find out where to write to.

### Cardiac simulations

The `CardiacSimulationArchiver` class provides a high-level interface to
checkpointing of cardiac simulations, and orchestrates the logic for
re-distributing data when loading on a different number of processes. The logic
is currently quite difficult to follow, and so this is an attempt to document the
main points.

In order to support SVI, and potentially other applications which require
loading halo information, all process-specific archives are read by all
processes when loading from a checkpoint. The only difference between the
migration case (when loading on a different number of processes from that which
saved the checkpoint) and the 'normal' case is which process-specific archive is
loaded first. If the number of processes matches, each process loads its own
process-specific archive while reading the common archive, so that the mesh can
maintain the same partitioning. When migrating, each process reads the process-0
archive first, since it is guaranteed to exist.
`AbstractCardiacProblem::LoadExtraArchive` is then called with each additional
process-specific archive.

When a `DistributedVectorFactory` is loaded from any process-specific archive,
then the `DistributedVectorFactory` `load_construct_data` will set
`mpOriginalFactory` to contain the version in the archive (i.e. using its
`lo, hi, size, num_procs`), and the object created will partition based on
PETSc's default for a `Vec` with problem size
`mpOriginalFactory->GetProblemSize()`. `CardiacSimulationArchiver` also calls
`DistributedVectorFactory::SetCheckNumberOfProcessesOnLoad(false)` to prevent
`load_construct_data` setting the local size as `hi-lo`, since these will not
always add up to the problem size when loading different process-specific
archives.

`AbstractTetrahedralMesh::load` makes use of the original factory, if present,
to partition the loaded mesh. (`AbstractMesh::serialize` checkpoints the mesh's
`DistributedVectorFactory` to the process-specific archive. This may be `NULL` in
some cases (when we're not a `DistributedTetrahedralMesh`?).) It unsets the
member variable temporarily, saving it to `p_factory`, and sets `p_our_factory`
to the original factory or `NULL`. If there is an original factory and the number
of processes matches, then `SetDistributedVectorFactory` is called to force use
of the same partition as before; otherwise `p_our_factory` is set to `NULL` to
allow repartitioning. We then `ConstructFromMeshReader`. Finally,
`mpDistributedVectorFactory` needs to be changed to point to `p_factory` so all
objects use the same factory, and `p_factory` updated if it exists and we
repartitioned using
`p_factory->SetFromFactory(this->mpDistributedVectorFactory)` (which clears
`mGlobalLows` and sets `mLo` and `mHi`).

## Other notes

### Using binary archives

Binary archives are faster to save and load, and take less disk space. The
disadvantages are that they become machine/architecture specific, and you can't
just look in the file to see what's changed, or check class names are exported
correctly. But if you are implementing archiving for a personal / science
project it can be worth using them. The `src` implementation is unchanged, the
tests that write/read the archives just need to use:

```c++
boost::archive::binary_iarchive
boost::archive::binary_oarchive
```

instead of

```c++
boost::archive::text_iarchive
boost::archive::text_oarchive
```

in all of the above example code. This can speed things up considerably, and
also reduce archive file sizes. It's easy to simply load an ASCII archive and
re-save in binary, or vice-versa, if you need to.

### Compressing the archive

Note that archive compression needs `libboost_iostreams` adding to the library
paths on compilation. You can find the line in `CMakeLists.txt` that looks like

```cmake
find_package(Boost COMPONENTS filesystem system serialization program_options REQUIRED)
```

and add `iostreams` to the list.

The standard way of using archives now becomes a bit more complicated with an
intermediate stream buffer that takes care of translating between boost
archiving and the raw filestream. The below code is an altered version of the
above standard test/use of archiving.

```c++
#include "CheckpointArchiveTypes.hpp"

// For compressing output
#include <boost/iostreams/filtering_stream.hpp>
#include <boost/iostreams/filter/zlib.hpp>

void TestArchivingOfConcreteClass() throw(Exception)
{
    OutputFileHandler handler("archive",false);
    std::string archive_filename = handler.GetOutputDirectoryFullPath() + "ConcreteClass.arch";

    // Create data structures to store variables to test for equality here

    {
        AbstractClass* const p_abstract_class = new ConcreteClass();

        // Create an output file
        std::ofstream ofs(archive_filename.c_str());

        // But instead of boost archive directly using this, pass boost archive
        // to a new boost filtered_ostream, and add a compressor to the filtered_ostream.
        boost::iostreams::filtering_ostream out;
        boost::iostreams::zlib_params zp(boost::iostreams::zlib::best_speed);
        out.push(boost::iostreams::zlib_compressor(zp));
        out.push(ofs);

        // As normal, but boost archive goes via the filtering_ostream instead of directly to the ostream.
        boost::archive::text_oarchive output_arch(out);

        // Record values to test into data structures
        // If necessary you can use static_cast<ConcreteClass*>(p_abstract_class)
        // (if your abstract class doesn't contain the necessary variables and methods)

        output_arch << p_abstract_class;
        delete p_abstract_class;
    }

    {
        AbstractClass* p_abstract_class_2;

        // Read from this input archive
        std::ifstream ifs(archive_filename.c_str(), std::ios::binary);

        // Set up the compressed reader filtering stream
        boost::iostreams::filtering_istream in;
        boost::iostreams::zlib_params zp(boost::iostreams::zlib::best_speed);
        in.push(boost::iostreams::zlib_decompressor(zp));
        in.push(ifs);

        // Copy boost archive input stream reads via the filtered stream, which does uncompression.
        boost::archive::text_iarchive input_arch(in);

        // restore from the archive
        input_arch >> p_abstract_class_2;

        // Check things in the data structures with TS_ASSERTS here.
        // If necessary you can use static_cast<ConcreteClass*>(p_abstract_class_2)
        // (if your abstract class doesn't contain the necessary variables and methods)

        delete p_abstract_class_2;
    }
}
```
