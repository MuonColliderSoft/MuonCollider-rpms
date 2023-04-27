%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 2.17.0
%global _tagver 02-17-MC

%global _sbuilddir %{_builddir}/%{name}-%{version}/LCIO-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_lcio_dir %{_libdir}/cmake/lcio

Summary: Event data model and persistency for Linear Collider detector
Name: ilc-lcio
Version: %{_pver}
Release: 1%{?dist}
License: BSD v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/LCIO
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: python3
BuildRequires: python3-rpm-macros
BuildRequires: zlib-devel
BuildRequires: chrpath
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/LCIO/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
LCIO (Linear Collider I/O) provides the event data model (EDM)
and persistency solution for Linear Collider detector R&D studies.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DBUILD_ROOTDICT=ON  \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
#mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mv %{buildroot}%{_includedir} %{buildroot}/lcio-includedir
mkdir -p %{buildroot}%{_includedir}
mv %{buildroot}/lcio-includedir %{buildroot}%{_includedir}/lcio
mkdir -p %{buildroot}%{cmake_lcio_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{_libdir}/cmake/*.cmake %{buildroot}%{cmake_lcio_dir}
sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' %{buildroot}%{cmake_lcio_dir}/*.cmake
sed -i -e 's|lib64/cmake|lib64/cmake/lcio|g' %{buildroot}%{cmake_lcio_dir}/*.cmake
sed -i -e 's|PATHS|PATHS %{_includedir}/lcio|g' %{buildroot}%{cmake_lcio_dir}/LCIOConfig.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*
chrpath --replace %{_libdir} \
                  %{buildroot}%{_bindir}/addRandomAccess \
                  %{buildroot}%{_bindir}/c* \
                  %{buildroot}%{_bindir}/d* \
                  %{buildroot}%{_bindir}/l* \
                  %{buildroot}%{_bindir}/p* \
                  %{buildroot}%{_bindir}/r* \
                  %{buildroot}%{_bindir}/s*
sed -i -e 's|env python|env python3|g' %{buildroot}%{_bindir}/anajob

mkdir -p %{buildroot}%{python3_sitelib}
mv %{buildroot}/usr/python/*.py  %{buildroot}/usr/python/pyLCIO %{buildroot}%{python3_sitelib}
rm -rf %{buildroot}/usr/python

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.pcm
%{_libdir}/*.a

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
%dir %{_includedir}/lcio/sio
%dir %{_includedir}/lcio/SIO
%dir %{_includedir}/lcio/pre-generated
%dir %{_includedir}/lcio/pre-generated/EVENT
%dir %{_includedir}/lcio/pre-generated/IO
%{_includedir}/lcio/*.h
%{_includedir}/lcio/DATA/*
%{_includedir}/lcio/EVENT/*
%{_includedir}/lcio/IMPL/*
%{_includedir}/lcio/IO/*
%{_includedir}/lcio/IOIMPL/*
%{_includedir}/lcio/MT/*
%{_includedir}/lcio/UTIL/*
%{_includedir}/lcio/rootDict/*
%{_includedir}/lcio/*
%{_includedir}/lcio/SIO/*
%{_includedir}/lcio/pre-generated/EVENT/*
%{_includedir}/lcio/pre-generated/IO/*
%{cmake_lcio_dir}
%{cmake_lcio_dir}/*.cmake

%package -n python3-lcio
Summary: Event data model and persistency for Linear Collider detector (python files)
BuildArch: noarch
Requires: %{name}
Requires: python3
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
%dir %{python3_sitelib}/pyLCIO/__pycache__
%dir %{python3_sitelib}/pyLCIO/base/__pycache__
%dir %{python3_sitelib}/pyLCIO/drivers/__pycache__
%dir %{python3_sitelib}/pyLCIO/exceptions/__pycache__
%dir %{python3_sitelib}/pyLCIO/io/__pycache__
%{python3_sitelib}/__pycache__/*.pyc
%{python3_sitelib}/pyLCIO/__pycache__/*.pyc
%{python3_sitelib}/pyLCIO/base/__pycache__/*.pyc
%{python3_sitelib}/pyLCIO/drivers/__pycache__/*.pyc
%{python3_sitelib}/pyLCIO/exceptions/__pycache__/*.pyc
%{python3_sitelib}/pyLCIO/io/__pycache__/*.pyc

%changelog
* Tue Feb 28 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.17.0-1
- New version of LCIO
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.16.1-1
- New version of LCIO
* Fri Nov 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.15.4-1
- Fork for MuonColliderSoft
* Mon Mar 23 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.13.1-1
- Repackaging for CentOS 8














