---
title : "Ubuntu package"
description: "Installing Chaste using the Ubuntu package"
lead: "Installing Chaste using the Ubuntu package"
date: 2020-10-06T08:47:36+00:00
lastmod: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
---

For Ubuntu users, there is a package available to greatly ease the installation of Chaste.
It requires an Ubuntu version of Intrepid or newer, as several dependencies are not available as Ubuntu packages in older versions.
We have also had success installing Chaste on a virtual machine running Ubuntu in other versions of Linux, macOS and Windows.

The package has been tested with all versions of Ubuntu from **Intrepid (8.10)** to **Jammy (22.04)** inclusive, and will be adapted to new versions as soon as possible after they are released.

Each release of Chaste should work with [all supported versions of Ubuntu](http://www.ubuntu.com/info/release-end-of-life) at the time of the Chaste release. But note that the latest Chaste releases won't work with the oldest (unsupported) Ubuntus, and the older Chaste releases (and their associated bolt-on projects) probably won't work with the newest Ubuntus without some updating (to use newer dependencies and compilers). The development code should always work with all the currently supported versions of Ubuntu.

## 1. Accessing the Chaste Package

The package can be downloaded using your package manager (e.g. [apt](https://ubuntu.com/server/docs/package-management)) by adding our repository to your configuration.
This can be done by, for example, opening a terminal and running

```
sudo nano /etc/apt/sources.list.d/chaste.list
```

and, depending on your version of Ubuntu, add **one** of the following lines to the `chaste.list` text file:

| **Ubuntu Version** | **Ubuntu codename** | **Line to add** |
|---|---|---|
| 13.10 or older | - | `deb http://www.cs.ox.ac.uk/chaste/ubuntu legacy/` |
| 14.04 LTS | trusty | `deb http://www.cs.ox.ac.uk/chaste/ubuntu trusty/` |
| 14.10 | utopic | `deb http://www.cs.ox.ac.uk/chaste/ubuntu utopic/` |
| 15.04 | vivid | `deb http://www.cs.ox.ac.uk/chaste/ubuntu vivid/` |
| 15.10 | wily | `deb http://www.cs.ox.ac.uk/chaste/ubuntu wily/` |
| 16.04 LTS | xenial | `deb http://www.cs.ox.ac.uk/chaste/ubuntu xenial/` |
| 16.10 | yakkety | `deb http://www.cs.ox.ac.uk/chaste/ubuntu yakkety/` |
| 17.04 | zesty | `deb http://www.cs.ox.ac.uk/chaste/ubuntu zesty/` |
| 17.10 | artful | `deb http://www.cs.ox.ac.uk/chaste/ubuntu artful/` |
| 18.04 LTS | bionic | `deb http://www.cs.ox.ac.uk/chaste/ubuntu bionic/` |
| 18.10 | cosmic | `deb http://www.cs.ox.ac.uk/chaste/ubuntu cosmic/` |
| 19.04 | disco | `deb http://www.cs.ox.ac.uk/chaste/ubuntu disco/` |
| 19.10 | eoan | `deb http://www.cs.ox.ac.uk/chaste/ubuntu eoan/` |
| 20.04 LTS | focal | `deb http://www.cs.ox.ac.uk/chaste/ubuntu focal/` |
| 20.10 | groovy | `deb http://www.cs.ox.ac.uk/chaste/ubuntu groovy/` |
| 21.04 | hirsute | `deb http://www.cs.ox.ac.uk/chaste/ubuntu hirsute/` |
| 21.10 | impish | `deb http://www.cs.ox.ac.uk/chaste/ubuntu impish/` |
| 22.04 LTS | jammy | `deb [signed-by=/usr/share/keyrings/chaste.asc] http://www.cs.ox.ac.uk/chaste/ubuntu jammy/` |


The last component of the line depends on your version of Ubuntu, as listed at https://wiki.ubuntu.com/DevelopmentCodeNames. Type `lsb_release -a` to find this out if you don't already know it.
Note that the trailing "/" is necessary!

Next, install the Chaste public licence key.
Back in the terminal, type:

```
OLD:
sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 422C4D99

NEW:
sudo wget -O /usr/share/keyrings/chaste.asc https://www.cs.ox.ac.uk/chaste/ubuntu/Chaste%20Team.asc
```

Note that you also need to ensure you have enabled 'multiverse' packages; this is normally the default.

## 2. Getting the correct dependencies

After following point 1 above, you should be able to install the dependencies for Chaste by running:

```
sudo apt update
sudo apt install chaste-dependencies
```

You should now decide whether you want to be a Code User or a Code Developer.

* Code Users - are people who want to work with a stable released version of the Chaste code (a new release is made roughly every six months).
* Code Developers - (both internal and external to the core team) are people who want to work with the latest development version of the Chaste code, between the main stable releases.

See [GettingStarted](https://github.com/Chaste/trac_archive/wiki/Getting-Started) for more detail if you still aren't sure.


### 2a. For Code USERS (working with a release, rather than developers)

You can obtain the latest stable release of the Chaste source code from our GitHub repository:

```
git clone --recursive -b release https://chaste.cs.ox.ac.uk/git/chaste.git Chaste
```

Finally, follow the [CMake First Run](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Cmake-First-Run) guide to get up and running with Chaste.


#### Installing previous releases

If you want a specific version of Chaste, and do not want to stay up-to-date with new versions on the `release` branch from our Git repository, you can download the source code from [[https://github.com/Chaste/Chaste/releases|our [GitHub](https://github.com/Chaste/trac_archive/wiki/Git-Hub) releases page]], back to Release 3.0.

### 2b. For Code DEVELOPERS (or users working with the latest trunk code and projects)

To install the suggested packages:

```
sudo apt update
sudo apt install --install-recommends chaste-dependencies
sudo apt install `dpkg -s chaste-dependencies | egrep "^Suggests" | cut -d "," -f 1-111 --output-delimiter " " | cut -d ":" -f 2`
```

If you want to use eclipse to work with Chaste (as we do - recommended), after the above you will then need to:

* [clone the Chaste repository](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Access-Code-Repository).
* [SetupEclipse](https://github.com/Chaste/trac_archive/wiki/Setup-Eclipse) - update eclipse settings to use Chaste code formatting etc.

If you don't want to use eclipse you can [checkout at the command line](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-Access-Code-Repository).
You can get information on the latest stable build on the [external developer guide page](https://github.com/Chaste/trac_archive/wiki/Chaste-Guides-_-External-Developer-Guide).

If you have the necessary permissions, see also [Check out a user project](https://github.com/Chaste/trac_archive/wiki/Install-Guides-_-Checkout-User-Project) - to make a new user project, or get a copy of an existing one.

#### Manual adjustments

You can choose different blas/lapack implementations. Look particularly at the atlas packages, (`apt-cache search libatlas` to see the options).  Use `libatlas-sse2-dev` on Intel, `libatlas-3dnow-dev` on AMD, `libatlas-base-dev` otherwise.
