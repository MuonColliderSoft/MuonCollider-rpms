%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.5.0
%global _tagver 00.05

%global _sbuilddir %{_builddir}/%{name}-%{version}/k4LCIOReader-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_lcioreader_dir %{_libdir}/cmake/k4LCIOReader

Summary: Generate EDM4hep data collections on the fly from LCIO input files.
Name: key4hep-lcio-reader
Version: %{_pver}
Release: 1%{?dist}
License: Apache License 2.0
URL: https://github.com/key4hep/k4LCIOReader
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: root
BuildRequires: key4hep-fw-core-devel
BuildRequires: python3-rpm-macros

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/key4hep/k4LCIOReader/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Generate EDM4hep data collections on the fly from LCIO input files.

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
      -DBUILD_TESTING=OFF \
      -DCPPGSL_INCLUDE_DIR=/opt/GSL/include \
      -DCMAKE_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
mv %{buildroot}%{_prefix}/lib/cmake/k4LCIOReader/* %{buildroot}%{cmake_lcioreader_dir}
rm -rf %{buildroot}%{_prefix}/lib

mkdir -p %{buildroot}/%{python3_sitelib}
mv %{buildroot}/%{_prefix}/python/LCIOInput %{buildroot}/%{python3_sitelib}/
rm -rf %{buildroot}/%{_prefix}/python

sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' %{buildroot}%{cmake_lcioreader_dir}/*.cmake

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.components
%{_libdir}/*.confdb
%{_libdir}/*.confdb2


%package devel
Summary: Generate EDM4hep data collections on the fly from LCIO input files (development files).
Requires: %{name}
Requires: root
Requires: key4hep-fw-core-devel

%description devel
Generate EDM4hep data collections on the fly from LCIO input files.

%files devel
%defattr(-,root,root)
%dir %{cmake_lcioreader_dir}
%{cmake_lcioreader_dir}/*.cmake
%{cmake_lcioreader_dir}/*.csv
%dir %{_includedir}/k4LCIOReader
%{_includedir}/k4LCIOReader/*.h

%package -n python3-k4lcioreader
Summary: Generate EDM4hep data collections on the fly from LCIO input files (python modules).
BuildArch: noarch
Requires: %{name}
Requires: python3-gaudi

%description -n python3-k4lcioreader
Generate EDM4hep data collections on the fly from LCIO input files.

%files -n python3-k4lcioreader
%defattr(-,root,root)
%dir %{python3_sitelib}/LCIOInput
%dir %{python3_sitelib}/LCIOInput/__pycache__
%{python3_sitelib}/LCIOInput/*.py
%{python3_sitelib}/LCIOInput/__pycache__/*



%changelog
* Wed Oct 25 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.5.0-1
- Porting to AlmaLinux 9

