%define xs_linux_tools_version 7.20.0
%define xs_linux_tools_release 1
%define xcp_ng_release 8.2.0

Name: xcp-ng-pv-tools
Version: %{xcp_ng_release}
Release: 1%{?dist}
Summary: ISO with the Linux PV Tools
License: GPLv2
Vendor: XCP-ng
# Until we're ready to build the tools ourselves, we'll extract the linux tools from XenServer's tarball
Source0: LinuxGuestTools-%{xs_linux_tools_version}-%{xs_linux_tools_release}.tar.gz
Source1: README.txt
Source2: sr_rescan
Source3: unmount_xstools.sh
# Patches from https://github.com/xcp-ng/xe-guest-utilities
# Produced by comparing the XS branch with install.sh added from tarball, with ours
# E.g.: git format-patch 7.20.0-XS_with_install_sh 7.20.0-8.2
Patch1: 0001-Add-support-for-CloudLinux-which-is-based-on-CentOS.patch
Patch2: 0002-Add-support-for-Sangoma-Linux-FreePBX-CentOS-based.patch
Patch3: 0003-Freebsd-support-1.patch

BuildArch: noarch
BuildRequires: genisoimage

Provides: xenserver-pv-tools
Obsoletes: xenserver-pv-tools

%define iso_version %{version}-%{release}

%description
ISO with the Linux PV Tools

%prep
%autosetup -p2 -n LinuxGuestTools-%{xs_linux_tools_version}-%{xs_linux_tools_release}
rm *.orig -f

%build
install -d iso
install -m 0755 %{SOURCE1} iso/README.txt
install -d iso/Linux
rm -f README.txt
find . -maxdepth 1 -type f -exec mv {} iso/Linux/ \;
pushd iso/Linux
chmod 644 *
chmod a+x install.sh xe-daemon xe-linux-distribution
popd
genisoimage -joliet -joliet-long -r \
            -A "XCP-ng Tools" \
            -V "XCP-ng Tools" \
            -publisher "XCP-ng" \
            -o guest-tools.iso \
            iso/

%install
install -D -m644 guest-tools.iso %{buildroot}/opt/xensource/packages/iso/guest-tools-%{iso_version}.iso
install -D -m755 %{SOURCE2} %{buildroot}/opt/xensource/bin/sr_rescan
install -D -m755 %{SOURCE3} %{buildroot}/opt/xensource/libexec/unmount_xstools.sh

%post
/opt/xensource/libexec/unmount_xstools.sh
/opt/xensource/bin/sr_rescan

%postun
/opt/xensource/bin/sr_rescan

%files
/opt/xensource/packages/iso/guest-tools-%{iso_version}.iso
/opt/xensource/bin/sr_rescan
/opt/xensource/libexec/unmount_xstools.sh

%changelog
* Mon Oct 05 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.2.0-1
- Update for XCP-ng 8.2.0
- Change versioning
- Build from tarball now, not from ISO that doesn't exist anymore
- Rename unmount_halted_xstools.sh to unmount_xstools.sh
- Update README.txt (new doc links + FreeBSD section)

* Wed Jan 29 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.45.0-2
- Add xcp-ng-pv-tools-7.45.0-fix-boot-hang-caused-by-CPU-hotplug-rule.backport.patch
- Backported from master

* Mon Jan 13 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.45.0-1
- Update for XCP-ng 8.1
- Remove xcp-ng-pv-tools-7.41.0-add-RHEL-8-and-derivatives.XCP-ng.patch
- Remove xcp-ng-pv-tools-7.41.0-add-SLES-15-SP1-support.backport.patch
- Remove xcp-ng-pv-tools-7.41.0-fix-installation-on-CoreOS.XCP-ng.patch
- Update and rename xcp-ng-pv-tools-7.45.0-add-cloudlinux-and-sangoma.XCP-ng.patch

* Wed Nov 27 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.41.0-10
- Eject mounted guest tools from all VMs, not just halted VMs
- Related to https://github.com/xcp-ng/xcp/issues/282

* Wed Oct 16 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.41.0-9
- Add detection of CloudLinux
- Add detection of FreePBX (Sangoma Linux)

* Tue Oct 15 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.41.0-7
- Add support for RHEL 8 and derivatives in install.sh

* Mon Jul 15 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.41.0-6
- Update README.txt with up to date links for Windows guest tools

* Wed Jun 19 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.41.0-4
- Backport support for SLES 15 SP1

* Thu Jun 13 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.41.0-3
- Fix installation of linux guest tools on CoreOS

* Thu May 09 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.41.0-1
- Update for XCP-ng 8.0.0

* Fri Sep 14 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.32.0-2.1.xcp
- Update for XCP-ng 7.6.0

* Fri Aug 03 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.29.0-2.1.xcp
- Update README.txt

* Wed Jun 27 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.29.0-2
- Import from XenServer
- Rename to xcp-ng-pv-tools
- Remove Windows tools, signed by Citrix
