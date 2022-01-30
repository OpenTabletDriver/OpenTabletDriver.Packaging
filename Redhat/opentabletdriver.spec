# saves time so we don't have to download the thing manually
%undefine _disable_source_fetch
# We don't have debug symbols, because .NET
%define debug_package %{nil}
# We aren't using Mono but RPM expected Mono
%global __requires_exclude_from ^/usr/share/OpenTabletDriver/.*$

Name: opentabletdriver
Version: %ver
Release: 1
Summary: A cross-platform open source tablet driver
License: LGPLv3
BuildArch: x86_64

URL: https://github.com/OpenTabletDriver/OpenTabletDriver

# if devel_package is 1
%if 0%{?devel_package:1}
Source0: opentabletdriver-%{version}.tar.gz
%define otddir OpenTabletDriver
%else
Source0: https://github.com/OpenTabletDriver/OpenTabletDriver/archive/refs/tags/v%{version}.tar.gz
%define otddir OpenTabletDriver-%{version}
%endif

Source1: opentabletdriver-common-%{version}.tar.gz

#BuildRequires: dotnet-sdk-6.0

Requires: dotnet-runtime-6.0
Requires: pkgconfig(libevdev)
Requires: libevdev
Requires: gtk3
Recommends: pkgconfig(x11)
Recommends: pkgconfig(xrandr)
Recommends: libX11
Recommends: libXrandr

%description
OpenTabletDriver is an open source, cross platform, user mode tablet driver. The goal of OpenTabletDriver is to be cross platform as possible with the highest compatibility in an easily configurable graphical user interface.

%prep
%autosetup -a 0 -a 1 -n %{otddir}

%build
./build.sh
find ./bin -name "*.pdb" -type f -exec rm {} ';'
./generate-rules.sh ./99-opentabletdriver.rules

%install
%define common %{_builddir}/%{otddir}/Common/Linux
mkdir -p %{buildroot}%{_datadir}
mv bin/ %{buildroot}%{_datadir}/OpenTabletDriver/

# copy udev rules
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
install -D -m 644 ./99-opentabletdriver.rules %{buildroot}%{_prefix}/lib/udev/rules.d/99-opentabletdriver.rules

mkdir -p %{buildroot}%{_bindir}
# the commands and binaries
install -m 0755 %{common}/scripts/opentabletdriver %{buildroot}%{_bindir}/opentabletdriver
install -m 0755 %{common}/scripts/opentabletdriver %{buildroot}%{_bindir}/otd
# modprobe rules
mkdir -p %{buildroot}/usr/lib/modprobe.d
install -m 0644 %{common}/modprobe/99-opentabletdriver.conf %{buildroot}%{_prefix}/lib/modprobe.d/99-opentabletdriver.conf
# systemd stuff
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user
install -m 0755 %{common}/systemd-user/opentabletdriver.service %{buildroot}%{_prefix}/lib/systemd/user/opentabletdriver.service

# finally, the desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0755 %{common}/desktop/OpenTabletDriver.desktop %{buildroot}%{_datadir}/applications/OpenTabletDriver.desktop
sed -i "s/Version: .\+$/Version: %{version}/g" %{buildroot}%{_datadir}/applications/OpenTabletDriver.desktop

# then desktop icons
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp -v OpenTabletDriver.UX/Assets/otd.ico OpenTabletDriver.UX/Assets/otd.png %{buildroot}%{_datadir}/pixmaps/

# license doc
mkdir -p %{buildroot}%{_defaultdocdir}/OpenTabletDriver
install -m 0644 %{common}/license/copyright %{buildroot}%{_defaultdocdir}/OpenTabletDriver/copyright

# man doc
mkdir -p %{buildroot}%{_mandir}/man8
gzip -c docs/manpages/opentabletdriver.8 > %{buildroot}%{_mandir}/man8/opentabletdriver.8.gz

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
