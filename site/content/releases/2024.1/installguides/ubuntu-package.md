---
title : "Ubuntu package"
description: "Installing Chaste using the Ubuntu package"
lead: "Installing Chaste using the Ubuntu package"
date: 2020-10-06T08:47:36+00:00
lastmod: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
version: "2024.1"
---

For Ubuntu users, there is a package available to greatly ease the installation of Chaste.
It requires an Ubuntu version of Focal (20.04) or newer.
Chaste can also be run on other versions of Linix, macOS and Windows using [Docker](../docker/).

The package has been tested with all versions of Ubuntu from **Intrepid (8.10)** to **Jammy (22.04)** inclusive, and will be adapted to new versions as soon as possible after they are released.

Each release of Chaste should work with [all supported versions of Ubuntu](http://www.ubuntu.com/info/release-end-of-life) at the time of the Chaste release. But note that the latest Chaste releases won't work with the oldest (unsupported) Ubuntus, and the older Chaste releases (and their associated bolt-on projects) probably won't work with the newest Ubuntus without some updating (to use newer dependencies and compilers). The development code should always work with all the currently supported versions of Ubuntu.

## 1. Accessing the Chaste Package

The package can be downloaded using your package manager (e.g. [apt](https://ubuntu.com/server/docs/package-management)) by adding our repository to your configuration.
This can be done by, for example, opening a terminal and running

```
sudo nano /etc/apt/sources.list.d/chaste.list
```

and, depending on your version of Ubuntu, add **one** of the following lines to the `chaste.list` text file:

{{< details "Ubuntu 22.04 LTS" open >}}
```
deb [signed-by=/usr/share/keyrings/chaste.asc] https://chaste.github.io/ubuntu jammy/
```
{{< /details >}}

{{< details "Ubuntu 21.10" >}}
```
deb [signed-by=/usr/share/keyrings/chaste.asc] https://chaste.github.io/ubuntu hirsute/
```
{{< /details >}}

{{< details "Ubuntu 21.04" >}}
```
deb [signed-by=/usr/share/keyrings/chaste.asc] https://chaste.github.io/ubuntu impish/
```
{{< /details >}}

{{< details "Ubuntu 20.10" >}}
```
deb [signed-by=/usr/share/keyrings/chaste.asc] https://chaste.github.io/ubuntu groovy/
```
{{< /details >}}

{{< details "Ubuntu 20.04 LTS" >}}
```
deb [signed-by=/usr/share/keyrings/chaste.asc] https://chaste.github.io/ubuntu focal/
```
{{< /details >}}

The last component of the line depends on your version of Ubuntu, as listed at https://wiki.ubuntu.com/DevelopmentCodeNames.
Type `lsb_release -a` to find this out if you don't already know it.
Note that the trailing "/" is necessary!

Next, install the Chaste public licence key.
Back in the terminal, type:
```
sudo wget -O /usr/share/keyrings/chaste.asc https://chaste.github.io/chaste.asc
```

## 2. Getting the correct dependencies

After following point 1 above, you should be able to install the dependencies for Chaste by running:

```
sudo apt update
sudo apt install chaste-dependencies
```

You should now decide whether you want to be a Code User or a Code Developer.

* Code Users - are people who want to work with a stable released version of the Chaste code (a new release is made roughly every six months).
* Code Developers - (both internal and external to the core team) are people who want to work with the latest development version of the Chaste code, between the main stable releases.

See [Getting Started](../..) for more detail if you still aren't sure.


### 2a. For Code USERS (working with a release, rather than developers)

You can obtain the latest stable release of the Chaste source code from our GitHub repository:

```
git clone --recursive -b release https://chaste.cs.ox.ac.uk/git/chaste.git Chaste
```

Finally, follow the [CMake First Run Guide](../../user-guides/cmake-first-run) to get up and running with Chaste.


#### Installing previous releases

If you want a specific version of Chaste, and do not want to stay up-to-date with new versions on the `release` branch from our Git repository, you can download the source code from our [GitHub releases page](https://github.com/Chaste/Chaste/releases), back to Release 3.0.

### 2b. For Code DEVELOPERS (or users working with the latest trunk code and projects)

To install the suggested packages:

```
sudo apt update
sudo apt install --install-recommends chaste-dependencies
sudo apt install `dpkg -s chaste-dependencies | egrep "^Suggests" | cut -d "," -f 1-111 --output-delimiter " " | cut -d ":" -f 2`
```
