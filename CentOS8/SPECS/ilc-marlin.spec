%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global _pypkg python36

%global cmake_marlin_dir %{_libdir}/cmake/Marlin

Summary: Modular Analysis and Reconstruction for the LINear Collider
Name: ilc-marlin
Version: 1.17.1
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/Marlin
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-gear-devel
BuildRequires: clhep-devel
BuildRequires: ilc-lccd-devel
BuildRequires: root-aida-devel
Requires: %{_pypkg}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
Modular Analysis and Reconstruction for the LINear Collider.

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
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
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
Requires: ilc-lccd-devel
Requires: root-aida-devel

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
* Fri Oct 02 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.17.1-1
- New version of Marlin
* Thu Jun 11 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.17.0-1
- Repackaging for CentOS 8


