%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 32.0.0
%global _tagver 32.0.0

%global _sbuilddir %{_builddir}/%{name}-%{version}/acts-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_acts_dir %{_libdir}/cmake/Acts
%global _boostp boost

Summary: Toolkit for charged particle track reconstruction
Name: acts-toolkit
Version: %{_pver}
Release: 1%{?dist}
License: MPL v.2
Vendor: INFN
URL: https://github.com/acts-project/acts
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: eigen3-devel
BuildRequires: json-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/acts-project/acts/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Toolkit for charged particle track reconstruction.

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
      -DACTS_USE_SYSTEM_BOOST=ON \
      -DACTS_USE_SYSTEM_EIGEN3=ON \
      -DACTS_USE_SYSTEM_NLOHMANN_JSON=ON \
      -DACTS_BUILD_PLUGIN_DD4HEP=ON \
      -DACTS_BUILD_PLUGIN_JSON=ON \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_acts_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{_bindir}/this_acts.sh

sed -i -e 's|Boost 1.75.0 CONFIG|Boost 1.75.0|g' %{buildroot}%{cmake_acts_dir}/ActsConfig.cmake

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so

%package devel
Summary: Toolkit for charged particle track reconstruction (development files)
Requires: %{name}
Requires: %{_boostp}-devel
Requires: eigen3-devel
Requires: json-devel

%description devel
Toolkit for charged particle track reconstruction.

%files devel
%defattr(-,root,root)
%dir %{cmake_acts_dir}
%{cmake_acts_dir}/*.cmake
%dir %{cmake_acts_dir}/Modules
%{cmake_acts_dir}/Modules/*.cmake
%dir %{_includedir}/Acts
%{_includedir}/Acts/*.hpp
%dir %{_includedir}/Acts/AmbiguityResolution
%{_includedir}/Acts/AmbiguityResolution/*.hpp
%{_includedir}/Acts/AmbiguityResolution/*.ipp
%dir %{_includedir}/Acts/Clusterization
%{_includedir}/Acts/Clusterization/*.hpp
%{_includedir}/Acts/Clusterization/*.ipp
%dir %{_includedir}/Acts/Definitions
%{_includedir}/Acts/Definitions/*.hpp
%dir %{_includedir}/Acts/Detector
%{_includedir}/Acts/Detector/*.hpp
%dir %{_includedir}/Acts/Detector/detail
%{_includedir}/Acts/Detector/detail/*.hpp
%dir %{_includedir}/Acts/Detector/interface
%{_includedir}/Acts/Detector/interface/*.hpp
%dir %{_includedir}/Acts/Digitization
%{_includedir}/Acts/Digitization/*.hpp
%dir %{_includedir}/Acts/EventData
%{_includedir}/Acts/EventData/*.hpp
%{_includedir}/Acts/EventData/*.ipp
%dir %{_includedir}/Acts/EventData/detail
%{_includedir}/Acts/EventData/detail/*.hpp
%dir %{_includedir}/Acts/Geometry
%{_includedir}/Acts/Geometry/*.hpp
%dir %{_includedir}/Acts/Geometry/detail
%{_includedir}/Acts/Geometry/detail/*.ipp
%dir %{_includedir}/Acts/MagneticField
%{_includedir}/Acts/MagneticField/*.hpp
%dir %{_includedir}/Acts/Material
%{_includedir}/Acts/Material/*.hpp
%dir %{_includedir}/Acts/Material/detail
%{_includedir}/Acts/Material/detail/*.hpp
%dir %{_includedir}/Acts/Navigation
%{_includedir}/Acts/Navigation/*.hpp
%dir %{_includedir}/Acts/Propagator
%{_includedir}/Acts/Propagator/*.hpp
%{_includedir}/Acts/Propagator/*.ipp
%dir %{_includedir}/Acts/Propagator/detail
%{_includedir}/Acts/Propagator/detail/*.hpp
%dir %{_includedir}/Acts/Seeding
%{_includedir}/Acts/Seeding/*.hpp
%{_includedir}/Acts/Seeding/*.ipp
%dir %{_includedir}/Acts/Seeding/detail
%{_includedir}/Acts/Seeding/detail/*.hpp
%{_includedir}/Acts/Seeding/detail/*.ipp
%dir %{_includedir}/Acts/SpacePointFormation
%{_includedir}/Acts/SpacePointFormation/*.hpp
%dir %{_includedir}/Acts/SpacePointFormation/detail
%{_includedir}/Acts/SpacePointFormation/detail/*.ipp
%dir %{_includedir}/Acts/Surfaces
%{_includedir}/Acts/Surfaces/*.hpp
%{_includedir}/Acts/Surfaces/*.ipp
%dir %{_includedir}/Acts/Surfaces/detail
%{_includedir}/Acts/Surfaces/detail/*.hpp
%dir %{_includedir}/Acts/TrackFinding
%{_includedir}/Acts/TrackFinding/*.hpp
%dir %{_includedir}/Acts/TrackFinding/detail
%{_includedir}/Acts/TrackFinding/detail/*.hpp
%dir %{_includedir}/Acts/TrackFitting
%{_includedir}/Acts/TrackFitting/*.hpp
%dir %{_includedir}/Acts/TrackFitting/detail
%{_includedir}/Acts/TrackFitting/detail/*.hpp
%dir %{_includedir}/Acts/Utilities
%{_includedir}/Acts/Utilities/*.hpp
%{_includedir}/Acts/Utilities/*.ipp
%dir %{_includedir}/Acts/Utilities/detail
%{_includedir}/Acts/Utilities/detail/*.hpp
%dir %{_includedir}/Acts/Utilities/detail/MPL
%{_includedir}/Acts/Utilities/detail/MPL/*.hpp
%dir %{_includedir}/Acts/Vertexing
%{_includedir}/Acts/Vertexing/*.hpp
%{_includedir}/Acts/Vertexing/*.ipp
%dir %{_includedir}/Acts/Visualization
%{_includedir}/Acts/Visualization/*.hpp
%dir %{_includedir}/Acts/Visualization/detail
%{_includedir}/Acts/Visualization/detail/*.ipp
%dir %{_includedir}/Acts/Plugins
%dir %{_includedir}/Acts/Plugins/DD4hep
%{_includedir}/Acts/Plugins/DD4hep/*.hpp
%dir %{_includedir}/Acts/Plugins/Identification
%{_includedir}/Acts/Plugins/Identification/*.hpp
%dir %{_includedir}/Acts/Plugins/Json
%{_includedir}/Acts/Plugins/Json/*.hpp
%dir %{_includedir}/Acts/Plugins/TGeo
%{_includedir}/Acts/Plugins/TGeo/*.hpp
%{_bindir}/this_acts.sh


%changelog
* Mon Jan 29 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 32.0.0-1
- New major version for ACTS
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 13.0.0-1
- Repackaging for CentOS 8


