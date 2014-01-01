#
# Conditional build:
%bcond_with	gtk3	# use GTK+ 3.x instead of 2.x
#
Summary:	MATE keyboard libraries
Summary(pl.UTF-8):	Biblioteki MATE do obsługi klawiatury
Name:		libmatekbd
Version:	1.6.2
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	35880a6bc967ed3093e7c46a58958b1f
URL:		http://wiki.mate-desktop.org/libmatekbd
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.18}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libxklavier-devel >= 5.0
BuildRequires:	mate-common >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	/sbin/ldconfig
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.18}
%{?with_gtk3:Requires:	gtk+3 >= 3.0}
Requires:	libxklavier >= 5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE keyboard libraries (fork of libgnomekbd).

%description -l pl.UTF-8
Biblioteki MATE do obsługi klawiatury (odgałęzienie z libgnomekbd).

%package devel
Summary:	Development files for libmatekbd
Summary(pl.UTF-8):	Pliki programistyczne bibliotek libmatekbd
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.26
%{!?with_gtk3:Requires:	gtk+2-devel >= 2:2.18}
%{?with_gtk3:Requires:	gtk+3-devel >= 3.0}
Requires:	libxklavier-devel >= 5.0

%description devel
Development files for libmatekbd.

%description devel -l pl.UTF-8
Pliki programistyczne bibliotek libmatekbd.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--disable-static \
	%{?with_gtk3:--with-gtk=3.0}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/matekbd.convert

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%glib_compile_schemas
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libmatekbd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmatekbd.so.4
%attr(755,root,root) %{_libdir}/libmatekbdui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmatekbdui.so.4
%{_datadir}/libmatekbd
%{_datadir}/glib-2.0/schemas/org.mate.peripherals-keyboard-xkb.gschema.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmatekbdui.so
%attr(755,root,root) %{_libdir}/libmatekbd.so
%{_includedir}/libmatekbd
%{_pkgconfigdir}/libmatekbd.pc
%{_pkgconfigdir}/libmatekbdui.pc
