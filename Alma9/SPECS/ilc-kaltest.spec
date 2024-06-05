%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 2.5.2
%global _tagver 02-05-02

%global _sbuilddir %{_builddir}/%{name}-%{version}/KalTest-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_kaltest_dir %{_libdir}/cmake/KalTest

Summary: Classes and utilities for Kalman filter algorithms
Name: ilc-kaltest
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/KalTest
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: patch
BuildRequires: ilc-utils-devel
BuildRequires: ilc-kaltest-headers
BuildRequires: root-genvector
Requires: ilc-kaltest-headers
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/KalTest/archive/refs/tags/v%{_tagver}.tar.gz
Patch0: ilc-kaltest-cmake-headers.patch
AutoReqProv: yes

%description
Classes and utilities for Kalman filter algorithms.

%prep
%setup -c

patch %{_sbuilddir}/src/CMakeLists.txt %{PATCH0}

rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_kaltest_dir}
mv %{buildroot}%{_libdir}/cmake/*.cmake \
   %{buildroot}/usr/*.cmake \
   %{buildroot}%{cmake_kaltest_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|lib/cmake|lib64/cmake/KalTest|g' \
    %{buildroot}%{cmake_kaltest_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*
rm -rf %{buildroot}/usr/include

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so*
%{_libdir}/*.pcm

%package devel
Summary: Classes and utilities for Kalman filter algorithms (development files)
Requires: %{name}
Requires: ilc-utils-devel
Requires: root-genvector

%description devel
Classes and utilities for Kalman filter algorithms.

%files devel
%defattr(-,root,root)
%dir %{cmake_kaltest_dir}
%{cmake_kaltest_dir}/*.cmake

%changelog
* Tue May 28 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.5.2-1
- New version of KalTest
* Thu Jun 18 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.5.0-1
- Repackaging for CentOS 8


