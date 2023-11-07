---
title : "PyChaste Docker"
description: "PyChaste docker install guide"
lead: "PyChaste docker install guide"
date: 2020-10-06T08:47:36+00:00
lastmod: 2020-10-06T08:47:36+00:00
draft: false
images: []
toc: true
---

## Overview
A docker container can be launched from an image which has PyChaste and Jupyter pre-installed.

## Installing Docker
If you would like to use this method but do not have docker already installed, you can find detailed guidance [here](https://docs.docker.com/get-docker/) on installing docker. Docker Desktop is the recommended route to getting docker running on your system.  

## Launching PyChaste with Docker
If you already have docker installed, you can launch a PyChaste container with the following command:
```
docker run -it --rm -p 8888:8888 chaste/pychaste
```

To open a jupyter notebook attached to the PyChaste container, launch a web browser and navigate to http://localhost::8888.