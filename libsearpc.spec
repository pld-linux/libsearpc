#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	A simple and easy-to-use C language RPC framework
Name:		libsearpc
Version:	3.0.7
Release:	1
License:	LGPL v3
Group:		Libraries
Source0:	https://github.com/haiwen/libsearpc/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1d20e93e0fb39f98c907e633d9f1b11b
URL:		https://github.com/haiwen/libsearpc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	jansson-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-pygobject
BuildRequires:	python-simplejson
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Searpc is a simple C language RPC framework based on GObject system.
Searpc handles the serialization/deserialization part of RPC, the
transport part is left to users.

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel
Requires:	jansson-devel >= 2.2.1

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn %{name}-%{version}

# meh is this?
sed -i -e 's/(DESTDIR)//' %{name}.pc.in

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-compile-demo \
	--disable-static

%{__make}
%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsearpc.la

mv $RPM_BUILD_ROOT%{_bindir}/searpc-codegen{.py,}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.markdown AUTHORS COPYING
%attr(755,root,root) %{_libdir}/libsearpc.so.*.*.*
%ghost %{_libdir}/libsearpc.so.1
%attr(755,root,root) %{_bindir}/searpc-codegen
%{py_sitedir}/pysearpc

%files devel
%defattr(644,root,root,755)
%doc COPYING
%{_includedir}/searpc-client.h
%{_includedir}/searpc-server.h
%{_includedir}/searpc-utils.h
%{_includedir}/searpc.h
%{_libdir}/libsearpc.so
%{_pkgconfigdir}/libsearpc.pc
