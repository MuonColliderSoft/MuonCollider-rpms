# workaround: QA_SKIP_BUILD_ROOT=1 rpmbuild -ba pandora-pfa.spec
%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 4.8.1
%global _tagver 04-08-01

%global _sbuilddir %{_builddir}/%{name}-%{version}/PandoraPFA-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_panutil_dir %{_libdir}/cmake/PandoraUtil
%global cmake_panmon_dir %{_libdir}/cmake/PandoraMonitoring
%global cmake_pansdk_dir %{_libdir}/cmake/PandoraSDK
%global cmake_panlcc_dir %{_libdir}/cmake/LCContent

Summary: Suite for particle flow analysis
Name: pandora-pfa
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/PandoraPFA/PandoraPFA
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/PandoraPFA/PandoraPFA/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Suite for particle flow analysis.

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
      -DPANDORA_MONITORING=ON \
      -DLC_PANDORA_CONTENT=ON \
      -DEXAMPLE_PANDORA_CONTENT=OFF \
      -DCMAKE_CXX_FLAGS="-std=c++17" \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
rm -rf %{buildroot}/usr/doc

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}

mkdir -p %{buildroot}%{cmake_panutil_dir}
cp %{_sbuilddir}/cmakemodules/MacroCheckPackageLibs.cmake \
   %{_sbuilddir}/cmakemodules/MacroCheckPackageVersion.cmake \
   %{buildroot}%{cmake_panutil_dir}

mkdir -p %{buildroot}%{cmake_pansdk_dir}
mv %{buildroot}/usr/PandoraSDKConfig* \
   %{buildroot}%{_libdir}/cmake/PandoraSDKLibDeps.cmake \
   %{buildroot}%{cmake_pansdk_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|%{_sbuilddir}/cmakemodules|%{cmake_panutil_dir}|g' \
       -e 's|lib/cmake|lib64/cmake/PandoraSDK|g'\
    %{buildroot}%{cmake_pansdk_dir}/*.cmake

mkdir -p %{buildroot}%{cmake_panmon_dir}
mv %{buildroot}/usr/PandoraMonitoringConfig* \
   %{buildroot}%{_libdir}/cmake/PandoraMonitoringLibDeps.cmake \
   %{buildroot}%{cmake_panmon_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|%{_sbuilddir}/cmakemodules|%{cmake_panutil_dir}|g' \
       -e 's|lib/cmake|lib64/cmake/PandoraMonitoring|g'\
       -e 's|usr/lib/lib|usr/lib64/lib|g' \
    %{buildroot}%{cmake_panmon_dir}/*.cmake

mkdir -p %{buildroot}%{cmake_panlcc_dir}
mv %{buildroot}/usr/LCContentConfig* \
   %{buildroot}%{_libdir}/cmake/LCContentLibDeps.cmake \
   %{buildroot}%{cmake_panlcc_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|%{_sbuilddir}/cmakemodules|%{cmake_panutil_dir}|g' \
       -e 's|lib/cmake|lib64/cmake/LCContent|g'\
       -e 's|usr/lib/lib|usr/lib64/lib|g' \
    %{buildroot}%{cmake_panlcc_dir}/*.cmake

chrpath --replace %{_libdir} %{buildroot}%{_libdir}/libLCContent.so.*
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/libPandoraMonitoring.so.*
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/libPandoraSDK.so.*

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Suite for particle flow analysis (development files)
Requires: %{name}
Requires: root

%description devel
Suite for particle flow analysis.

%files devel
%defattr(-,root,root)
%dir %{cmake_panutil_dir}
%dir %{cmake_panmon_dir}
%dir %{cmake_pansdk_dir}
%dir %{cmake_panlcc_dir}
%{cmake_panutil_dir}/*.cmake
%{cmake_panmon_dir}/*.cmake
%{cmake_pansdk_dir}/*.cmake
%{cmake_panlcc_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/Api
%dir %{_includedir}/Geometry
%dir %{_includedir}/Helpers
%dir %{_includedir}/Managers
%dir %{_includedir}/Objects
%dir %{_includedir}/Pandora
%dir %{_includedir}/Persistency
%dir %{_includedir}/Plugins
%dir %{_includedir}/Templates
%dir %{_includedir}/Xml
%dir %{_includedir}/LCCheating
%dir %{_includedir}/LCClustering
%dir %{_includedir}/LCFragmentRemoval
%dir %{_includedir}/LCHelpers
%dir %{_includedir}/LCMonitoring
%dir %{_includedir}/LCObjects
%dir %{_includedir}/LCParticleId
%dir %{_includedir}/LCPersistency
%dir %{_includedir}/LCPfoConstruction
%dir %{_includedir}/LCPlugins
%dir %{_includedir}/LCReclustering
%dir %{_includedir}/LCTopologicalAssociation
%dir %{_includedir}/LCTrackClusterAssociation
%dir %{_includedir}/LCUtility
%{_includedir}/Api/*.h
%{_includedir}/Geometry/*.h
%{_includedir}/Helpers/*.h
%{_includedir}/Managers/*.h
%{_includedir}/Objects/*.h
%{_includedir}/Pandora/*.h
%{_includedir}/Persistency/*.h
%{_includedir}/Plugins/*.h
%{_includedir}/Templates/*.h
%{_includedir}/Xml/*.h
%{_includedir}/LCCheating/*.h
%{_includedir}/LCClustering/*.h
%{_includedir}/LCFragmentRemoval/*.h
%{_includedir}/LCHelpers/*.h
%{_includedir}/LCMonitoring/*.h
%{_includedir}/LCObjects/*.h
%{_includedir}/LCParticleId/*.h
%{_includedir}/LCPersistency/*.h
%{_includedir}/LCPfoConstruction/*.h
%{_includedir}/LCPlugins/*.h
%{_includedir}/LCReclustering/*.h
%{_includedir}/LCTopologicalAssociation/*.h
%{_includedir}/LCTrackClusterAssociation/*.h
%{_includedir}/LCUtility/*.h
%{_includedir}/LCContent.h
%{_includedir}/PandoraMonitoring.h
%{_includedir}/PandoraMonitoringApi.h
%{_includedir}/TTreeWrapper.h

%changelog
* Wed May 22 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 4.8.1-1
- New version of PandoraPFA
* Mon Jan 23 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 4.2.0-1
- New version of PandoraPFA
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 3.25.3-1
- New version of Pandora PFA
* Thu Jul 09 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 3.14.0-1
- Repackaging for CentOS 8


