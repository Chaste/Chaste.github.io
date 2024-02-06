# Setting up dependency versions with environment modules



The Chaste [dependency-modules](https://github.com/Chaste/dependency-modules) repository contains a collection of scripts that can be used for installing multiple versions of Chaste dependencies side-by-side as [Environment Modules](https://modules.readthedocs.io/en/latest/).

Environment Modules enables switching between different versions of installed libraries, which can be useful for testing Chaste with different combinations of dependency versions.

The dependency-modules repository also has a [docker image](https://github.com/Chaste/dependency-modules/blob/main/Dockerfile) that can be used as an isolated environment for testing Chaste with different versions of dependencies during development. The install scripts in the repository can be used with or without the docker image.

## Using Chaste dependency-modules without docker
The [example](https://github.com/Chaste/dependency-modules/blob/main/scripts/example.sh) in the repository provides a demonstration showing how the install scripts can be used:
1. [Install](https://modules.readthedocs.io/en/latest/INSTALL.html) Environment Modules or a similar modules package such as [Lmod](https://lmod.readthedocs.io/en/latest/030_installing.html). <br/>On Ubuntu, this can be done with `sudo apt-get install environment-modules`.

2. Log out and back into the shell to activate the `module` command. <br/>Alternatively, source `.  /etc/profile.d/modules.sh` in the current shell. <br/>If all is well,`module --version` should print out the Environment Modules version.

3. Create the directory where you would like the Chaste software dependency versions to be installed. Within it, create a `modulefiles` sub-directory e.g. `mkdir -p $HOME/modules/modulefiles` will make both directories.

4. Run `module use <base-dir>/modulefiles` to tell Environment Modules where find the dependency versions you are going to install e.g. `module use $HOME/modules/modulefiles`.

5. Get the [install scripts](https://github.com/Chaste/dependency-modules/tree/main/scripts): <br/>`git clone https://github.com/Chaste/dependency-modules.git` <br/>`cd dependency-modules/scripts`

6. To get a printout of options for a script, run the script without any parameters. <br/>For example, running `./install_xercesc.sh` will generate the following output:

```

Usage: install_xercesc.sh --version=version --modules-dir=path [--parallel=value]

```


7. Install specific versions of dependencies using the scripts. For example:

```

./install_xsd.sh --version=4.0.0 --modules-dir=$HOME/modules

./install_xercesc.sh  --version=3.2.3  --modules-dir=$HOME/modules --parallel=4

./install_sundials.sh --version=5.8.0 --modules-dir=$HOME/modules --parallel=4

./install_boost.sh --version=1.74.0 --modules-dir=$HOME/modules --parallel=4

./install_vtk.sh --version=9.1.0 --modules-dir=$HOME/modules --parallel=4

./install_petsc_hdf5.sh \
    --petsc-version=3.11.3 \
    --hdf5-version=1.10.5 \
    --petsc-arch=linux-gnu \
    --modules-dir=$HOME/modules \
    --parallel=4

```

    This will install the specified dependency versions in `$HOME/modules/opt`.<br/>
    Related [modulefiles](https://modules.readthedocs.io/en/latest/modulefile.html) will be placed in `$HOME/modules/modulefiles` for Environment Modules to find.<br/>
    The source code and build directories will be kept in `$HOME/modules/src`, which can be emptied with `rm -rf $HOME/modules/src/*`.

8. Running `module avail` will show a list of installed modules similar to the one below:

```

---------------- /home/username/modules/modulefiles ----------------
boost/1.74.0                              vtk/9.1.0
petsc_hdf5/3.11.3_1.10.5/linux-gnu        xercesc/3.2.3
sundials/5.8.0                            xsd/4.0.0

```


9. To load the modules into the shell environment,

```

module load boost/1.74.0
module load petsc_hdf5/3.11.3_1.10.5/linux-gnu
module load sundials/5.8.0
module load vtk/9.1.0
module load xercesc/3.2.3
module load xsd/4.0.0

```

    To verify that these modules have been loaded, run `module list`.<br/>
    To unload a module run `module unload <modulefile>`, or run `module purge` to unload all modules.

10. To build Chaste with the loaded modules, follow the [install guide](https://chaste.cs.ox.ac.uk/trac/wiki/ChasteGuides/CmakeFirstRun) and modify the "configure" step to:

```

cmake \
  -DBoost_NO_BOOST_CMAKE=ON \
  -DBoost_NO_SYSTEM_PATHS=ON \
  -DBOOST_ROOT=${BOOST_ROOT} \
  -DCMAKE_PREFIX_PATH="${SUNDIALS_ROOT};${VTK_ROOT};${XERCESC_ROOT};${XSD_ROOT}" \
  /path/to/Chaste_source_code

```

  The environment variables `BOOST_ROOT`, `SUNDIALS_ROOT`, `VTK_ROOT`, `XERCESC_ROOT`, and `XSD_ROOT` are automatically set when the relevant modules are loaded. In addition, `PETSC_DIR` and `PETSC_ARCH` are set in the environment to help CMake find the right dependency versions.

## Using Chaste dependency-modules with docker
The docker image has Environment modules pre-installed, along with system versions of Chaste dependencies from the Ubuntu repository. The image also contains  the dependency-modules [install scripts](https://github.com/Chaste/dependency-modules/tree/main/scripts). To use the docker image:

1. Install [Docker Desktop](https://docs.docker.com/desktop/install/linux-install/).

2. Start a docker container using the `chaste/runner` image:

```

docker run -it --init --rm \
--name <container_name> \
--volume <volume_name>:/home/runner \
-e RUNNER_OFF=1 \
chaste/runner:latest

```

    `-it` attaches to an [interactive tty](https://docs.docker.com/engine/reference/run/#foreground) for user input.

    `--init` starts the container with an [init process](https://docs.docker.com/engine/reference/run/#specify-an-init-process) which manages subsequent processes.

    `--rm` performs automatic [clean up](https://docs.docker.com/engine/reference/run/#clean-up---rm) when the container exits.

    `--volume` creates a [docker volume](https://docs.docker.com/storage/volumes/) attached to `/home/runner`. Data stored here will persist after the container exits. The data can be accessed on the next run by re-attaching the same volume.

    `-e RUNNER_OFF=1` sets an environment variable that directs the container to open an interactive bash [login shell](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html) instead of starting a github runner. Login shells automatically enable the `module` command by sourcing `/etc/profile.d/modules.sh` on startup.

3. Follow the steps in the "without docker" [section above](https://chaste.cs.ox.ac.uk/trac/wiki/ChasteGuides/ModulesSetupGuide#UsingChastedependency-moduleswithoutdocker) to install specific dependency versions and build Chaste. <br/>As the Environment Modules package is already installed in the container, the steps for installing it can be skipped. <br/>The dependency installation scripts are also available on the `PATH` in the container and can be launched  directly e.g. <br/>`install_xsd.sh --version=4.0.0 --modules-dir=/home/runner/modules `

4. VS Code can be attached to the docker container by installing the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension and following the [official instructions](https://code.visualstudio.com/docs/remote/attach-container) for attaching to a running container.
