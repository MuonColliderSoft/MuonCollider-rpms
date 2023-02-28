%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.17.0
%global _tagver 00-17-MC

%global _sbuilddir %{_builddir}/%{name}-%{version}/lcgeo-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

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
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/lcgeo/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Implementation of Linear Collider detector models in DD4hep.

%prep
%setup -c
sed -i -e 's|VERSION 3.12|VERSION 3.11|g' %{_sbuilddir}/CMakeLists.txt
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DBUILD_TESTING=OFF \
      -DBOOST_INCLUDEDIR=%{_includedir}/boost \
      -DBOOST_LIBRARYDIR=%{_libdir}/boost  \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%{_bindir}/thislcgeo.sh
%{_libdir}/*.so
%{_libdir}/*.components

%changelog
* Tue Feb 28 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.17.0-1
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


