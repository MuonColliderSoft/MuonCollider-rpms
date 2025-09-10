%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.2.99
%global _tagver 0.2.99

%global _sbuilddir %{_builddir}/%{name}-%{version}/k4Reco-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_k4reco_dir %{_libdir}/cmake/k4Reco

Summary: Gaudi algorithms for reconstruction using EDM4hep natively.
Name: key4hep-reco
Version: %{_pver}
Release: 1%{?dist}
License: Apache License 2.0
URL: https://github.com/key4hep/k4Reco
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: key4hep-fw-core-devel
BuildRequires: python3-podio-utils
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-ddkaltest-devel
BuildRequires: key4hep-sim-geant4-devel
BuildRequires: key4hep-geo-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://nexus.pd.infn.it/artifacts/repository/misc/k4Reco-%{_tagver}.tar.gz
Patch0: key4hep-reco-lcio-setup.patch
AutoReqProv: yes

%description
Gaudi algorithms for reconstruction using EDM4hep natively.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}
patch %{_sbuilddir}/CMakeLists.txt %{PATCH0}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}

# TODO investigate the following workaround (RPM custom options for the build)
unset CFLAGS
unset CXXFLAGS
unset LDFLAGS

cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=20 \
      -DBUILD_TESTING=OFF \
      -DCPPGSL_INCLUDE_DIR=/opt/GSL/include \
      -DCMAKE_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
chrpath --delete %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{cmake_k4reco_dir}
mv %{buildroot}%{_prefix}/lib/cmake/k4Reco/* %{buildroot}%{cmake_k4reco_dir}
rm -rf %{buildroot}%{_prefix}/lib/

mkdir -p %{buildroot}%{python3_sitelib}
mv %{buildroot}%{_prefix}/python/k4Reco \
   %{buildroot}%{_prefix}/python/conformal_tracking_utils \
   %{buildroot}%{python3_sitelib}
rm -rf %{buildroot}%{_prefix}/python

# mv %{buildroot}%{_includedir}/k4Reco/GaudiTrkUtils/include/*.h %{buildroot}%{_includedir}/k4Reco
# rm -rf %{buildroot}%{_includedir}/k4Reco/GaudiTrkUtils

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
Summary: Gaudi algorithms for reconstruction using EDM4hep natively (development files).
Requires: %{name}
Requires: key4hep-fw-core-devel
Requires: ilc-lcio-devel
Requires: ilc-ddkaltest-devel
Requires: key4hep-sim-geant4-devel
Requires: key4hep-geo-devel

%description devel
Gaudi algorithms for reconstruction using EDM4hep natively.

%files devel
%defattr(-,root,root)
%dir %{cmake_k4reco_dir}
%{cmake_k4reco_dir}/*
%dir %{_includedir}/k4Reco
%{_includedir}/k4Reco/*.h


%package -n python3-k4reco
Summary: Gaudi algorithms for reconstruction using EDM4hep natively (python modules).
BuildArch: noarch
Requires: %{name}
Requires: python3-k4fwcore
Requires: key4hep-sim-geant4

%description -n python3-k4reco
Gaudi algorithms for reconstruction using EDM4hep natively.

%files -n python3-k4reco
%defattr(-,root,root)
%dir %{python3_sitelib}/k4Reco
%dir %{python3_sitelib}/k4Reco/__pycache__
%{python3_sitelib}/k4Reco/*.py
%{python3_sitelib}/k4Reco/__pycache__/*
%dir %{python3_sitelib}/conformal_tracking_utils
%dir %{python3_sitelib}/conformal_tracking_utils/__pycache__
%{python3_sitelib}/conformal_tracking_utils/*.py
%{python3_sitelib}/conformal_tracking_utils/__pycache__/*


%changelog
* Tue Aug 26 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.2.99-1
- Porting to AlmaLinux

