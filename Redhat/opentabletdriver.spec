Name: opentabletdriver
Version: 0.0.0
Release: 1
Summary: A cross-platform open source tablet driver
License: LGPLv3
URL: https://github.com/OpenTabletDriver/OpenTabletDriver

Source0: opentabletdriver-%{version}.tar.gz
Source1: opentabletdriver-linux-common.tar.gz

AutoReqProv: no
Requires: dotnet-runtime-6.0
Requires: pkgconfig(libevdev)
Requires: gtk3
Recommends: pkgconfig(xrandr)
Recommends: pkgconfig(x11)

%description
OpenTabletDriver is an open source, cross platform, user mode tablet driver. The goal of OpenTabletDriver is to be cross platform as possible with the highest compatibility in an easily configurable graphical user interface.

%prep
%autosetup -a 0 -a 1 -n OpenTabletDriver

%build
./build.sh
find ./bin -name "*.pdb" -type f -exec rm {} ';'

%install
mkdir -p %{buildroot}/%{_datadir}/OpenTabletDriver
cp -r bin/* %{buildroot}/%{_datadir}/OpenTabletDriver

cp -r Common/Linux/* %{buildroot}/%{_prefix}

mkdir -p %{buildroot}/%{_mandir}/man8
gzip -c docs/manpages/opentabletdriver.8 > %{buildroot}/%{_mandir}/man8/opentabletdriver.8.gz

mkdir -p %{buildroot}/%{_datadir}/pixmaps
cp -v OpenTabletDriver.UX/Assets/* %{buildroot}/%{_datadir}/pixmaps

mkdir -p %{buildroot}/%{_prefix}/lib/udev/rules.d
./generate-rules.sh -v OpenTabletDriver.Configurations/Configurations %{buildroot}/%{_prefix}/lib/udev/rules.d/99-opentabletdriver.rules

sed -i "s/^Version=.\+$/Version=%{version}/g" "%{buildroot}/%{_datadir}/applications/OpenTabletDriver.desktop"

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
