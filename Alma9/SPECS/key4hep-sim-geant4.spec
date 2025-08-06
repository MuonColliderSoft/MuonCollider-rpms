%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.99.16
%global _tagver 0.1.0pre16

%global _sbuilddir %{_builddir}/%{name}-%{version}/k4SimGeant4-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_k4sim_dir %{_libdir}/cmake/k4SimGeant4

Summary: Gaudi Components for Geant4 Simulation in the Key4hep software framework.
Name: key4hep-sim-geant4
Version: %{_pver}
Release: 1%{?dist}
License: Apache License 2.0
URL: https://github.com/key4hep/k4SimGeant4
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: key4hep-fw-core-devel
BuildRequires: python3-podio-utils

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/key4hep/k4SimGeant4/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Gaudi Components for Geant4 Simulation in the Key4hep software framework.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=20 \
      -DBUILD_TESTING=OFF \
      -DBUILD_DOCS=OFF \
      -DCPPGSL_INCLUDE_DIR=/opt/GSL/include \
      -DCMAKE_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
chrpath --delete %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{cmake_k4sim_dir}
mv %{buildroot}%{_prefix}/lib/cmake/k4SimGeant4/* %{buildroot}%{cmake_k4sim_dir}
rm -rf %{buildroot}%{_prefix}/lib

mkdir -p %{buildroot}%{python3_sitelib}
mv %{buildroot}%{_prefix}/python/DetComponents \
   %{buildroot}%{_prefix}/python/DetStudies \
   %{buildroot}%{_prefix}/python/SimG4Components \
   %{buildroot}%{_prefix}/python/SimG4Fast \
   %{buildroot}%{_prefix}/python/SimG4Full \
   %{buildroot}%{python3_sitelib}/
rm -rf %{buildroot}%{_prefix}/python

sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' %{buildroot}%{cmake_k4sim_dir}/*.cmake

rm -rf %{buildroot}%{_datadir}

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.components
%{_libdir}/*.confdb
%{_libdir}/*.confdb2

%package devel
Summary: Gaudi Components for Geant4 Simulation in the Key4hep software framework (development files).
Requires: %{name}
Requires: key4hep-fw-core-devel

%description devel
Gaudi Components for Geant4 Simulation in the Key4hep software framework.

%files devel
%defattr(-,root,root)
%dir %{cmake_k4sim_dir}
%{cmake_k4sim_dir}/*.cmake
%{cmake_k4sim_dir}/*.csv
%dir %{_includedir}/SimG4Common
%dir %{_includedir}/SimG4Fast
%dir %{_includedir}/SimG4Full
%dir %{_includedir}/SimG4Interface
%{_includedir}/SimG4Common/*.h
%{_includedir}/SimG4Fast/*.h
%{_includedir}/SimG4Full/*.h
%{_includedir}/SimG4Interface/*.h


%package -n python3-k4sim-geant4
Summary: Gaudi Components for Geant4 Simulation in the Key4hep software framework (python modules).
BuildArch: noarch
Requires: %{name}
Requires: python3-k4fwcore

%description -n python3-k4sim-geant4
Gaudi Components for Geant4 Simulation in the Key4hep software framework.

%files -n python3-k4sim-geant4
%defattr(-,root,root)
%dir %{python3_sitelib}/DetComponents
%dir %{python3_sitelib}/DetComponents/__pycache__
%{python3_sitelib}/DetComponents/*.py
%{python3_sitelib}/DetComponents/__pycache__/*
%dir %{python3_sitelib}/DetStudies
%dir %{python3_sitelib}/DetStudies/__pycache__
%{python3_sitelib}/DetStudies/*.py
%{python3_sitelib}/DetStudies/__pycache__/*
%dir %{python3_sitelib}/SimG4Components
%dir %{python3_sitelib}/SimG4Components/__pycache__
%{python3_sitelib}/SimG4Components/*.py
%{python3_sitelib}/SimG4Components/__pycache__/*
%dir %{python3_sitelib}/SimG4Fast
%dir %{python3_sitelib}/SimG4Fast/__pycache__
%{python3_sitelib}/SimG4Fast/*.py
%{python3_sitelib}/SimG4Fast/__pycache__/*
%dir %{python3_sitelib}/SimG4Full
%dir %{python3_sitelib}/SimG4Full/__pycache__
%{python3_sitelib}/SimG4Full/*.py
%{python3_sitelib}/SimG4Full/__pycache__/*


%changelog
* Wed Aug 06 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.99.16-1
- Porting to AlmaLinux

