%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.7.2
%global _tagver 01-07-02

%global _sbuilddir %{_builddir}/%{name}-%{version}/iLCUtil-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_ilcutil_dir %{_libdir}/cmake/ilcutil

Summary: Utilities for the iLCSoft software framework
Name: ilc-utils
Version: %{_pver}
Release: 1%{?dist}
License: GPLv3 License
Vendor: CERN
URL: https://github.com/iLCSoft/iLCUtil
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: doxygen
BuildRequires: chrpath
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source0: https://github.com/iLCSoft/iLCUtil/archive/refs/tags/v%{_tagver}.tar.gz

%description
ILCUTIL is a utility package for the iLCSoft software framework.
It is intended to be a "meta-package" which packages together a set of independent
utility packages living in separate sub-directories.

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
      -DINSTALL_DOC=OFF \
      -Wno-dev \
      %{_sbuilddir}

%install
cd %{_cbuilddir}
make %{?_smp_mflags}
make install
rm -rf %{buildroot}/usr/doc

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
rm -f %{SOURCE0}

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

%changelog
* Wed Feb 07 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.7.2-1
- New version
* Fri Jan 19 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.7.1-1
- New version
* Mon Jan 23 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.7.0-1
- New version of iLC utils
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.6.2-1
- New version of iLC utils
* Fri Oct 02 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.6.1-1
- New version of iLC utils
* Fri Feb 28 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.6-1
- Repackaging for CentOS 8


