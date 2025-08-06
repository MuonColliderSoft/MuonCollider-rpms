%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.1.0
%global _tagver 0.1.0

%global _sbuilddir %{_builddir}/%{name}-%{version}/k4GaudiPandora-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_k4gpand_dir %{_libdir}/cmake/k4GaudiPandora

Summary: Gaudi algorithms based on Pandora PFA.
Name: key4hep-gaudi-pandora
Version: %{_pver}
Release: 1%{?dist}
License: Apache License 2.0
URL: https://github.com/key4hep/k4GaudiPandora
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: key4hep-fw-core-devel
BuildRequires: python3-podio-utils
BuildRequires: pandora-pfa-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/key4hep/k4GaudiPandora/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Gaudi algorithms based on Pandora PFA.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=20 \
      -DBUILD_TESTING=OFF \
      -DCPPGSL_INCLUDE_DIR=/opt/GSL/include \
      -DCMAKE_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
chrpath --delete %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{cmake_k4gpand_dir}
mv %{buildroot}%{_prefix}/lib/cmake/k4GaudiPandora/* %{buildroot}%{cmake_k4gpand_dir}
rm -rf %{buildroot}%{_prefix}/lib/

mkdir -p %{buildroot}%{python3_sitelib}
mv %{buildroot}%{_prefix}/python/k4GaudiPandora %{buildroot}%{python3_sitelib}
rm -rf %{buildroot}%{_prefix}/python

sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' %{buildroot}%{cmake_k4gpand_dir}/*.cmake

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
Summary: GGaudi algorithms based on Pandora PFA (development files).
Requires: %{name}
Requires: key4hep-fw-core-devel
Requires: pandora-pfa-devel

%description devel
Gaudi algorithms based on Pandora PFA.

%files devel
%defattr(-,root,root)
%dir %{cmake_k4gpand_dir}
%{cmake_k4gpand_dir}/*.cmake
%{cmake_k4gpand_dir}/*.csv
%dir %{_includedir}/k4GaudiPandora
%{_includedir}/k4GaudiPandora/*.h


%package -n python3-k4GaudiPandora
Summary: Gaudi algorithms based on Pandora PFA (python modules).
BuildArch: noarch
Requires: %{name}
Requires: python3-k4fwcore

%description -n python3-k4GaudiPandora
Gaudi algorithms based on Pandora PFA.

%files -n python3-k4GaudiPandora
%defattr(-,root,root)
%dir %{python3_sitelib}/k4GaudiPandora
%dir %{python3_sitelib}/k4GaudiPandora/__pycache__
%{python3_sitelib}/k4GaudiPandora/*.py
%{python3_sitelib}/k4GaudiPandora/__pycache__/*


%changelog
* Wed Aug 06 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.1.0-1
- Porting to AlmaLinux

