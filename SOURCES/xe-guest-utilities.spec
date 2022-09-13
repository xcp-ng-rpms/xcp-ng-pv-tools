# -*- rpm-spec -*-

Summary: Virtual Machine Monitoring Scripts
Name: xe-guest-utilities
Version: %xgu_version
Release: %xgu_release
License: BSD
Group: Xen
URL: https://github.com/xcp-ng/xe-guest-utilities

Source0: xe-linux-distribution
Source1: xe-linux-distribution.service
Source2: xe-daemon
Source3: xenstore
Source4: LICENSE
Source5: xen-vcpu-hotplug.rules

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Obsoletes: xe-guest-utilities-xenstore < 7.30.0-11

%description
Scripts for monitoring Virtual Machines and utilities for interacting with XenStore.

Writes distribution version information and IP address to XenStore.

%install
install -d %{buildroot}/usr/sbin/
install -d %{buildroot}/etc/udev/rules.d
install -d %{buildroot}/usr/bin/
install -d %{buildroot}/usr/share/doc/%{name}-%{version}
install -d %{buildroot}/usr/lib/systemd/system

install -m 755 %{SOURCE0} %{buildroot}/usr/sbin/xe-linux-distribution
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/xe-linux-distribution.service
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
    systemctl enable xe-linux-distribution.service >/dev/null 2>&1 ||:
    # If a version of the tools with an init.d service was uninstalled just before, systemd may see the service
    # as active just after it enables it. In this situation, a start won't work and a restart is necessary.
    if [ $(systemctl is-active xe-linux-distribution.service) == 'active' ] >/dev/null 2>&1; then
        systemctl restart xe-linux-distribution.service >/dev/null 2>&1 ||:
    else
        systemctl start xe-linux-distribution.service >/dev/null 2>&1 ||:
    fi
elif [ $1 -eq 2 ]; then
    # Handle the transition from an init.d service if needed
    if command -v chkconfig >/dev/null 2>&1 && chkconfig --list xe-linux-distribution >/dev/null 2>&1; then
        service xe-linux-distribution stop >/dev/null 2>&1 ||:
        /sbin/chkconfig --del xe-linux-distribution >/dev/null 2>&1 ||:
        systemctl enable xe-linux-distribution.service >/dev/null 2>&1 ||:
        # systemd may see the new service as active, because it used to know it as an init.d service.
        # And this despite the fact that we stopped the old service above.
        # In this situation, a start won't work and a restart is necessary.
        systemctl restart xe-linux-distribution.service >/dev/null 2>&1 ||:
    else
        systemctl restart xe-linux-distribution.service >/dev/null 2>&1 ||:
    fi
fi

%preun
if [ $1 -eq 0 ]; then
    if systemctl is-enabled xe-linux-distribution >/dev/null 2>&1; then
        systemctl disable xe-linux-distribution.service >/dev/null 2>&1 ||:
        systemctl stop xe-linux-distribution.service >/dev/null 2>&1 ||:
    fi
fi

%postun
systemctl daemon-reload >/dev/null 2>&1 ||:

%files
/usr/sbin/xe-linux-distribution
/usr/sbin/xe-daemon
/etc/udev/rules.d/z10-xen-vcpu-hotplug.rules
/usr/share/doc/%{name}-%{version}/LICENSE
/usr/lib/systemd/system/xe-linux-distribution.service
/usr/bin/xenstore-*
/usr/bin/xenstore

%changelog
* %changelogdate XCP-ng <xcp-ng.org> - %xgu_version-%xgu_release
- Version %xgu_version
