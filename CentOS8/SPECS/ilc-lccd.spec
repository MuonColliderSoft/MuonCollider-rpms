%global _pver 1.5.1
%global _tagver v01-05-01

%global _maindir %{_builddir}/%{name}-%{version}
%global cmake_lccd_dir %{_libdir}/cmake/LCCD

Summary: Linear Collider Conditions Data framework
Name: ilc-lccd
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/LCCD
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: doxygen
BuildRequires: ilc-utils-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-cond-db-mysql-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Linear Collider Conditions Data framework

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/LCCD %{_maindir}
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
mkdir -p %{buildroot}%{cmake_lccd_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{cmake_lccd_dir}

sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_lccd_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

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
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.5.1-1
- New version of LCCD
* Fri Jun 05 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.5.0-1
- Repackaging for CentOS 8


