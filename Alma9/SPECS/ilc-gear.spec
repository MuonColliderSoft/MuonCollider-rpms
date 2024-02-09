%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.9.2
%global _tagver 01-09-02

%global _sbuilddir %{_builddir}/%{name}-%{version}/GEAR-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_gear_dir %{_libdir}/cmake/gear

Summary: GEometry Api for Reconstruction
Name: ilc-gear
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: DESY/SLAC
URL: https://github.com/iLCSoft/GEAR
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: ilc-utils-devel
BuildRequires: root
BuildRequires: root-geom
BuildRequires: root-gdml
BuildRequires: clhep-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/GEAR/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
GEometry Api for Reconstruction.

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
      -DGEAR_TGEO=ON \
      -DINSTALL_DOC=OFF \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_gear_dir}
mv %{buildroot}%{_prefix}/*.cmake %{buildroot}%{cmake_gear_dir}
sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' %{buildroot}%{cmake_gear_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/*

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*

%package devel
Summary: GEometry Api for Reconstruction (development files)
Requires: %{name}
Requires: ilc-utils-devel
Requires: clhep-devel
Requires: root
Requires: root-geom
Requires: root-geom-builder
Requires: root-geom-painter
Requires: root-gdml

%description devel
GEometry Api for Reconstruction.

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%dir %{_includedir}/gear
%dir %{_includedir}/gear/gearcga
%dir %{_includedir}/gear/gearimpl
%dir %{_includedir}/gear/gearsurf
%dir %{_includedir}/gear/geartgeo
%dir %{_includedir}/gear/gearxml
%{_includedir}/gearimpl
%{_includedir}/gearsurf
%{_includedir}/geartgeo
%{_includedir}/gearxml
%{_includedir}/gear/*.h
%{_includedir}/gear/gearcga/*.h
%{_includedir}/gear/gearimpl/*.h
%{_includedir}/gear/gearsurf/*.h
%{_includedir}/gear/geartgeo/*.h
%{_includedir}/gear/gearxml/*.h
%dir %{cmake_gear_dir}
%{cmake_gear_dir}/*.cmake


%changelog
* Wed Feb 07 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.9.2-1
- New version of GEAR
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.9.1-1
- New version of GEAR
* Wed Mar 25 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.9.0-1
- Repackaging for CentOS 8














