# -*- rpm-spec -*-

Summary: Virtual Machine Monitoring Scripts
# Keep name as xe-guest-utilities to avoid upgrade issues with scriptlets preun/post scriptlets
# The file name will change, the but the RPM identifier will remain the same.
# To differenciate them, we'll add .legacy to the release tag.
Name: xe-guest-utilities
Version: %xgu_version
Release: %{xgu_release}.legacy
License: BSD
Group: Xen
URL: https://github.com/xcp-ng/xe-guest-utilities
Obsoletes: xe-guest-utilities < 7.30.0

Source0: xe-linux-distribution
Source1: xe-linux-distribution.init
Source2: xe-daemon
Source3: xenstore
Source4: LICENSE
Source5: xen-vcpu-hotplug.rules

Requires(post): chkconfig
Requires(preun): chkconfig
Requires(postun): chkconfig

%description
Scripts for monitoring Virtual Machine.

Writes distribution version information and IP address to XenStore.

%package xenstore

Summary: Virtual Machine XenStore utilities
%description xenstore
Utilities for interacting with XenStore from within a Xen Virtual Machine

Obsoletes: xe-guest-utilities-xenstore < 7.30.0

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
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add xe-linux-distribution >/dev/null 2>&1 ||:
    service xe-linux-distribution start >/dev/null 2>&1 ||:
elif [ $1 -eq 2 ]; then
    service xe-linux-distribution restart >/dev/null 2>&1 ||:
fi

%preun
if [ $1 -eq 0 ]; then
    if chkconfig --list xe-linux-distribution >/dev/null 2>&1; then
        service xe-linux-distribution stop >/dev/null 2>&1 ||:
        /sbin/chkconfig --del xe-linux-distribution >/dev/null 2>&1 ||:
    fi
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
