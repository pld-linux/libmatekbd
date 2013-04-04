Summary:	Libraries for mate kbd
Name:		libmatekbd
Version:	1.6.0
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	9e17f7cc984c2723821d30375c5d7f2a
URL:		http://wiki.mate-desktop.org/libmatekbd
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.18
BuildRequires:	gtk+2-devel
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libxklavier-devel
BuildRequires:	mate-common >= 1.5
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries for matekbd

%package devel
Summary:	Development libraries for libmatekbd
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development libraries for libmatekbd

%prep
%setup -q

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-silent-rules \
	--disable-static
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
%doc AUTHORS README
%{_datadir}/libmatekbd
%{_datadir}/glib-2.0/schemas/org.mate.peripherals-keyboard-xkb.gschema.xml
%attr(755,root,root) %{_libdir}/libmatekbd.so.*.*.*
%ghost %{_libdir}/libmatekbd.so.4
%attr(755,root,root) %{_libdir}/libmatekbdui.so.*.*.*
%ghost %{_libdir}/libmatekbdui.so.4

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmatekbdui.so
%{_libdir}/libmatekbd.so
%{_includedir}/libmatekbd
%{_pkgconfigdir}/libmatekbd.pc
%{_pkgconfigdir}/libmatekbdui.pc
