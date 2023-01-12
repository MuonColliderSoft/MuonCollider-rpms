%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_sio_dir %{_libdir}/cmake/sio

Summary: Persistency solution for reading and writing binary data
Name: ilc-sio
Version: 0.0.2
Release: 1%{?dist}
License: BSD v.3
Vendor: DESY/SLAC
URL: https://github.com/iLCSoft/SIO
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: zlib-devel
BuildRequires: chrpath
Conflicts: ilc-lcio
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
SIO is a persistency solution for reading and writing binary data
in SIO structures called record and block. SIO has originally been
implemented as persistency layer for LCIO.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=17 \
             -DSIO_BUILTIN_ZLIB=OFF \
             -DSIO_EXAMPLES=OFF \
             -DSIO_MACROS_WITH_EXCEPTION=OFF \
             -DSIO_RELEASE_OFAST=OFF \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}

%install
cd %{_builddir}/%{name}-%{version}/build
make %{?_smp_mflags}
make install
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_sio_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{_libdir}/cmake/*.cmake %{buildroot}%{cmake_sio_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_sio_dir}/*.cmake
sed -i -e 's|lib/cmake|lib64/cmake/sio|g' %{buildroot}%{cmake_sio_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*

%package devel
Summary: Persistency solution for reading and writing binary data (development files)
Requires: %{name}
Requires: zlib-devel
Conflicts: ilc-lcio-devel

%description devel
SIO is a persistency solution for reading and writing binary data
in SIO structures called record and block. SIO has originally been
implemented as persistency layer for LCIO.

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%dir %{_includedir}/sio
%dir %{_includedir}/sio/compression
%{_includedir}/sio/*.h
%{_includedir}/sio/compression/*.h
%dir %{cmake_sio_dir}
%{cmake_sio_dir}/*.cmake



%changelog
* Mon Mar 23 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.0.2-1
- Repackaging for CentOS 8














