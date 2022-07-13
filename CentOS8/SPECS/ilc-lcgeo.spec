%global _pver 0.16.8
%global _tagver v00-16-08-MC

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost169

Summary: Implementation of Linear Collider detector models in DD4hep.
Name: ilc-lcgeo
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/lcgeo
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: aida-dd4hep-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Implementation of Linear Collider detector models in DD4hep.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/MuonColliderSoft/lcgeo %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
sed -i -e 's|VERSION 3.12|VERSION 3.11|g' %{_maindir}/CMakeLists.txt
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_maindir}/build
cd %{_maindir}/build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DBUILD_TESTING=OFF \
      -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
      -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install

mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_bindir}/thislcgeo.sh
%{_libdir}/*.so
%{_libdir}/*.components

%changelog
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


