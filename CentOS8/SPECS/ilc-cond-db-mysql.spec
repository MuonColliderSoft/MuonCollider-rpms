Summary: Interface to MySQL Conditions Database
Name: ilc-cond-db-mysql
Version: 0.9.7
Release: 1%{?dist}
License: GPLv2 License
Vendor: CERN
URL: https://github.com/iLCSoft/CondDBMySQL.git
Group: Development/Libraries
BuildArch: %{_arch}
%if %{?rhel}%{!?rhel:0} >= 8
BuildRequires: cmake
%else
BuildRequires: cmake3
%endif
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
%cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/usr \
       -DINCLUDE_INSTALL_DIR=%{buildroot}/usr/include/CondDBMySQL \
       -DLIB_INSTALL_DIR=%{buildroot}%{_libdir} \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCMAKE_CXX_STANDARD=14 \
       -Wno-dev \
       %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

mkdir -p %{buildroot}%{_libdir}/cmake/CondDBMySQL
mv %{buildroot}/usr/lib/cmake/* %{buildroot}/usr/*.cmake %{buildroot}%{_libdir}/cmake/CondDBMySQL
rm -rf %{buildroot}/usr/lib

sed -i -e 's|%{buildroot}/usr|/usr|g' %{buildroot}%{_libdir}/cmake/CondDBMySQL/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.0.9.6

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Interface to MySQL Conditions Database (development files)
Requires: mysql-devel
Requires: ilc-utils-devel

%description devel
Interface to MySQL Conditions Database.

%files devel
%defattr(-,root,root)
%{_libdir}/cmake/CondDBMySQL/*.cmake
%{_libdir}/*.so
%dir /usr/include/CondDBMySQL
/usr/include/CondDBMySQL/*.h
%dir /usr/include/CondDBMySQL/ConditionsDB
/usr/include/CondDBMySQL/ConditionsDB/*.h

%changelog
* Fri Feb 28 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.6-1
- Repackaging for CentOS 8

