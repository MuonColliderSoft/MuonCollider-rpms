%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.19.1
%global _tagver 01-19-01

%global _sbuilddir %{_builddir}/%{name}-%{version}/Marlin-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global _pypkg python

%global cmake_marlin_dir %{_libdir}/cmake/Marlin

Summary: Modular Analysis and Reconstruction for the LINear Collider
Name: ilc-marlin
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/Marlin
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-gear-devel
BuildRequires: clhep-devel
BuildRequires: ilc-root-aida-devel
Requires: %{_pypkg}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/Marlin/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Modular Analysis and Reconstruction for the LINear Collider.

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
      -DMARLIN_LCCD=OFF \
      -DMARLIN_GUI=OFF \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_marlin_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{cmake_marlin_dir}

sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_marlin_dir}/*.cmake
sed -i -e 's|bin/env python|usr/bin/python3|g' %{buildroot}%{_bindir}/*.py
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/Marlin

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*

%package devel
Summary: Modular Analysis and Reconstruction for the LINear Collider (development files)
Requires: %{name}
Requires: ilc-utils-devel
Requires: ilc-lcio-devel
Requires: ilc-gear-devel
Requires: clhep-devel
Requires: ilc-root-aida-devel

%description devel
Modular Analysis and Reconstruction for the LINear Collider.

%files devel
%defattr(-,root,root)
%dir %{cmake_marlin_dir}
%{cmake_marlin_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/marlin
%{_includedir}/marlin/*.h

%changelog
* Wed Feb 07 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.19.1-1
- New version of Marlin
* Mon Jan 23 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.19.0-1
- New version of Marlin
* Fri Oct 02 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.17.1-1
- New version of Marlin
* Thu Jun 11 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.17.0-1
- Repackaging for CentOS 8


