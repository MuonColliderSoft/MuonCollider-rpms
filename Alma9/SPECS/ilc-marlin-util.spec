%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.17.2
%global _tagver 01-17-02

%global _sbuilddir %{_builddir}/%{name}-%{version}/MarlinUtil-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global _boostp boost

%global cmake_marlutil_dir %{_libdir}/cmake/MarlinUtil

Summary: Classes and functions used by Marlin processors
Name: ilc-marlin-util
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinUtil
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-ced-devel
BuildRequires: gsl-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: %{_boostp}-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/MarlinUtil/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
This library that containes classes and functions that are used by
more than one processor.

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
      -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
      -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
      -DUSE_EXTERNAL_CATCH2=OFF \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_marlutil_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{cmake_marlutil_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_marlutil_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Classes and functions used by Marlin processors (development files)
Requires: %{name}
Requires: ilc-marlin-devel
Requires: ilc-ced-devel
Requires: gsl-devel
Requires: aida-dd4hep-devel
Requires: %{_boostp}-devel

%description devel
This library that containes classes and functions that are used by
more than one processor.

%files devel
%defattr(-,root,root)
%dir %{cmake_marlutil_dir}
%{cmake_marlutil_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/marlinutil
%dir %{_includedir}/marlinutil/ANN
%dir %{_includedir}/marlinutil/mille
%{_includedir}/marlinutil/*.h
%{_includedir}/marlinutil/*.ipp
%{_includedir}/marlinutil/ANN/*.h
%{_includedir}/marlinutil/mille/*.h

%changelog
* Mon Jan 29 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.17.2-1
- New version of Marlin utils
* Mon Jan 23 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.17.0-1
- New version of Marlin utils
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.16.2-1
- New version of Marlin utils
* Mon Jun 15 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.15.1-1
- Repackaging for CentOS 8


