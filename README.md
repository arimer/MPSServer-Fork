# MPSServer

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FStrumenta%2FMPSServer%2Fbadge&style=flat)](https://actions-badge.atrox.dev/Strumenta/MPSServer/goto)
[ ![Download](https://api.bintray.com/packages/strumenta/strumenta-oss-maven/MPSServer/images/download.svg) ](https://bintray.com/strumenta/strumenta-oss-maven/MPSServer/_latestVersion)


This is a solution that starts a server to read and modify MPS models through HTTP and WebSocket.

The server can be started from MPS running normally or in headless mode.

There is also a framework to define web editors interoperable with MPSServer. This framework is called [WebEditKit](https://github.com/Strumenta/webeditkit) and it is open-source.

You can find some basic instructions and an example here: https://github.com/Strumenta/calc-webeditkit-example

## The simplest way to use MPSServer

Simply look in the `example` directory.

Basically you need a simple build.gradle file in your project and that is it.

1. Create this build.gradle file

```
buildscript {
    repositories {
        jcenter()
        maven { url 'https://projects.itemis.de/nexus/content/repositories/mbeddr' }
    }
}

plugins {
    id 'com.strumenta.mpsserver' version "0.1.0-snapshot"
}

repositories {
	mavenCentral()
	maven {
		url 'https://dl.bintray.com/strumenta/strumenta-oss-maven'
	}
	maven {
		url 'https://projects.itemis.de/nexus/content/groups/OS/'
	}
}

mpsserver {
	mpsServerVersion = '1.1.0-rc1'
}
```

2. Launch `./gradlew launchMpsServer`

And you are good to go!

At that point simply visit `http://localhost:2904/models/<my model>/<my node id>` to see the data of your model.

You can find the Node ID in the inspector:
![](images/nodeid.png)

And this is how you can use the simplest API call:
![](images/api.png)
