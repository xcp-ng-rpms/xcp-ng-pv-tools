XCP-ng Tools for Linux (and a word about Windows)
=================================================

This CD contains the XCP-ng Tools and Drivers for supported linux
guest operating systems. You will need to install them to get the best
performance from your virtual machine, and to access advanced features
such as XenMotion.

Windows
-------

We are not allowed to redistribute the windows tools built and signed by
Citrix, so they are not included here.

Refer to our online documentation for instructions:
https://xcp-ng.org/docs/guests.html#windows

Linux
-----

Linux users need to install the guest tools from the /Linux directory on
this CD. This will ensure your Linux VM has access to advanced features
such as XenMotion and in-guest performance metrics.

In addition, we have provided a number of kernel files, which are mostly
based on the vendor-provided kernels, but provide specific enhancements
for improved stability and performance when running on XCP-ng. 
Those are only required for very old VMs since the linux kernel has
included xen drivers by default for many years now.

You can install the required packages by running install.sh like so:

$ <mnt>/Linux/install.sh

where <mnt> is the CD mount point.

To omit the kernel upgrade pass the -k flag to install.sh.

More information on our online documentation:
https://xcp-ng.org/docs/guests.html#linux

FreeBSD
-------

Run the install.sh script, which will offer to download and install
the `xe-guest-utilities` package from FreeBSD's repositories.

More information at https://xcp-ng.org/docs/guests.html#freebsd
