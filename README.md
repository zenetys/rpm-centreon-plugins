| <nobr>Package name</nobr> | <nobr>Supported targets</nobr> | Includes |
| :--- | :--- | :--- |
| <nobr>centreon-plugins</nobr> | el9 | JMX::Jmx4Perl, UUID::generate(), ZMQ::Constants, ZMQ::LibZMQ4 |
<br/>

## Build:

The package can be built easily using the rpmbuild-docker script provided
in this repository. In order to use this script, _**a functional Docker
environment is needed**_, with ability to pull Rocky Linux (el9) images
from internet if not already downloaded.

```
$ ./rpmbuild-docker -d el9
```

## Prebuilt packages:

Builds of these packages are available on ZENETYS yum repositories:<br/>
https://packages.zenetys.com/latest/redhat/
