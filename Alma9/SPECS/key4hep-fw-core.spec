%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.9.19
%global _tagver 01-00pre19

%global _sbuilddir %{_builddir}/%{name}-%{version}/k4FWCore-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_k4fwcore_dir %{_libdir}/cmake/k4FWCore

Summary: Gaudi framework for podio-based event data models.
Name: key4hep-fw-core
Version: %{_pver}
Release: 1%{?dist}
License: Apache License 2.0
URL: https://github.com/key4hep/k4FWCore
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: podio-devel
BuildRequires: python3-podio-utils
BuildRequires: gaudi-devel
BuildRequires: gaudi-tools
BuildRequires: python3-rpm-macros

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/key4hep/k4FWCore/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
k4FWCore is a Gaudi package that provides the PodioDataService, 
which allows to use podio-based event data models like EDM4hep in Gaudi workflows.

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
      -DBUILD_TESTING=OFF \
      -DCPPGSL_INCLUDE_DIR=/opt/GSL/include \
      -DCMAKE_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
mv %{buildroot}%{_prefix}/lib/cmake/k4FWCore/* %{buildroot}%{cmake_k4fwcore_dir}
rm -rf %{buildroot}%{_prefix}/lib

mkdir -p %{buildroot}/%{python3_sitelib}
mv %{buildroot}/%{_prefix}/python/k4FWCore %{buildroot}/%{python3_sitelib}/
rm -rf %{buildroot}/%{_prefix}/python

sed -i -e 's|env python|env python3|g' %{buildroot}/%{_bindir}/*
sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' %{buildroot}%{cmake_k4fwcore_dir}/*.cmake

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.components
%{_libdir}/*.confdb
%{_libdir}/*.confdb2
%{_bindir}/*

%package devel
Summary: Gaudi framework for podio-based event data models (development files).
Requires: %{name}
Requires: podio-devel
Requires: gaudi-devel

%description devel
k4FWCore is a Gaudi package that provides the PodioDataService, 
which allows to use podio-based event data models like EDM4hep in Gaudi workflows.

%files devel
%defattr(-,root,root)
%dir %{cmake_k4fwcore_dir}
%{cmake_k4fwcore_dir}/*.cmake
%{cmake_k4fwcore_dir}/*.csv
%dir %{_includedir}/k4FWCore
%dir %{_includedir}/k4Interface
%{_includedir}/k4FWCore/*.h
%{_includedir}/k4Interface/*.h

%package -n python3-k4fwcore
Summary: A generic event data model for future HEP collider experiments (python modules).
BuildArch: noarch
Requires: %{name}
Requires: python3-gaudi

%description -n python3-k4fwcore
A generic event data model for future HEP collider experiments.

%files -n python3-k4fwcore
%defattr(-,root,root)
%dir %{python3_sitelib}/k4FWCore
%dir %{python3_sitelib}/k4FWCore/__pycache__
%{python3_sitelib}/k4FWCore/*.py
%{python3_sitelib}/k4FWCore/__pycache__/*

%changelog
* Tue May 28 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.9.19-1
- Porting to AlmaLinux 9










