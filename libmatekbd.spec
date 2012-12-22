Summary:	Libraries for mate kbd
Name:		libmatekbd
Version:	1.5.0
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
URL:		http://mate-desktop.org/
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	aa3781beb79ceb8126df589cea481140
BuildRequires:	desktop-file-utils
BuildRequires:	mate-common
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libxklavier)
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
	--disable-static
%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' | xargs rm

#desktop-file-install \
#	--remove-category="MATE" \
#	--add-category="X-Mate" \
#	--delete-original \
#	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
#$RPM_BUILD_ROOT%{_desktopdir}/matekbd-indicator-plugins-capplet.desktop

%find_lang %{name} --all-name

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
%doc AUTHORS COPYING.LIB README
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
