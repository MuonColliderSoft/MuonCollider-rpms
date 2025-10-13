%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.1.0
%global _tagver eaffaff7ddb57c673769371ea7fa7b8ef9eeee1e

%global _sbuilddir %{_builddir}/%{name}-%{version}/k4ActsTracking-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_k4acts_dir %{_libdir}/cmake/k4ActsTracking

Summary: Gaudi algorithms for running track reconstructions using the ACTS library
Name: key4hep-acts-tracking
Version: %{_pver}
Release: 1%{?dist}
License: Apache License 2.0
URL: https://github.com/MuonColliderSoft/k4ActsTracking
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: key4hep-fw-core-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: acts-toolkit-devel
BuildRequires: root
BuildRequires: edm4hep-devel
BuildRequires: lua-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/k4ActsTracking/archive/%{_tagver}.zip
AutoReqProv: yes

%description
Gaudi algorithms for running track reconstructions using the ACTS library.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=20 \
      -DBUILD_TESTING=OFF \
      -DCPPGSL_INCLUDE_DIR=/opt/GSL/include \
      -DCMAKE_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
chrpath --delete %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{cmake_k4acts_dir}
mv %{buildroot}%{_prefix}/lib/cmake/k4ActsTracking/* %{buildroot}%{cmake_k4acts_dir}
rm -rf %{buildroot}%{_prefix}/lib/

mkdir -p %{buildroot}%{python3_sitelib}
mv %{buildroot}%{_prefix}/python/k4ActsTracking %{buildroot}%{python3_sitelib}
rm -rf %{buildroot}%{_prefix}/python

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.components
%{_libdir}/*.confdb
%{_libdir}/*.confdb2
%dir %{_datadir}/ACTSTracking
%dir %{_datadir}/ACTSTracking/data
%{_datadir}/ACTSTracking/data/*

%package devel
Summary: Gaudi algorithms for running track reconstructions using the ACTS library (development files).
Requires: %{name}
Requires: Requires: key4hep-fw-core-devel
Requires: aida-dd4hep-devel
Requires: acts-toolkit-devel
Requires: edm4hep-devel
Requires: root
Requires: lua-devel

%description devel
Gaudi algorithms for running track reconstructions using the ACTS library.

%files devel
%defattr(-,root,root)
%dir %{cmake_k4acts_dir}
%{cmake_k4acts_dir}/*
%dir %{_includedir}/k4ActsTracking
%{_includedir}/k4ActsTracking/*.h
%{_includedir}/k4ActsTracking/*.hxx

%package -n python3-k4actstracking
Summary: Gaudi algorithms for running track reconstructions using the ACTS library (python modules).
BuildArch: noarch
Requires: %{name}
Requires: python3-k4fwcore

%description -n python3-k4actstracking
Gaudi algorithms for running track reconstructions using the ACTS library.

%files -n python3-k4actstracking
%defattr(-,root,root)
%dir %{python3_sitelib}/k4ActsTracking
%dir %{python3_sitelib}/k4ActsTracking/__pycache__
%{python3_sitelib}/k4ActsTracking/*.py
%{python3_sitelib}/k4ActsTracking/__pycache__/*


%changelog
* Mon Oct 13 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.1.0-1
- Porting to AlmaLinux

