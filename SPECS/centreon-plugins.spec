# Supported targets: el9

%define perl_zmq_libzmq4 ZMQ-LibZMQ4-0.01
%define perl_zmq_constants ZMQ-Constants-1.04

%define packager_deps /opt/centreon-plugins/_packager_deps

Name: centreon-plugins
Version: 20231114
Release: 1%{?dist}.zenetys
Summary: Centreon plugins collection
Group: Applications/System
License: ASL 2.0
URL: https://github.com/centreon/centreon-plugins

# centreon-plugins
Source0: https://github.com/centreon/centreon-plugins/archive/refs/tags/plugins-%{version}.tar.gz
Patch0: centreon-plugins-packager-deps.patch

# bundled dependencies
Source100: https://cpan.metacpan.org/authors/id/M/MO/MOSCONI/%{perl_zmq_libzmq4}.tar.gz
Patch100: ZMQ-LibZMQ4-0.01-Fix-building-on-Perl-without-.-in-INC.patch
Source200: https://cpan.metacpan.org/authors/id/D/DM/DMAKI/%{perl_zmq_constants}.tar.gz
Source300: UUID.pm

# build requirements for bundled dependencies
BuildRequires: findutils
BuildRequires: make
BuildRequires: perl(inc::Module::Install)
BuildRequires: zeromq-devel

Requires: net-snmp-perl
Requires: perl-base
Requires: perl-DateTime
Requires: perl-FindBin
Requires: perl-JSON-XS
Requires: perl-lib
Requires: perl-LWP-Protocol-https
Requires: perl-Net-DNS
Requires: perl-Safe
Requires: perl-Time-HiRes

# requirements for bundled dependencies
Requires: perl-UUID-Tiny

%description
Centreon collection of standard plugins to discover and gather
cloud-to-edge metrics and status across your whole IT infrastructure.

Bundled dependencies:
- perl UUID::generate() wrapper for UUID::Tiny (epel)
- perl %{perl_zmq_constants}
- perl %{perl_zmq_libzmq4}

%prep
# centreon-plugins
%setup -c
cd centreon-plugins-plugins-%{version}
%patch0 -p1
cd ..

# perl ZMQ-LibZMQ4
%setup -T -D -a 100
cd %{perl_zmq_libzmq4}
%patch100 -p1 -b .build-no-dot-in-inc
cd ..

# perl ZMQ-Constants
%setup -T -D -a 200

%build
# perl ZMQ-LibZMQ4
cd %{perl_zmq_libzmq4}
perl Makefile.PL INSTALL_BASE=%{packager_deps} OPTIMIZE="$RPM_OPT_FLAGS" NO_PACKLIST=1
make %{?_smp_mflags}
cd ..

# perl ZMQ-Constants
cd %{perl_zmq_constants}
perl Makefile.PL INSTALL_BASE=%{packager_deps} NO_PACKLIST=1
make %{?_smp_mflags}
cd ..

%install
# centreon plugins
cd centreon-plugins-plugins-%{version}
install -d -m 0755 %{buildroot}/opt/centreon-plugins
cp -RT --preserve=timestamp src %{buildroot}/opt/centreon-plugins
cd ..

# perl ZMQ-LibZMQ4
cd %{perl_zmq_libzmq4}
make pure_install DESTDIR=%{buildroot}
cd ..

# perl ZMQ-Constants
cd %{perl_zmq_constants}
make pure_install DESTDIR=%{buildroot}
cd ..

# perl UUID::generate() wrapper for UUID::Tiny
install -Dp -m 0644 %{SOURCE300} %{buildroot}/%{packager_deps}/lib/perl5/

# cleanup unnecessary stuff from bundled perl modules
rm -rf %{buildroot}/%{packager_deps}/man
%{_fixperms} %{buildroot}/%{packager_deps}

%files
%doc centreon-plugins-plugins-%{version}/changelog
%doc centreon-plugins-plugins-%{version}/README.md
%license centreon-plugins-plugins-%{version}/LICENSE.txt
/opt/centreon-plugins
