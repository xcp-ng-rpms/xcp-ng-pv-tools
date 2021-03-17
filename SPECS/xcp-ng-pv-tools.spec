# xgu stands for xe-guest-utilities
%define xgu_major 7
%define xgu_minor 20
%define xgu_micro 0
%define xgu_version %{xgu_major}.%{xgu_minor}.%{xgu_micro}

# xcp-ng-pv-tools is versioned after the release of XCP-ng it was made for
%define xcp_ng_release 8.2.0

Name: xcp-ng-pv-tools
Version: %{xcp_ng_release}
%define _release 3
Release: %{_release}%{?dist}

# The xe-guest-utilities release is the xcp-ng-pv-tools release
%define xgu_release %{_release}

Summary: ISO with the Linux PV Tools

# The tools in the ISO are licensed under a BSD-2-clause license
# The license of the sr_rescan and unmount_xstools.sh scripts is unclear:
# GPLv2 according to the License tag and description of the xenserver-pv-tools RPM in Citrix Hypervisor 8.1,
# but that description was already dubious since it said that the Linux PV Tools were GPLv2,
# when they've actually been under a BSD license for years.
# To play it safe, we'll consider those two scripts are GPLv2, since they came from a RPM that was under such license.
# The rest is BSD.
License: BSD and GPLv2
URL: https://github.com/xcp-ng/xe-guest-utilities

# We want an archive that matches upstream tag, but with install.sh included.
# Tarball created from https://github.com/xcp-ng/xe-guest-utilities with command:
# git archive $XGUVERSION-XS_with_install_sh --prefix=xe-guest-utilities-$XGUVERSION/ --format tar.gz -o xe-guest-utilities-$XGUVERSION-with_install_sh.tar.gz
# When upstream will finally add install.sh to their repo, then this will become simpler
Source0: xe-guest-utilities-%{xgu_version}-with_install_sh.tar.gz
Source1: README.txt
Source2: sr_rescan
Source3: unmount_xstools.sh
Source4: xe-guest-utilities.spec
Source10: debian-changelog
Source11: debian-compat
Source12: debian-control
Source13: debian-copyright
Source14: debian-postinst
Source15: debian-postrm
Source16: debian-prerm
Source17: debian-rules
Patch0: LICENSE.patch

# Additional patches, created from the maintenance branch (e.g. 7.20.0-8.2)
# Example creation command:
# git format-patch 7.20.0-XS_with_install_sh..7.20.0-8.2
Patch1: 0001-Add-support-for-CloudLinux-which-is-based-on-CentOS.patch
Patch2: 0002-Add-support-for-Sangoma-Linux-FreePBX-CentOS-based.patch
Patch3: 0003-Freebsd-support-1.patch
Patch4: 0004-Backport-Fix-name-of-tarball-based-on-GOARCH.patch

BuildArch: noarch
BuildRequires: genisoimage
BuildRequires: golang
BuildRequires: golang-github-golang-sys-devel
BuildRequires: dpkg-dev
BuildRequires: fakeroot

Provides: xenserver-pv-tools
Obsoletes: xenserver-pv-tools

%define iso_version %{version}-%{release}

%description
ISO with the Linux PV Tools

%prep
%autosetup -p1 -n xe-guest-utilities-%{xgu_version}

%build
# *** Functions ***
function build_and_copy_rpm {
    ARCH=$1
    mkdir -p rpmbuild-$ARCH
    pushd rpmbuild-$ARCH
    mkdir SPECS SOURCES
    cp %{SOURCE4} SPECS/
    cp ../build/obj/{xe-daemon,xenstore} SOURCES/
    cp ../LICENSE SOURCES/
    cp ../mk/{xe-linux-distribution,xe-linux-distribution.init,xen-vcpu-hotplug.rules} SOURCES/
    # _rpmfilename redefined to be independent from the build environment definition
    rpmbuild --target $ARCH \
        -bb SPECS/xe-guest-utilities.spec \
        --define "_topdir $(pwd)" \
        --define "xgu_version %{xgu_version}" \
        --define "xgu_release %{xgu_release}" \
        --define "changelogdate $(LC_ALL=C date +'%a %b %d %Y')" \
        --define "_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm"
    popd

    # Copy RPMs
    install -m 0644 rpmbuild-$ARCH/RPMS/*.rpm iso/Linux/
    # Two RPMs are produced
    RPMS=$(cd rpmbuild-$ARCH/RPMS/ && ls *.rpm)
    echo "XE_GUEST_UTILITIES_PKG_FILE_$ARCH='$(echo $RPMS | tr '\n' ' ')'" >> versions.rpm
}

function build_and_copy_deb {
    ARCH=$1
    mkdir -p debian-$ARCH/xe-guest-utilities-%{xgu_version}/debian
    pushd debian-$ARCH/xe-guest-utilities-%{xgu_version}
    cp %{SOURCE10} debian/changelog
    sed -i debian/changelog -e 's/@VERSION_RELEASE@/%{xgu_version}-%{xgu_release}/'
    sed -i debian/changelog -e 's/@XCPNG_VERSION@/%{xcp_ng_release}/'
    sed -i debian/changelog -e "s/@DATE@/$(date -R)/"
    cp %{SOURCE11} debian/compat
    cp %{SOURCE12} debian/control
    cp %{SOURCE13} debian/copyright
    cp %{SOURCE14} debian/postinst
    cp %{SOURCE15} debian/postrm
    cp %{SOURCE16} debian/prerm
    cp %{SOURCE17} debian/rules
    cp ../../build/obj/{xe-daemon,xenstore} .
    cp ../../LICENSE .
    cp ../../mk/{xe-linux-distribution,xe-linux-distribution.init,xen-vcpu-hotplug.rules} .
    dpkg-buildpackage -us -uc -a $ARCH
    popd

    # Copy Deb
    install -m 0644 debian-$ARCH/*.deb iso/Linux/
    # Only one deb is produced but what follows will work if there are several
    DEBS=$(cd debian-$ARCH/ && ls *.deb)
    echo "XE_GUEST_UTILITIES_PKG_FILE_$ARCH='$(echo $DEBS | tr '\n' ' ')'" >> versions.deb
}

function copy_tgz {
    ARCH=$1
    install -m 0644 build/dist/*.tgz iso/Linux/
    # Only one tgz is produced but what follows will work if there are several
    TGZS=$(cd build/dist/ && ls *.tgz)
    echo "XE_GUEST_UTILITIES_PKG_FILE_$ARCH='$(echo $TGZS | tr '\n' ' ')'" >> versions.tgz
}

# *** Begin ***
export GOPATH=/usr/share/gocode
mkdir -p iso/Linux
touch iso/Linux/versions.rpm
touch iso/Linux/versions.deb
touch iso/Linux/versions.tgz

# *** x86_64 build ***
GOARCH=amd64 make \
    PRODUCT_MAJOR_VERSION=%{xgu_major} \
    PRODUCT_MINOR_VERSION=%{xgu_minor} \
    PRODUCT_MICRO_VERSION=%{xgu_micro} \
    RELEASE=%{xgu_release}

copy_tgz amd64
build_and_copy_rpm x86_64
build_and_copy_deb amd64

# *** i386 build ***
make clean
GOARCH=386 make \
    PRODUCT_MAJOR_VERSION=%{xgu_major} \
    PRODUCT_MINOR_VERSION=%{xgu_minor} \
    PRODUCT_MICRO_VERSION=%{xgu_micro} \
    RELEASE=%{xgu_release}

copy_tgz i386
# Copy 32 bit xe-daemon binary
install -m 0755 build/obj/xe-daemon iso/Linux/
build_and_copy_rpm i386
build_and_copy_deb i386

# *** Build the ISO ***
install -m 0644 %{SOURCE1} iso/README.txt
install -m 0644 versions.tgz versions.rpm versions.deb iso/Linux/
install -m 0755 mk/install.sh \
                mk/xe-linux-distribution \
                mk/xe-linux-distribution.service \
                mk/xen-vcpu-hotplug.rules \
                LICENSE \
                iso/Linux/

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
* Tue Feb 23 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.2.0-3
- Build the binaries and packages contained in the ISO ourselves

* Mon Oct 12 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.2.0-2
- Fix typo in sr_rescan (rhe => the)

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
