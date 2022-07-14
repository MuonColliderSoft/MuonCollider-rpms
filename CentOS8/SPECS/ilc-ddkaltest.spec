%global _pver 1.7.0
%global _tagver v01-07

%global _maindir %{_builddir}/%{name}-%{version}

%global cmake_ddkalt_dir %{_libdir}/cmake/DDKalTest
%global _boostp boost169

Summary: Interface between KalTest fitter and DD4hep based geometry
Name: ilc-ddkaltest
Version: %{_pver}
Release: 1%{?dist}
License: GPLv3 License
Vendor: INFN
URL: https://github.com/iLCSoft/DDKalTest
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-kaltest-devel
BuildRequires: aida-tracking-toolkit-devel
BuildRequires: gsl-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Re-implentation of some of the code in KalDet, now using the DDRec:Surface
provided by a DD4hep based tracking geometry as input for the measurement
surfaces needed in KalTest. Intersection calculation is currently done in
aidaTT. Material effects use averaged material from the DDRec:Surface.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/DDKalTest %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
sed -i -e 's|ILD/include|include/DDKalTest|g' %{_maindir}/CMakeLists.txt
mkdir %{_maindir}/build
cd %{_maindir}/build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
      -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
      -Dstreamlog_DIR=%{_libdir}/cmake/ilcutil/ \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_ddkalt_dir}
mv %{buildroot}%{_prefix}/*.cmake %{buildroot}%{cmake_ddkalt_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_ddkalt_dir}/*.cmake

chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/printSurfaces

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_bindir}/thisDDKalTest.sh
%{_bindir}/printSurfaces
%{_libdir}/*.so.*

%package devel
Summary: Tracking Toolkit from the AIDA project (development files)
Requires: %{name}
Requires: ilc-utils-devel
Requires: ilc-lcio-devel
Requires: ilc-kaltest-devel
Requires: aida-tracking-toolkit-devel
Requires: gsl-devel

%description devel
Re-implentation of some of the code in KalDet, now using the DDRec:Surface
provided by a DD4hep based tracking geometry as input for the measurement
surfaces needed in KalTest. Intersection calculation is currently done in
aidaTT. Material effects use averaged material from the DDRec:Surface.

%files devel
%defattr(-,root,root)
%dir %{cmake_ddkalt_dir}
%{cmake_ddkalt_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/DDKalTest
%{_includedir}/DDKalTest/*.h

%changelog
* Fri Jul 03 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.6.0-1
- Repackaging for CentOS 8

