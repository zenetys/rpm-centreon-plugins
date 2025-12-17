# Supported targets: el9

%define perl_zmq_libzmq4 ZMQ-LibZMQ4-0.01
%define perl_zmq_constants ZMQ-Constants-1.04
%define perl_net_ntp Net-NTP-1.5
%define perl_net_curl Net-Curl-0.56
%define perl_net_curl Net-Curl-0.56
%define perl_jmx4perl jmx4perl-1.13
%define perl_dbd_sybase DBD-Sybase-1.26

%define packager_deps /opt/centreon-plugins/_packager_deps

Name: centreon-plugins
Version: 20251200
Release: 1%{?dist}.zenetys
Summary: Centreon plugins collection
Group: Applications/System
License: ASL 2.0
URL: https://github.com/centreon/centreon-plugins

# centreon-plugins
Source0: https://github.com/centreon/centreon-plugins/archive/refs/tags/plugins-%{version}.tar.gz
Patch0: centreon-plugins-packager-deps.patch
Patch1: centreon-plugins-cifs-options-port-timeout.patch
Patch2: centreon-plugins-cifs-default-port-445.patch

# bundled dependencies
Source100: https://cpan.metacpan.org/authors/id/M/MO/MOSCONI/%{perl_zmq_libzmq4}.tar.gz
Patch100: ZMQ-LibZMQ4-0.01-Fix-building-on-Perl-without-.-in-INC.patch
Source200: https://cpan.metacpan.org/authors/id/D/DM/DMAKI/%{perl_zmq_constants}.tar.gz
Source300: UUID.pm
Source400: https://cpan.metacpan.org/authors/id/A/AB/ABH/%{perl_net_ntp}.tar.gz
Source500: https://cpan.metacpan.org/authors/id/S/SY/SYP/%{perl_net_curl}.tar.gz
Source600: https://cpan.metacpan.org/authors/id/R/RO/ROLAND/%{perl_jmx4perl}.tar.gz
Source700: https://cpan.metacpan.org/authors/id/M/ME/MEWP/%{perl_dbd_sybase}.tar.gz

# build requirements for bundled dependencies
BuildRequires: findutils
BuildRequires: freetds-devel
BuildRequires: libcurl-devel
BuildRequires: libsmbclient-devel
BuildRequires: make
BuildRequires: perl(inc::Module::Install)
BuildRequires: perl-DBI
BuildRequires: zeromq-devel

Requires: freetds-libs
Requires: perl-base
Requires: perl-DateTime
Requires: perl-DateTime-Format-Strptime
Requires: perl-DBI
Requires: perl-FindBin
Requires: perl-JSON-XS
Requires: perl-lib
Requires: perl-LWP-Protocol-https
Requires: perl-Net-DNS
Requires: perl-Safe
Requires: perl(SNMP)
Requires: perl-Time-HiRes
Requires: perl-Tie

# requirements for bundled dependencies
# jmx4perl
Requires: perl-Module-Find
Requires: perl-Sys-SigAction
# perl-UUID wrapper
Requires: perl-UUID-Tiny

%description
Centreon collection of standard plugins to discover and gather
cloud-to-edge metrics and status across your whole IT infrastructure.

Bundled dependencies:
- perl UUID::generate() wrapper for UUID::Tiny (epel)
- perl %{perl_zmq_constants}
- perl %{perl_zmq_libzmq4}
- perl %{perl_net_ntp}
- perl Filesys::SmbClient (dependencies/perl-filesys-smbclient)

%prep
# centreon-plugins
%setup -c
cd centreon-plugins-plugins-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
cd ..

# perl ZMQ-LibZMQ4
%setup -T -D -a 100
cd %{perl_zmq_libzmq4}
%patch100 -p1 -b .build-no-dot-in-inc
cd ..

# perl ZMQ-Constants
%setup -T -D -a 200

# perl Net-NTP
%setup -T -D -a 400

# perl Net-Curl
%setup -T -D -a 500

# jmx4perl
%setup -T -D -a 600

# perl DBD-Sybase
%setup -T -D -a 700

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

# perl Net-NTP
cd %{perl_net_ntp}
perl Makefile.PL INSTALL_BASE=%{packager_deps} NO_PACKLIST=1
make %{?_smp_mflags}
cd ..

# perl Net-Curl
cd %{perl_net_curl}
perl Makefile.PL INSTALL_BASE=%{packager_deps} OPTIMIZE="$RPM_OPT_FLAGS" NO_PACKLIST=1
make %{?_smp_mflags}
cd ..

# jmx4perl
cd %{perl_jmx4perl}
# noop
cd ..

# perl DBD-Sybase
cd %{perl_dbd_sybase}
SYBASE=/usr \
DBD_SYB_USE_ENV=Y \
DBD_SYB_CHAINED=Y \
DBD_SYB_THREADED_LIBS=N \
DBD_SYB_SRV=SYBASE \
DBD_SYB_DB= \
DBD_SYB_UID= \
DBD_SYB_PWD= \
    perl Makefile.PL INSTALL_BASE=%{packager_deps} OPTIMIZE="$RPM_OPT_FLAGS" NO_PACKLIST=1
make %{?_smp_mflags}
cd ..

# centreon plugins
cd centreon-plugins-plugins-%{version}
# perl Filesys-SmbClient (dependencies/perl-filesys-smbclient)
cd dependencies/perl-filesys-smbclient/src
perl Makefile.PL INSTALL_BASE=%{packager_deps} OPTIMIZE="$RPM_OPT_FLAGS" NO_PACKLIST=1
make %{?_smp_mflags}
cd ../../..
cd ..

%install
# centreon plugins
cd centreon-plugins-plugins-%{version}
install -d -m 0755 %{buildroot}/opt/centreon-plugins
cp -RT --preserve=timestamp src %{buildroot}/opt/centreon-plugins
# perl Filesys-SmbClient (dependencies/perl-filesys-smbclient)
cd dependencies/perl-filesys-smbclient/src/
make pure_install DESTDIR=%{buildroot}
cd ../../..
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

# perl Net-NTP
cd %{perl_net_ntp}
make pure_install DESTDIR=%{buildroot}
cd ..

# perl Net-Curl
cd %{perl_net_curl}
make pure_install DESTDIR=%{buildroot}
cd ..

# jmx4perl
cd %{perl_jmx4perl}
cp -RT --preserve=timestamps lib %{buildroot}/%{packager_deps}/lib/perl5/
cd ..

# perl DBD-Sybase
cd %{perl_dbd_sybase}
make pure_install DESTDIR=%{buildroot}
cd ..

# cleanup unnecessary stuff from bundled perl modules
rm -rf %{buildroot}/%{packager_deps}/man
%{_fixperms} %{buildroot}/%{packager_deps}

%files
%doc centreon-plugins-plugins-%{version}/changelog
%doc centreon-plugins-plugins-%{version}/README.md
%license centreon-plugins-plugins-%{version}/LICENSE.txt
/opt/centreon-plugins
