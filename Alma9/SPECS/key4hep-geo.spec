%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.22.99
%global _tagver MuSIC_0_23_pre01

%global _sbuilddir %{_builddir}/%{name}-%{version}/k4geo-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_k4geo_dir %{_libdir}/cmake/k4geo
%global _pgeoname muonc-detector-geometry

Summary: Implementation of Lepton Collider detector models in DD4hep.
Name: key4hep-geo
Version: %{_pver}
Release: 1%{?dist}
License: Apache License 2.0
URL: https://github.com/pandreetto/k4geo
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: aida-dd4hep-devel
BuildRequires: ilc-lcio-devel
BuildRequires: python3-podio-utils
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/pandreetto/k4geo/archive/refs/tags/%{_tagver}.tar.gz
Patch0: key4hep-geom-CMakeLists.patch
AutoReqProv: yes

%description
Implementation of Lepton Collider detector models in DD4hep.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}
patch %{_sbuilddir}/CMakeLists.txt %{PATCH0}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=20 \
      -DBUILD_TESTING=OFF \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

rm -rf %{buildroot}%{_prefix}/lib
chrpath --delete %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{_datadir}/%{_pgeoname}
cp -r %{_sbuilddir}/MuColl/MuColl/compact/MuColl_v0 %{buildroot}%{_datadir}/%{_pgeoname}
cp -r %{_sbuilddir}/MuColl/MuColl/compact/MuColl_v1 %{buildroot}%{_datadir}/%{_pgeoname}
cp -r %{_sbuilddir}/MuColl/MuColl/compact/MuColl_v1.0.1 %{buildroot}%{_datadir}/%{_pgeoname}
cp -r %{_sbuilddir}/MuColl/MuColl/compact/MuColl_v1.0.2 %{buildroot}%{_datadir}/%{_pgeoname}
cp -r %{_sbuilddir}/MuColl/MuColl/compact/MuColl_v1.1 %{buildroot}%{_datadir}/%{_pgeoname}
cp -r %{_sbuilddir}/MuColl/MuColl/compact/MuColl_v1.1.1 %{buildroot}%{_datadir}/%{_pgeoname}
cp -r %{_sbuilddir}/MuColl/MuColl/compact/MuColl_v1.1.2 %{buildroot}%{_datadir}/%{_pgeoname}
cp -r %{_sbuilddir}/MuColl/MuColl/compact/MuColl_v1.1.3 %{buildroot}%{_datadir}/%{_pgeoname}
cp -r %{_sbuilddir}/MuColl/MuColl/compact/MuSIC_v1 %{buildroot}%{_datadir}/%{_pgeoname}
cp -r %{_sbuilddir}/MuColl/MuColl/compact/MuSIC_v2 %{buildroot}%{_datadir}/%{_pgeoname}
find %{buildroot}%{_datadir}/%{_pgeoname} -name '*.md' -exec rm '{}' \;

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MUCOLL_GEO=%{_datadir}/%{_pgeoname}/MuSIC_v2/MuSIC_v2.xml\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/%{_pgeoname}.sh
printf "setenv MUCOLL_GEO %{_datadir}/%{_pgeoname}/MuSIC_v2/MuSIC_v2.xml\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/%{_pgeoname}.csh


%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.components

%package devel
Summary: Implementation of Lepton Collider detector models in DD4hep (development files).
Requires: %{name}
Requires: aida-dd4hep-devel
Requires: ilc-lcio-devel

%description devel
Implementation of Lepton Collider detector models in DD4hep (development files).

%files devel
%defattr(-,root,root)
%dir %{cmake_k4geo_dir}
%{cmake_k4geo_dir}/*.cmake
%dir %{_includedir}/detectorCommon
%{_includedir}/detectorCommon/*.h
%dir %{_includedir}/detectorSegmentations
%{_includedir}/detectorSegmentations/*.h

%package -n %{_pgeoname}
Summary: The Muon Collider detector geometry
BuildArch: noarch
Requires: %{name}

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
%dir %{_datadir}/%{_pgeoname}/MuSIC_v1
%{_datadir}/%{_pgeoname}/MuSIC_v1/*.xml
%dir %{_datadir}/%{_pgeoname}/MuSIC_v2
%{_datadir}/%{_pgeoname}/MuSIC_v2/*.xml
%{_sysconfdir}/profile.d/*

%changelog
* Tue Aug 26 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.22.99-1
- Packages for AlmaLinux 10

