%global _smp_mflags %nil

Name: opentabletdriver
Version: 0.0.0
Release: 1
Summary: A cross-platform open source tablet driver
License: LGPLv3
URL: https://github.com/OpenTabletDriver/OpenTabletDriver

Source0: opentabletdriver-%{version}.tar.gz

AutoReqProv: no
Requires: dotnet-runtime-6.0
Requires: pkgconfig(libevdev)
Requires: gtk3
Recommends: pkgconfig(xrandr)
Recommends: pkgconfig(x11)

%description
OpenTabletDriver is an open source, cross platform, user mode tablet driver. The goal of OpenTabletDriver is to be cross platform as possible with the highest compatibility in an easily configurable graphical user interface.

%prep
%autosetup -n OpenTabletDriver

%build
%make_build

%install
%make_install

%post
udevadm control --reload-rules

if lsmod | grep hid_uclogic > /dev/null ; then
     rmmod hid_uclogic || true
fi

if lsmod | grep wacom > /dev/null ; then
     rmmod wacom || true
fi

%files
%defattr(-,root,root)
%dir %{_datadir}/OpenTabletDriver
%dir %{_defaultdocdir}/OpenTabletDriver
%{_datadir}/OpenTabletDriver/*
%{_defaultdocdir}/OpenTabletDriver/*
%{_mandir}/man8/opentabletdriver.8*
%{_datadir}/pixmaps/otd.ico
%{_datadir}/pixmaps/otd.png
%{_datadir}/applications/OpenTabletDriver.desktop
%{_prefix}/bin/opentabletdriver
%{_prefix}/bin/otd
%{_prefix}/lib/systemd/user/opentabletdriver.service
%{_prefix}/lib/udev/rules.d/99-opentabletdriver.rules
%{_prefix}/lib/modprobe.d/99-opentabletdriver.conf
