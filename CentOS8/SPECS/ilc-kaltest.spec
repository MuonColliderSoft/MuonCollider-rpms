%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_kaltest_dir %{_libdir}/cmake/KalTest

Summary: Classes and utilities for Kalman filter algorithms
Name: ilc-kaltest
Version: 2.5.0
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/KalTest
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: root
BuildRequires: root-graf3d-eve
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
Classes and utilities for Kalman filter algorithms.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=17 \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_kaltest_dir}
mv %{buildroot}%{_libdir}/cmake/*.cmake \
   %{buildroot}/usr/*.cmake \
   %{buildroot}%{cmake_kaltest_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|lib/cmake|lib64/cmake/KalTest|g' \
    %{buildroot}%{cmake_kaltest_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.pcm

%package devel
Summary: Classes and utilities for Kalman filter algorithms (development files)
Requires: %{name}
Requires: ilc-utils-devel
Requires: root
Requires: root-graf3d-eve

%description devel
Classes and utilities for Kalman filter algorithms.

%files devel
%defattr(-,root,root)
%dir %{cmake_kaltest_dir}
%{cmake_kaltest_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/kaltest
%{_includedir}/kaltest/*.h

%changelog
* Thu Jun 18 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.5.0-1
- Repackaging for CentOS 8


