Summary:	GNOME Bluetooth
Name:		gnome-bluetooth
Version:	3.12.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-bluetooth/3.12/%{name}-%{version}.tar.xz
# Source0-md5:	c23666aa1d0bfc37be38f45493679de2
Source1:	61-gnome-bluetooth-rfkill.rules
URL:		http://live.gnome.org/GnomeBluetooth
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gobject-introspection-devel >= 1.40.0
BuildRequires:	gtk+3-devel >= 3.12.0
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	libnotify-devel
BuildRequires:	libtool
BuildRequires:	nautilus-devel >= 3.12.0
BuildRequires:	pkg-config
BuildRequires:	udev-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bluez
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Bluetooth is a fork of bluez-gnome focused on integration
with the GNOME desktop environment

%package libs
Summary:	GNOME Bluetooth libraries
License:	LGPL
Group:		Development/Libraries

%description libs
GNOME bluetooth shared libraries.

%package devel
Summary:	Header files for GNOME bluetooth subsystem
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for GNOME Bluetooth subsystem.

%package apidocs
Summary:	GNOME Bluetooth API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GNOME Bluetooth API documentation.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%{__sed} -i 's/$(LIBGNOMEBT_LIBS)/$(LIBGNOMEBT_LIBS) -lm/' \
    lib/Makefile.am

%build
%{__libtoolize}
%{__gtkdocize}
%{__intltoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-desktop-update	\
	--disable-icon-update		\
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-static		\
	--with-html-dir=%{_gtkdocdir}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/en@shaw

%find_lang %{name} --with-gnome --all-name

install -D %{SOURCE1} \
	$RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d//61-gnome-bluetooth-rfkill.rules

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_icon_cache hicolor
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_iconsdir}/hicolor/*/status/*
%{_prefix}/lib/udev/rules.d//61-gnome-bluetooth-rfkill.rules
%{_mandir}/man1/bluetooth-*.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgnome-bluetooth.so.??
%attr(755,root,root) %{_libdir}/libgnome-bluetooth.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/%{name}
%{_pkgconfigdir}/gnome-bluetooth-1.0.pc
%{_datadir}/gir-1.0/GnomeBluetooth-1.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}

