%global _pver 2.5.1
%global _tagver v02-05-01

%global _maindir %{_builddir}/%{name}-%{version}

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
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: root
BuildRequires: root-graf3d-eve
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Classes and utilities for Kalman filter algorithms.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/KalTest %{_maindir}
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
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
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

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

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
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.5.1-1
- New version of KalTest
* Thu Jun 18 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.5.0-1
- Repackaging for CentOS 8


