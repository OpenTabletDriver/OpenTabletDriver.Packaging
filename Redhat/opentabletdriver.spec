Name: opentabletdriver
Version: 0.0.0
Release: 1
Summary: A cross-platform open source tablet driver
BuildArch: x86_64

%if 0%{?suse_version}
License: LGPL-3.0-only
Group: Hardware/Other
%else
License: LGPLv3
%endif

URL: https://github.com/OpenTabletDriver/OpenTabletDriver

Requires: dotnet-runtime-5.0
Requires: pkgconfig(libevdev)
# Requires: pkgconfig(appindicator3-0.1) <- it is included in deb package but not in aur
Requires: gtk3
Recommends: pkgconfig(xrandr)
Recommends: pkgconfig(x11)

%description
OpenTabletDriver is an open source, cross platform, user mode tablet driver. The goal of OpenTabletDriver is to be cross platform as possible with the highest compatibility in an easily configurable graphical user interface.

%clean
rm -f %{_builddir}/LICENSE

%prep

%build

%install
cp -r %{pkg_dir}/* %{buildroot}/
rm %{buildroot}/LICENSE

cp %{pkg_dir}/LICENSE %{_builddir}

%post
udevadm control --reload-rules

%files
%defattr(-,root,root)
%license LICENSE
%dir /usr/share/OpenTabletDriver
/usr/share/OpenTabletDriver/*
/usr/lib/udev/rules.d/99-opentabletdriver.rules
/usr/share/pixmaps/otd.ico
/usr/share/pixmaps/otd.png
/usr/share/applications/OpenTabletDriver.desktop
/usr/bin/opentabletdriver
/usr/bin/otd
/usr/lib/systemd/user/opentabletdriver.service

%changelog