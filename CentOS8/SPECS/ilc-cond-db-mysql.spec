%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_cdbm_dir %{_libdir}/cmake/CondDBMySQL

Summary: Interface to MySQL Conditions Database
Name: ilc-cond-db-mysql
Version: 0.9.7
Release: 1%{?dist}
License: GPLv2 License
Vendor: CERN
URL: https://github.com/iLCSoft/CondDBMySQL.git
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: mysql-devel
BuildRequires: ilc-utils-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz

%description
Interface to MySQL Conditions Database.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DINCLUDE_INSTALL_DIR=%{buildroot}%{_includedir}/CondDBMySQL \
             -DLIB_INSTALL_DIR=%{buildroot}%{_libdir} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=14 \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
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
* Fri Feb 28 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.6-1
- Repackaging for CentOS 8

