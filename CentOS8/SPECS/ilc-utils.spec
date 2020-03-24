%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_ilcutil_dir %{_libdir}/cmake/ilcutil-%{version}

Summary: Utilities for the iLCSoft software framework
Name: ilc-utils
Version: 1.6
Release: 1%{?dist}
License: GPLv3 License
Vendor: CERN
URL: https://github.com/iLCSoft/iLCUtil.git
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: chrpath
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz

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
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=14 \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}

%install
cd %{_builddir}/%{name}-%{version}/build
make %{?_smp_mflags}
make install
mkdir -p %{buildroot}%{_datadir}
mv %{buildroot}/usr/doc %{buildroot}%{_datadir}
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_ilcutil_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}/usr/cmakemodules %{buildroot}%{cmake_ilcutil_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_ilcutil_dir}/*.cmake
sed -i -e 's|/usr/cmakemodules|%{cmake_ilcutil_dir}/cmakemodules|g' %{buildroot}%{cmake_ilcutil_dir}/*.cmake
sed -i -e 's|/usr|%{cmake_ilcutil_dir}|g' %{buildroot}%{cmake_ilcutil_dir}/ILCUTILConfig.cmake
sed -i -e 's|/usr|%{cmake_ilcutil_dir}|g' %{buildroot}%{cmake_ilcutil_dir}/ILCTESTConfig.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.0.4.0

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Utilities for the iLCSoft software framework (development files)
Requires: %{name}

%description devel
ILCUTIL is a utility package for the iLCSoft software framework.
It is intended to be a "meta-package" which packages together a set of independent
utility packages living in separate sub-directories.

%files devel
%defattr(-,root,root)
%dir %{cmake_ilcutil_dir}
%dir %{cmake_ilcutil_dir}/cmakemodules
%{cmake_ilcutil_dir}/*.cmake
%{cmake_ilcutil_dir}/cmakemodules/*.cmake
%{cmake_ilcutil_dir}/cmakemodules/README
%{cmake_ilcutil_dir}/cmakemodules/cmake_uninstall.cmake.in
%{cmake_ilcutil_dir}/cmakemodules/release.notes
%{_libdir}/*.so

%dir %{_includedir}/ilctest
%{_includedir}/ilctest/*.h
%dir %{_includedir}/streamlog
%{_includedir}/streamlog/*.h

%package doc
Summary: Utilities for the iLCSoft software framework (documentation)

%description doc
ILCUTIL is a utility package for the iLCSoft software framework.
It is intended to be a "meta-package" which packages together a set of independent
utility packages living in separate sub-directories.

%files doc
%defattr(-,root,root)
%dir %{_datadir}/doc/streamlog
%dir %{_datadir}/doc/streamlog/html
%{_datadir}/doc/streamlog/html/*
%dir %{_datadir}/doc/ilcutil
%{_datadir}/doc/ilcutil/*

%changelog
* Fri Feb 28 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.6-1
- Repackaging for CentOS 8


