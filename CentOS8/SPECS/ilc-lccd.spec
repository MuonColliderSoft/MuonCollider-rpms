%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_lccd_dir %{_libdir}/cmake/LCCD

Summary: Linear Collider Conditions Data framework
Name: ilc-lccd
Version: 1.5.0
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/LCCD
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: doxygen
BuildRequires: ilc-utils-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-cond-db-mysql-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz

%description
Linear Collider Conditions Data framework

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
mkdir -p %{buildroot}%{cmake_lccd_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{cmake_lccd_dir}

sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_lccd_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.1.5.0

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Linear Collider Conditions Data framework (development files)
Requires: %{name}
Requires: ilc-utils-devel
Requires: ilc-lcio-devel
Requires: ilc-cond-db-mysql-devel

%description devel
Linear Collider Conditions Data framework

%files devel
%defattr(-,root,root)
%{cmake_lccd_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/lccd
%{_includedir}/lccd.h
%{_includedir}/lccd_exceptions.h
%{_includedir}/lccd/*.h
%{_includedir}/lccd/*.hh

%changelog
* Fri Jun 05 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.5.0-1
- Repackaging for CentOS 8


