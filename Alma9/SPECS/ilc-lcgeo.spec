%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.20.0
%global _tagver 00-20-RC1

%global _sbuilddir %{_builddir}/%{name}-%{version}/lcgeo-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global _pgeoname muonc-detector-geometry

Summary: Implementation of Linear Collider detector models in DD4hep.
Name: ilc-lcgeo
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/lcgeo
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: aida-dd4hep-devel
BuildRequires: chrpath
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/lcgeo/archive/refs/tags/v%{_tagver}.tar.gz
Patch0: ilc-lcgeo_lcio_incdir.patch
AutoReqProv: yes

%description
Implementation of Linear Collider detector models in DD4hep.

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
      -DBUILD_TESTING=OFF \
      -DINSTALL_MUONC_FILES=ON \
      -DMUONC_GEO_DIR=%{buildroot}%{_datadir}/%{_pgeoname} \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so
rm -rf %{buildroot}%{_includedir}/detectorSegmentations
rm -rf %{buildroot}%{_libdir}/cmake/k4geo
rm -rf %{buildroot}%{_includedir}/detectorCommon

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.components

%package -n %{_pgeoname}
Summary: The Muon Collider detector geometry
BuildArch: noarch
Requires: ilc-lcgeo

%description -n %{_pgeoname}
The Muon Collider detector geometry.

%files -n %{_pgeoname}
%defattr(-,root,root)
%dir %{_datadir}/%{_pgeoname}
%dir %{_datadir}/%{_pgeoname}/MuColl_v0
%{_datadir}/%{_pgeoname}/MuColl_v0/*.xml
%dir %{_datadir}/%{_pgeoname}/MuColl_v1
%{_datadir}/%{_pgeoname}/MuColl_v1/*.xml
%dir %{_datadir}/%{_pgeoname}/MuColl_v1.0.1
%{_datadir}/%{_pgeoname}/MuColl_v1.0.1/*.xml
%dir %{_datadir}/%{_pgeoname}/MuColl_v1.0.2
%{_datadir}/%{_pgeoname}/MuColl_v1.0.2/*.xml
%dir %{_datadir}/%{_pgeoname}/MuColl_v1.1
%dir %{_datadir}/%{_pgeoname}/MuColl_v1.1/include
%{_datadir}/%{_pgeoname}/MuColl_v1.1/*.xml
%{_datadir}/%{_pgeoname}/MuColl_v1.1/include/*.xml
%dir %{_datadir}/%{_pgeoname}/MuColl_v1.1.1
%dir %{_datadir}/%{_pgeoname}/MuColl_v1.1.1/include
%{_datadir}/%{_pgeoname}/MuColl_v1.1.1/*.xml
%{_datadir}/%{_pgeoname}/MuColl_v1.1.1/include/*.xml
%dir %{_datadir}/%{_pgeoname}/MuColl_v1.1.2
%dir %{_datadir}/%{_pgeoname}/MuColl_v1.1.2/include
%{_datadir}/%{_pgeoname}/MuColl_v1.1.2/*.xml
%{_datadir}/%{_pgeoname}/MuColl_v1.1.2/include/*.xml
%dir %{_datadir}/%{_pgeoname}/MuColl_v1.1.3
%dir %{_datadir}/%{_pgeoname}/MuColl_v1.1.3/include
%{_datadir}/%{_pgeoname}/MuColl_v1.1.3/*.xml
%{_datadir}/%{_pgeoname}/MuColl_v1.1.3/include/*.xml

%changelog
* Wed Jun 26 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.20.0-1
- Imported changes from Key4HEP
* Wed Apr 26 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.18.1-1
- Imported changes from Key4HEP
* Mon Dec 21 2020 Nazar Bartosik <nazar.bartosik@cern.ch> - 0.16.8-1
- Fixed a bug with reflected slices in TrackerEndcapSupport_o1_v02
- Recovered the double thickness bug in TrackerEndcapSupport_o1_v01
- Fixed double thickness in the negative side of TrackerEndcapSupport
* Mon Sep 21 2020 Nazar Bartosik <nazar.bartosik@to.infn.it> - 0.16.6-1
- Added a modified version of the Generic Cal Endcap without cutout
- Added support of Z segmentation to ZPlanarTracker class
- Implemented Z segmentation in a separate plugin: ZSegmentedPlanarTracker
* Fri Apr 03 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.16.5-1
- Repackaging for CentOS 8


