%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 2.20.2
%global _tagver 02-20-02-MC

%global _sbuilddir %{_builddir}/%{name}-%{version}/LCIO-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_lcio_dir %{_libdir}/cmake/LCIO

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
BuildRequires: patch
BuildRequires: python3
BuildRequires: python3-rpm-macros
BuildRequires: zlib-devel
BuildRequires: chrpath
BuildRequires: root
BuildRequires: ilc-lcio-headers
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#Source0: https://github.com/MuonColliderSoft/LCIO/archive/refs/tags/v%{_tagver}.tar.gz
Source0: v%{_tagver}.tar.gz
Patch0: ilc-lcio-new-headers.patch
AutoReqProv: yes

%description
LCIO (Linear Collider I/O) provides the event data model (EDM)
and persistency solution for Linear Collider detector R&D studies.

%prep
%setup -c
patch %{_sbuilddir}/CMakeLists.txt %{PATCH0}
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
rm -rf %{buildroot}%{_includedir}/*
mv %{buildroot}%{_libdir}/cmake/*.cmake %{buildroot}%{cmake_lcio_dir}
ln -s %{buildroot}%{_libdir}/cmake/SIO/SIOTargets-relwithdebinfo.cmake \
      %{buildroot}%{cmake_lcio_dir}/SIOTargets-relwithdebinfo.cmake
ln -s %{buildroot}%{_libdir}/cmake/SIO/SIOTargets.cmake \
      %{buildroot}%{cmake_lcio_dir}/SIOTargets.cmake
sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' \
       -e 's|lib64/cmake|lib64/cmake/LCIO|g' %{buildroot}%{cmake_lcio_dir}/*.cmake
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
%{_libdir}/*.so*
%{_libdir}/*.pcm

%package devel
Summary: Event data model and persistency for Linear Collider detector (development files)
Requires: %{name}
Requires: ilc-lcio-headers

%description devel
LCIO (Linear Collider I/O) provides the event data model (EDM)
and persistency solution for Linear Collider detector R&D studies.

%files devel
%defattr(-,root,root)
%dir %{cmake_lcio_dir}
%{cmake_lcio_dir}/*.cmake
%dir %{_libdir}/cmake/SIO
%{_libdir}/cmake/SIO/*.cmake

%package -n python3-lcio
Summary: Event data model and persistency for Linear Collider detector (python files)
BuildArch: noarch
Requires: %{name}
Requires: ilc-lcio-headers
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

%package tools
Summary: Event data model and persistency for Linear Collider detector (tools)
Requires: python3-lcio

%description tools
LCIO (Linear Collider I/O) provides the event data model (EDM)
and persistency solution for Linear Collider detector R&D studies.

%files tools
%defattr(-,root,root)
%{_bindir}/*

%changelog
* Tue Feb 28 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.17.0-1
- New version of LCIO
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.16.1-1
- New version of LCIO
* Fri Nov 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.15.4-1
- Fork for MuonColliderSoft
* Mon Mar 23 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.13.1-1
- Repackaging for CentOS 8














