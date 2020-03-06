Summary: Utilities for the iLCSoft software framework
Name: ilc-utils
Version: 1.6
Release: 1%{?dist}
License: GPLv3 License
Vendor: CERN
URL: https://github.com/iLCSoft/iLCUtil.git
Group: Development/Libraries
BuildArch: %{_arch}
%if %{?rhel}%{!?rhel:0} >= 8
BuildRequires: cmake
%else
BuildRequires: cmake3
%endif
BuildRequires: chrpath
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz

%global cmake_ilcutil_dir ilcutil-%{version}

%description
ILCUTIL is a utility package for the iLCSoft software framework.
It is intended to be a "meta-package" which packages together a set of independent
utility packages living in separate sub-directories.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/usr \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCMAKE_CXX_STANDARD=14 \
       -Wno-dev \
       %{_builddir}/%{name}-%{version}

%install
cd %{_builddir}/%{name}-%{version}/build
make %{?_smp_mflags}
make install
mkdir -p %{buildroot}/usr/share
mv %{buildroot}/usr/doc %{buildroot}/usr/share
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/cmake/%{cmake_ilcutil_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}/usr/cmakemodules %{buildroot}%{_libdir}/cmake/%{cmake_ilcutil_dir}
sed -i -e 's|%{buildroot}/usr|/usr|g' %{buildroot}%{_libdir}/cmake/%{cmake_ilcutil_dir}/*.cmake
sed -i -e 's|/usr/cmakemodules|%{_libdir}/cmake/%{cmake_ilcutil_dir}/cmakemodules|g' %{buildroot}%{_libdir}/cmake/%{cmake_ilcutil_dir}/*.cmake
sed -i -e 's|/usr|%{_libdir}/cmake/%{cmake_ilcutil_dir}|g' %{buildroot}%{_libdir}/cmake/%{cmake_ilcutil_dir}/ILCUTILConfig.cmake
sed -i -e 's|/usr|%{_libdir}/cmake/%{cmake_ilcutil_dir}|g' %{buildroot}%{_libdir}/cmake/%{cmake_ilcutil_dir}/ILCTESTConfig.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.0.4.0

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Utilities for the iLCSoft software framework (development files)

%description devel
ILCUTIL is a utility package for the iLCSoft software framework.
It is intended to be a "meta-package" which packages together a set of independent
utility packages living in separate sub-directories.

%files devel
%defattr(-,root,root)
%dir %{_libdir}/cmake/%{cmake_ilcutil_dir}
%dir %{_libdir}/cmake/%{cmake_ilcutil_dir}/cmakemodules
%{_libdir}/cmake/%{cmake_ilcutil_dir}/*.cmake
%{_libdir}/cmake/%{cmake_ilcutil_dir}/cmakemodules/*.cmake
%{_libdir}/cmake/%{cmake_ilcutil_dir}/cmakemodules/README
%{_libdir}/cmake/%{cmake_ilcutil_dir}/cmakemodules/cmake_uninstall.cmake.in
%{_libdir}/cmake/%{cmake_ilcutil_dir}/cmakemodules/release.notes
%{_libdir}/*.so

%dir /usr/include/ilctest
/usr/include/ilctest/*.h
%dir /usr/include/streamlog
/usr/include/streamlog/*.h

%package doc
Summary: Utilities for the iLCSoft software framework (documentation)

%description doc
ILCUTIL is a utility package for the iLCSoft software framework.
It is intended to be a "meta-package" which packages together a set of independent
utility packages living in separate sub-directories.

%files doc
%defattr(-,root,root)
%dir /usr/share/doc/streamlog
%dir /usr/share/doc/streamlog/html
/usr/share/doc/streamlog/html/*
%dir /usr/share/doc/ilcutil
/usr/share/doc/ilcutil/*

%changelog
* Fri Feb 28 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.6-1
- Repackaging for CentOS 8


