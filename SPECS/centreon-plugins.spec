# Supported targets: el9

Name: centreon-plugins
Version: 20230118
Release: 1%{?dist}.zenetys
Summary: Centreon plugins collection
Group: Applications/System
License: ASL 2.0
URL: https://github.com/centreon/centreon-plugins
Source0: https://github.com/centreon/centreon-plugins/archive/refs/tags/%{version}.tar.gz
BuildArch: noarch

Requires: net-snmp-perl
Requires: perl-base
Requires: perl-DateTime
Requires: perl-FindBin
Requires: perl-JSON-XS
Requires: perl-lib
Requires: perl-Safe
Requires: perl-Time-HiRes

%description
Centreon collection of standard plugins to discover and gather
cloud-to-edge metrics and status across your whole IT infrastructure.

%prep
%setup

%install
install -d -m 0755 %{buildroot}/opt/centreon-plugins
cp -RT --preserve=timestamp src %{buildroot}/opt/centreon-plugins

%files
%doc changelog README.md
%license LICENSE.txt
%dir /opt/centreon-plugins
/opt/centreon-plugins/*
