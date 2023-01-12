%global _pver 1.14.1
%global _tagver v01-14-01

%global _maindir %{_builddir}/%{name}-%{version}

%global cmake_kaldet_dir %{_libdir}/cmake/KalDet

Summary: Kalman filter algorithms applied to detectors
Name: ilc-kaldet
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/KalDet
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: ilc-kaltest-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-gear-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Kalman filter algorithms applied to detectors.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/KalDet %{_maindir}
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
mkdir -p %{buildroot}%{cmake_kaldet_dir}
mv %{buildroot}%{_libdir}/cmake/*.cmake \
   %{buildroot}/usr/*.cmake \
   %{buildroot}%{cmake_kaldet_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|lib/cmake|lib64/cmake/KalDet|g' \
    %{buildroot}%{cmake_kaldet_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.pcm

%package devel
Summary: Kalman filter algorithms applied to detectors (development files)
Requires: %{name}
Requires: ilc-utils-devel
Requires: ilc-kaltest-devel
Requires: ilc-marlin-devel
Requires: ilc-marlin-util-devel
Requires: ilc-gear-devel
Requires: root

%description devel
Kalman filter algorithms applied to detectors.

%files devel
%defattr(-,root,root)
%dir %{cmake_kaldet_dir}
%{cmake_kaldet_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/kaldet
%{_includedir}/kaldet/*.h

%changelog
* Mon Jul 13 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.14.1-1
- Repackaging for CentOS 8


