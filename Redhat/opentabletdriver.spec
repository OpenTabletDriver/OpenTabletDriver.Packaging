# saves time so we don't have to download the thing manually
%undefine _disable_source_fetch
# We don't have debug symbols, because .NET
%define debug_package %{nil}

Name: opentabletdriver
Version: 0.6.0.2
Release: 1
Summary: A cross-platform open source tablet driver
BuildArch: x86_64
# We aren't using Mono but RPM expected Mono
%global __requires_exclude_from ^/usr/share/OpenTabletDriver/.*$

%if 0%{?suse_version}
License: LGPL-3.0-only
Group: Hardware/Other
%else
License: LGPLv3
%endif

URL: https://github.com/OpenTabletDriver/OpenTabletDriver
# if devel_package is 1
%if 0%{?devel_package:1}
Source0: opentabletdriver.tar.gz
%else
Source0: https://github.com/OpenTabletDriver/OpenTabletDriver/archive/refs/tags/v%{version}.tar.gz
%endif
# commands and binaries
Source1: opentabletdriver
Source2: otd

#modprobe rules
Source3: 99-opentabletdriver.conf
# systemd
Source4: opentabletdriver.service
Source5: 50-opentabletdriver.preset
Source6: OpenTabletDriver.desktop

BuildRequires: dotnet-sdk-6.0
BuildRequires: systemd-rpm-macros
BuildRequires: libX11-devel
BuildRequires: libXrandr-devel
BuildRequires: gtk3-devel
Requires: dotnet-runtime-6.0
Requires: pkgconfig(libevdev)
Requires: libX11
Requires: libXrandr
Requires: libevdev
Requires: gtk3
Requires: libX11-devel
Requires: libXrandr-devel
Requires: gtk3-devel
Recommends: pkgconfig(xrandr)
Recommends: pkgconfig(x11)

%description
OpenTabletDriver is an open source, cross platform, user mode tablet driver. The goal of OpenTabletDriver is to be cross platform as possible with the highest compatibility in an easily configurable graphical user interface.

%clean
rm -f %{_builddir}/LICENSE

%prep
%if 0%{?devel_package:1}
%autosetup -n OpenTabletDriver
%else
%autosetup -n OpenTabletDriver-%{version}
%endif
%build
./build.sh

%install

mkdir -p %{buildroot}%{_datadir}
mv bin/ %{buildroot}%{_datadir}/OpenTabletDriver/

# copy udev rules
./generate-rules.sh
mkdir -p %{buildroot}/etc/udev/rules.d
install -D -m 644 ./bin/99-opentabletdriver.rules %{buildroot}/usr/lib/udev/rules.d/99-opentabletdriver.rules

mkdir -p %{buildroot}%{_bindir}
# the commands and binaries
install -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/opentabletdriver
install -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/otd
# modprobe rules
mkdir -p %{buildroot}/usr/lib/modprobe.d
install -m 0644 %{SOURCE3} %{buildroot}/usr/lib/modprobe.d/99-opentabletdriver.conf
# systemd stuff
mkdir -p %{buildroot}%{_userunitdir}
install -m 0644 %{SOURCE4} %{buildroot}%{_userunitdir}/opentabletdriver.service
mkdir -p %{buildroot}/usr/lib/systemd/user-preset/
install -m 0644 %{SOURCE5} %{buildroot}/usr/lib/systemd/user-preset/50-opentabletdriver.preset

# finally, the desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0644 %{SOURCE6} %{buildroot}%{_datadir}/applications/OpenTabletDriver.desktop

# then desktop icons
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp -rv OpenTabletDriver.UX/Assets/* %{buildroot}%{_datadir}/pixmaps/

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
%license LICENSE
%dir %{_datadir}/OpenTabletDriver
%{_datadir}/OpenTabletDriver/
/usr/lib/udev/rules.d/99-opentabletdriver.rules
/usr/lib/modprobe.d/99-opentabletdriver.conf
%{_datadir}/pixmaps/otd.ico
%{_datadir}/pixmaps/otd.png
%{_datadir}/applications/OpenTabletDriver.desktop
%{_bindir}/opentabletdriver
%{_bindir}/otd
/usr/lib/systemd/user/opentabletdriver.service
/usr/lib/systemd/user-preset/50-opentabletdriver.preset

%changelog
