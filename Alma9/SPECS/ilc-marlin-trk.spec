%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 2.9.0
%global _tagver 02-09-01

%global _sbuilddir %{_builddir}/%{name}-%{version}/MarlinTrk-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global _boostp boost
%global cmake_martrk_dir %{_libdir}/cmake/MarlinTrk

Summary: Tracking Package for Marlin
Name: ilc-marlin-trk
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinTrk
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: root
BuildRequires: ilc-utils-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-gear-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: aida-tracking-toolkit-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/MarlinTrk/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Tracking Package based on LCIO and GEAR, primarily aimed at providing
track fitting in Marlin.

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
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_martrk_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{cmake_martrk_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_martrk_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so*

%package devel
Summary: Tracking Package for Marlin (development files)
Requires: %{name}
Requires: root
Requires: ilc-utils-devel
Requires: ilc-lcio-devel
Requires: ilc-gear-devel
Requires: ilc-marlin-devel
Requires: ilc-marlin-util-devel
Requires: aida-dd4hep-devel
Requires: aida-tracking-toolkit-devel

%description devel
Tracking Package based on LCIO and GEAR, primarily aimed at providing
track fitting in Marlin.

%files devel
%defattr(-,root,root)
%dir %{cmake_martrk_dir}
%{cmake_martrk_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/MarlinTrk
%{_includedir}/MarlinTrk/*.h

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.9.0-1
- New version of Marlin Tracking
* Mon Jul 13 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.8.0-1
- Repackaging for CentOS 8


