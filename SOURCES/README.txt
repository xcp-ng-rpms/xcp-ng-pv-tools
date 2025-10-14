XCP-ng Tools and Drivers
========================

This CD contains the XCP-ng Tools and Drivers for supported Windows and
Linux guest operating systems. You will need to install them to get the
best performance from your virtual machine, and to access advanced
features such as live VM migration and in-guest performance metrics.

Windows
-------

The bundled XCP-ng Windows Guest Tools are now production-ready and
compatible with guest Secure Boot.

Before installing, please note the following:
- We recommend creating backups and/or snapshots.
- These tools are not compatible with the "Manage Citrix PV drivers via
  Windows Update" option. This option can be disabled by navigating to
  the VM's Advanced tab in Xen Orchestra.
- Existing incompatible tools and drivers (XCP-ng Windows PV Tools 8.2
  or earlier, as well as any Citrix/XenServer drivers) must be
  uninstalled first.

Run the XenTools-<arch>.msi file in the /Windows directory to start the
installation.

This CD also includes two useful utilities for Windows guests:
- XenClean, an utility for cleanly removing all Xen tools and drivers
  from XCP-ng, XenServer among others;
- XenBootFix, an utility for recovering from boot failures caused by Xen
  drivers.

Refer to our online documentation for detailed instructions:
https://docs.xcp-ng.org/vms/#windows-guest-tools

Linux
-----

Linux users need to install the guest tools from the /Linux directory on
this CD.

In addition, we have provided a number of kernel files, which are mostly
based on the vendor-provided kernels, but provide specific enhancements
for improved stability and performance when running on XCP-ng.
Those are only required for very old VMs since the Linux kernel has
included Xen drivers by default for many years now.

You can install the required packages by running install.sh like so:

$ <mnt>/Linux/install.sh

where <mnt> is the CD mount point.

To omit the kernel upgrade pass the -k flag to install.sh.

More information on our online documentation:
https://docs.xcp-ng.org/vms/#linux-guest-tools

FreeBSD
-------

Run the install.sh script, which will offer to download and install
the `xe-guest-utilities` package from FreeBSD's repositories.

More information at https://docs.xcp-ng.org/vms/#bsd-guest-tools
