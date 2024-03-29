%global _pver 0.9.7
%global _tagver CondDBMySQL_ILC-0-9-7

%global _maindir %{_builddir}/%{name}-%{version}
%global cmake_cdbm_dir %{_libdir}/cmake/CondDBMySQL

Summary: Interface to MySQL Conditions Database
Name: ilc-cond-db-mysql
Version: %{_pver}
Release: 1%{?dist}
License: GPLv2 License
Vendor: CERN
URL: https://github.com/iLCSoft/CondDBMySQL
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: mysql-devel
BuildRequires: ilc-utils-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Interface to MySQL Conditions Database.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/CondDBMySQL %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_maindir}/build
cd %{_maindir}/build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DINCLUDE_INSTALL_DIR=%{buildroot}%{_includedir}/CondDBMySQL \
      -DLIB_INSTALL_DIR=%{buildroot}%{_libdir} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install

mkdir -p %{buildroot}%{cmake_cdbm_dir}
mv %{buildroot}/usr/lib/cmake/* %{buildroot}/usr/*.cmake %{buildroot}%{cmake_cdbm_dir}
rm -rf %{buildroot}/usr/lib

sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|PATH_SUFFIXES|PATH_SUFFIXES include/CondDBMySQL|g' \
       -e 's|lib/cmake|lib64/cmake/CondDBMySQL|g' \
       %{buildroot}%{cmake_cdbm_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.0.9.6

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Interface to MySQL Conditions Database (development files)
Requires: %{name}
Requires: mysql-devel
Requires: ilc-utils-devel

%description devel
Interface to MySQL Conditions Database.

%files devel
%defattr(-,root,root)
%{cmake_cdbm_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/CondDBMySQL
%{_includedir}/CondDBMySQL/*.h
%dir %{_includedir}/CondDBMySQL/ConditionsDB
%{_includedir}/CondDBMySQL/ConditionsDB/*.h

%changelog
* Fri Feb 28 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.9.7-1
- Repackaging for CentOS 8

