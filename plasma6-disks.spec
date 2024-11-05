%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
%define plasmaver %(echo %{version} |cut -d. -f1-3)
#define git 20240222
%define gitbranch Plasma/6.0
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

Summary:	Hard disk health monitoring for KDE Plasma
Name:		plasma6-disks
Version:	6.2.3
Release:	%{?git:0.%{git}.}1
License:	GPL
Group:		Graphical desktop/KDE
URL:		https://kde.org
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/plasma-disks/-/archive/%{gitbranch}/plasma-disks-%{gitbranchd}.tar.bz2#/plasma-disks-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/plasma/%{plasmaver}/plasma-disks-%{version}.tar.xz
%endif
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(KF6DBusAddons)
BuildRequires:	cmake(KF6Declarative)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6KIO)
BuildRequires:	cmake(KF6Notifications)
BuildRequires:	cmake(KF6Service)
BuildRequires:	cmake(KF6Solid)
BuildRequires:	cmake(KF6Auth)
BuildRequires:	cmake(KF6Package)
BuildRequires:	cmake(KF6KCMUtils)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	smartmontools
BuildRequires:	gettext
Requires:	smartmontools

%description
Plasma Disks monitors S.M.A.R.T. data of disks and alerts the user when
signs of imminent failure appear.

%prep
%autosetup -n plasma-disks-%{?git:%{gitbranchd}}%{!?git:%{version}} -p1
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%find_lang %{name} --all-name

%files -f %{name}.lang
%license LICENSES/*.txt
%{_libdir}/libexec/kf6/kauth/kded-smart-helper
%{_datadir}/dbus-1/system-services/org.kde.kded.smart.service
%{_datadir}/dbus-1/system.d/org.kde.kded.smart.conf
%{_datadir}/metainfo/org.kde.plasma.disks.metainfo.xml
%{_datadir}/polkit-1/actions/org.kde.kded.smart.policy
%{_qtdir}/plugins/kf6/kded/smart.so
%{_qtdir}/plugins/plasma/kcms/kinfocenter/kcm_disks.so
%{_datadir}/applications/kcm_disks.desktop
%{_datadir}/knotifications6/org.kde.kded.smart.notifyrc
