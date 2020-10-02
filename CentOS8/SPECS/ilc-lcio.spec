%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_lcio_dir %{_libdir}/cmake/lcio
%global _pypkg python36

Summary: Event data model and persistency for Linear Collider detector
Name: ilc-lcio
Version: 2.15.3
Release: 1%{?dist}
License: BSD v.3
Vendor: DESY/SLAC
URL: https://github.com/iLCSoft/LCIO
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: %{_pypkg}
BuildRequires: %{_pypkg}-rpm-macros
BuildRequires: zlib-devel
BuildRequires: chrpath
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
LCIO (Linear Collider I/O) provides the event data model (EDM)
and persistency solution for Linear Collider detector R&D studies.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=14 \
             -DBUILD_ROOTDICT=ON  \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mv %{buildroot}%{_includedir} %{buildroot}/lcio-includedir
mkdir -p %{buildroot}%{_includedir}
mv %{buildroot}/lcio-includedir %{buildroot}%{_includedir}/lcio
mkdir -p %{buildroot}%{cmake_lcio_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{_libdir}/cmake/*.cmake %{buildroot}%{cmake_lcio_dir}
sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' %{buildroot}%{cmake_lcio_dir}/*.cmake
sed -i -e 's|lib/cmake|lib64/cmake/lcio|g' %{buildroot}%{cmake_lcio_dir}/*.cmake
sed -i -e 's|PATHS|PATHS %{_includedir}/lcio|g' %{buildroot}%{cmake_lcio_dir}/LCIOConfig.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/*

mkdir -p %{buildroot}%{python3_sitelib}
mv %{buildroot}/usr/python/*.py  %{buildroot}/usr/python/pyLCIO %{buildroot}%{python3_sitelib}
rm -rf %{buildroot}/usr/python

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.pcm

%package devel
Summary: Event data model and persistency for Linear Collider detector (development files)
Requires: %{name}
Requires: root
Requires: zlib-devel

%description devel
LCIO (Linear Collider I/O) provides the event data model (EDM)
and persistency solution for Linear Collider detector R&D studies.

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%dir %{_includedir}/lcio
%dir %{_includedir}/lcio/DATA
%dir %{_includedir}/lcio/EVENT
%dir %{_includedir}/lcio/IMPL
%dir %{_includedir}/lcio/IO
%dir %{_includedir}/lcio/IOIMPL
%dir %{_includedir}/lcio/MT
%dir %{_includedir}/lcio/UTIL
%dir %{_includedir}/lcio/rootDict
%{_includedir}/lcio/*.h
%{_includedir}/lcio/DATA/*
%{_includedir}/lcio/EVENT/*
%{_includedir}/lcio/IMPL/*
%{_includedir}/lcio/IO/*
%{_includedir}/lcio/IOIMPL/*
%{_includedir}/lcio/MT/*
%{_includedir}/lcio/UTIL/*
%{_includedir}/lcio/rootDict/*
%dir %{cmake_lcio_dir}
%{cmake_lcio_dir}/*.cmake

%package -n python3-lcio
Summary: Event data model and persistency for Linear Collider detector (python files)
BuildArch: noarch
Requires: %{name}
Requires: %{_pypkg}
Requires: python3-root

%description -n python3-lcio
LCIO (Linear Collider I/O) provides the event data model (EDM)
and persistency solution for Linear Collider detector R&D studies.

%files -n python3-lcio
%defattr(-,root,root)
%dir %{python3_sitelib}/pyLCIO
%dir %{python3_sitelib}/pyLCIO/base
%dir %{python3_sitelib}/pyLCIO/drivers
%dir %{python3_sitelib}/pyLCIO/exceptions
%dir %{python3_sitelib}/pyLCIO/io
%{python3_sitelib}/*.py
%{python3_sitelib}/pyLCIO/*.py
%{python3_sitelib}/pyLCIO/base/*.py
%{python3_sitelib}/pyLCIO/drivers/*.py
%{python3_sitelib}/pyLCIO/exceptions/*.py
%{python3_sitelib}/pyLCIO/io/*.py

%changelog
* Fri Oct 02 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.15.3-1
- New version of LCIO
* Mon Mar 23 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.13.1-1
- Repackaging for CentOS 8














