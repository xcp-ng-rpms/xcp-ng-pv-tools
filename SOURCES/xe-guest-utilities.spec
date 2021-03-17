# -*- rpm-spec -*-

Summary: Virtual Machine Monitoring Scripts
Name: xe-guest-utilities
Version: %xgu_version
Release: %xgu_release
License: BSD
Group: Xen
URL: https://github.com/xcp-ng/xe-guest-utilities

Source0: xe-linux-distribution
Source1: xe-linux-distribution.init
Source2: xe-daemon
Source3: xenstore
Source4: LICENSE
Source5: xen-vcpu-hotplug.rules

%description
Scripts for monitoring Virtual Machine.

Writes distribution version information and IP address to XenStore.

%package xenstore

Summary: Virtual Machine XenStore utilities
%description xenstore
Utilities for interacting with XenStore from within a Xen Virtual Machine

%install
install -d %{buildroot}/usr/sbin/
install -d %{buildroot}/etc/init.d
install -d %{buildroot}/etc/udev/rules.d
install -d %{buildroot}/usr/bin/
install -d %{buildroot}/usr/share/doc/%{name}-%{version}

install -m 755 %{SOURCE0} %{buildroot}/usr/sbin/xe-linux-distribution
install -m 755 %{SOURCE1} %{buildroot}/etc/init.d/xe-linux-distribution
install -m 755 %{SOURCE2} %{buildroot}/usr/sbin/xe-daemon
install -m 755 %{SOURCE3} %{buildroot}/usr/bin/xenstore
ln -s /usr/bin/xenstore %{buildroot}/usr/bin/xenstore-read
ln -s /usr/bin/xenstore %{buildroot}/usr/bin/xenstore-write
ln -s /usr/bin/xenstore %{buildroot}/usr/bin/xenstore-exists
ln -s /usr/bin/xenstore %{buildroot}/usr/bin/xenstore-rm
ln -s /usr/bin/xenstore %{buildroot}/usr/bin/xenstore-list
ln -s /usr/bin/xenstore %{buildroot}/usr/bin/xenstore-ls
ln -s /usr/bin/xenstore %{buildroot}/usr/bin/xenstore-chmod
ln -s /usr/bin/xenstore %{buildroot}/usr/bin/xenstore-watch

install -m 755 %{SOURCE4} %{buildroot}/usr/share/doc/%{name}-%{version}/
install -m 755 %{SOURCE5} %{buildroot}/etc/udev/rules.d/z10-xen-vcpu-hotplug.rules

%post
/sbin/chkconfig --add xe-linux-distribution >/dev/null
[ -n "${EXTERNAL_P2V}" ] || service xe-linux-distribution start >/dev/null 2>&1

%preun
if [ $1 -eq 0 ] ; then
    service xe-linux-distribution stop >/dev/null 2>&1
    /sbin/chkconfig --del xe-linux-distribution >/dev/null
fi

%files
/usr/sbin/xe-linux-distribution
/etc/init.d/xe-linux-distribution
/usr/sbin/xe-daemon
/etc/udev/rules.d/z10-xen-vcpu-hotplug.rules
/usr/share/doc/%{name}-%{version}/LICENSE

%files xenstore
/usr/bin/xenstore-*
/usr/bin/xenstore

%changelog
* %changelogdate XCP-ng <xcp-ng.org> - %xgu_version-%xgu_release
- Version %xgu_version
