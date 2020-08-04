%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_gear_dir %{_libdir}/cmake/gear
%global _pypkg python36

Summary: GEometry Api for Reconstruction
Name: ilc-gear
Version: 1.9.0
Release: 1%{?dist}
License: GPL v.3
Vendor: DESY/SLAC
URL: https://github.com/iLCSoft/GEAR
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: ilc-utils-devel
BuildRequires: root
BuildRequires: root-geom
BuildRequires: root-gdml
BuildRequires: clhep-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
GEometry Api for Reconstruction.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=14 \
             -DGEAR_TGEO=ON \
             -DINSTALL_DOC=OFF \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_gear_dir}
mv %{buildroot}%{_prefix}/*.cmake %{buildroot}%{cmake_gear_dir}
sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' %{buildroot}%{cmake_gear_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/*

%clean
rm -rf %{buildroot}

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
* Wed Mar 25 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.13.1-1
- Repackaging for CentOS 8














