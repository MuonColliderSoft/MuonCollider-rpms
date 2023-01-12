%global _pver 1.9.1
%global _tagver v01-09-01

%global _maindir %{_builddir}/%{name}-%{version}
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
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: ilc-utils-devel
BuildRequires: root
BuildRequires: root-geom
BuildRequires: root-gdml
BuildRequires: clhep-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
GEometry Api for Reconstruction.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/GEAR %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_maindir}/build
cd %{_maindir}/build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DGEAR_TGEO=ON \
      -DINSTALL_DOC=OFF \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_gear_dir}
mv %{buildroot}%{_prefix}/*.cmake %{buildroot}%{cmake_gear_dir}
sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' %{buildroot}%{cmake_gear_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/*

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

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
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.9.1-1
- New version of GEAR
* Wed Mar 25 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.9.0-1
- Repackaging for CentOS 8














