This tutorial was generated from the file projects/Angiogenesis/test/python/tutorials/TestPythonBuildVesselNetworkLiteratePaper.py at revision r26879.
Note that the code is given in full at the bottom of the page.



# Introduction
This tutorial is designed to introduce the Python interface for modelling vessel networks. An equivalent C++ tutorial
is [here](https://github.com/Chaste/trac_archive/wiki/Paper-Tutorials-_-Angiogenesis-_-Build-Vessel-Network).

This tutorial covers:

* Building a network from a collection of nodes, segments and vessels
* Writing networks to file and visualizing with Paraview
* Building a network using a network generator
* Reading a network from file


Further functionality is gradually introduced over the course of subsequent tutorials.

# The Test
```

#!python
import unittest
import chaste.core
import chaste.population.vessel as vessel

class TestPythonBuildVesselNetworkLiteratePaper(unittest.TestCase):
```

# Test 1 - Building a vessel network manually, writing it to file and visualizing it
In the first test we will build a vessel network from its constituent components; nodes, segments and vessels. We will do some
simple tests to make sure the network has been formed as expected. Then we write the network to file and visualize it in Paraview.
```

#!python
    def test_BuildNetworkManually(self):
```

First we make some nodes, which are point features from which vessels can be constructed. They are initialized with a location.
All vessel network components are created using special factory methods which return shared pointers, rather than being created
directly through their constructors. Vessel network components are templated over spatial dimension, and can be 2D or 3D. We will
create a Y shaped network. Later we will learn how to build up networks in a more efficient manner.
```

#!python
        length = 100.0
        n1 = vessel.VesselNode(0.0, 0.0 ,0.0)
        n2 = vessel.VesselNode(length, 0.0, 0.0)
        n3 = vessel.VesselNode(2.0 * length, length, 0.0)
        n4 = vessel.VesselNode(2.0 * length, -length, 0.0)
```

Next we make vessel segments and vessels. Vessel segments are straight-line features which contain a vascular node at each end. Vessels
can be constructed from multiple vessel segments, but in this case each vessel just has a single segment.
```

#!python
        v1 = vessel.Vessel([n1 ,n2])
        v2 = vessel.Vessel([n2, n3])
        v3 = vessel.Vessel([n2, n4])
```

Now we can add our vessels to a vessel network.
```

#!python
        network = vessel.VesselNetwork()
        network.AddVessel(v1)
        network.AddVessel(v2)
        network.AddVessel(v3)
```

We use our test framework to make sure that the network has been created correctly by checking the number of vessels and nodes
```

#!python
        self.assertEqual(network.GetNumberOfNodes(), 4)
        self.assertEqual(network.GetNumberOfVessels(), 3)
```

Next we write out network to file. We use the Chaste `OutputFileHandler` functionality to management the output location
Networks are written using VTKs [PolyData](https://github.com/Chaste/trac_archive/wiki/Poly-Data) format, which should have a .vtp extension.
```

#!python
        file_handler = chaste.core.OutputFileHandler("TestPythonBuildVesselNetworkLiteratePaper", True)
        network.Write(file_handler.GetOutputDirectoryFullPath() + "bifurcating_network.vtp")
```

Now we can visualize then network in Paraview. See the tutorial [here](https://github.com/Chaste/trac_archive/wiki/User-Tutorials-_-Visualizing-With-Paraview), to get started. To view the network import the file
`TestPythonBuildVesselNetworkLiteratePaper\bifurcating_network.vtp` into Paraview. For a nicer rendering you can do `Filters->Alphabetical->Tube`.
```

#!python
if __name__ == '__main__':
    unittest.main()


= Code =
The full code is given below


== File name `TestPythonBuildVesselNetworkLiteratePaper.py` ==
```

#!python
import unittest
import chaste.core
import chaste.population.vessel as vessel

class TestPythonBuildVesselNetworkLiteratePaper(unittest.TestCase):
    def test_BuildNetworkManually(self):

        length = 100.0
        n1 = vessel.VesselNode(0.0, 0.0 ,0.0)
        n2 = vessel.VesselNode(length, 0.0, 0.0)
        n3 = vessel.VesselNode(2.0 * length, length, 0.0)
        n4 = vessel.VesselNode(2.0 * length, -length, 0.0)

        v1 = vessel.Vessel([n1 ,n2])
        v2 = vessel.Vessel([n2, n3])
        v3 = vessel.Vessel([n2, n4])

        network = vessel.VesselNetwork()
        network.AddVessel(v1)
        network.AddVessel(v2)
        network.AddVessel(v3)

        self.assertEqual(network.GetNumberOfNodes(), 4)
        self.assertEqual(network.GetNumberOfVessels(), 3)

        file_handler = chaste.core.OutputFileHandler("TestPythonBuildVesselNetworkLiteratePaper", True)
        network.Write(file_handler.GetOutputDirectoryFullPath() + "bifurcating_network.vtp")

if __name__ == '__main__':
    unittest.main()
```


