Name: opentabletdriver
Version: 0.0.0
Release: 1
Summary: A cross-platform open source tablet driver
License: LGPLv3
URL: https://github.com/OpenTabletDriver/OpenTabletDriver

Requires: dotnet-runtime-5.0
Requires: pkgconfig(libevdev)
Requires: gtk3
Recommends: pkgconfig(xrandr)
Recommends: pkgconfig(x11)

%description
OpenTabletDriver is an open source, cross platform, user mode tablet driver. The goal of OpenTabletDriver is to be cross platform as possible with the highest compatibility in an easily configurable graphical user interface.

%install
mkdir -p %{buildroot}
cp -r %{pkg_dir}/* %{buildroot}/

%pre
%systemd_user_pre opentabletdriver.service

%post
udevadm control --reload-rules
%systemd_user_post opentabletdriver.service

if lsmod | grep hid_uclogic > /dev/null ; then
     rmmod hid_uclogic || true
fi

if lsmod | grep wacom > /dev/null ; then
     rmmod wacom || true
fi

%preun
%systemd_user_preun opentabletdriver.service

%postun
%systemd_user_postun opentabletdriver.service

%files
%defattr(-,root,root)
%dir /usr/share/OpenTabletDriver
%dir /usr/share/doc/OpenTabletDriver
/usr/share/OpenTabletDriver/*
/usr/share/doc/OpenTabletDriver/*
/usr/share/man/man8/opentabletdriver.8*
/usr/share/pixmaps/otd.ico
/usr/share/pixmaps/otd.png
/usr/share/applications/OpenTabletDriver.desktop
/usr/bin/opentabletdriver
/usr/bin/otd
/usr/lib/systemd/user/opentabletdriver.service
/usr/lib/systemd/user-preset/50-opentabletdriver.preset
/usr/lib/udev/rules.d/99-opentabletdriver.rules
/usr/lib/modprobe.d/99-opentabletdriver.conf
