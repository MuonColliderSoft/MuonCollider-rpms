%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_ddkalt_dir %{_libdir}/cmake/DDKalTest
%global _boostp boost169

Summary: Interface between KalTest fitter and DD4hep based geometry
Name: ilc-ddkaltest
Version: 1.6.0
Release: 1%{?dist}
License: GPLv3 License
Vendor: INFN
URL: https://github.com/iLCSoft/DDKalTest
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-kaltest-devel
BuildRequires: aida-tracking-toolkit-devel
BuildRequires: gsl-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
Re-implentation of some of the code in KalDet, now using the DDRec:Surface
provided by a DD4hep based tracking geometry as input for the measurement
surfaces needed in KalTest. Intersection calculation is currently done in
aidaTT. Material effects use averaged material from the DDRec:Surface.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
sed -i -e 's|ILD/include|include/DDKalTest|g' %{_builddir}/%{name}-%{version}/CMakeLists.txt
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=14 \
             -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
             -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
             -Dstreamlog_DIR=%{_libdir}/cmake/ilcutil-1.6/ \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_ddkalt_dir}
mv %{buildroot}%{_prefix}/*.cmake %{buildroot}%{cmake_ddkalt_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_ddkalt_dir}/*.cmake

chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/printSurfaces

%clean
rm -rf %{buildroot}

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

