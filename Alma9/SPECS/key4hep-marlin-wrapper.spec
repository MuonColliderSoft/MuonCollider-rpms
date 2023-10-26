%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.6.0
%global _tagver 00-06

%global _sbuilddir %{_builddir}/%{name}-%{version}/k4MarlinWrapper-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

Summary: Gaudi algorithm wrapping Marlin processors.
Name: key4hep-marlin-wrapper
Version: %{_pver}
Release: 1%{?dist}
License: Apache License 2.0
URL: https://github.com/key4hep/k4MarlinWrapper
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: key4hep-fw-core-devel
BuildRequires: ilc-marlin-devel
BuildRequires: key4hep-edm4hep2lcio-devel
BuildRequires: key4hep-lcio-reader-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/key4hep/k4MarlinWrapper/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Gaudi algorithm wrapping Marlin processors.

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

rm -rf %{buildroot}%{_prefix}/lib

mkdir -p %{buildroot}/%{python3_sitelib}
mv %{buildroot}/%{_prefix}/python/k4MarlinWrapper %{buildroot}/%{python3_sitelib}/
rm -rf %{buildroot}/%{_prefix}/python

sed -i -e 's|env python|env python3|g' %{buildroot}/%{_bindir}/*

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.components
%{_libdir}/*.confdb
%{_libdir}/*.confdb2

%package -n python3-k4marlin-wrapper
Summary: Gaudi algorithm wrapping Marlin processors (python modules).
BuildArch: noarch
Requires: %{name}
Requires: python3-k4fwcore

%description -n python3-k4marlin-wrapper
Gaudi algorithm wrapping Marlin processors.

%files -n python3-k4marlin-wrapper
%defattr(-,root,root)
%dir %{python3_sitelib}/k4MarlinWrapper
%dir %{python3_sitelib}/k4MarlinWrapper/__pycache__
%{python3_sitelib}/k4MarlinWrapper/*.py
%{python3_sitelib}/k4MarlinWrapper/__pycache__/*
%{_bindir}/*.py
%dir %{_datadir}/k4MarlinWrapper
%dir %{_datadir}/k4MarlinWrapper/examples
%{_datadir}/k4MarlinWrapper/examples/*.py


%changelog
* Wed Oct 25 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.6.0-1
- Porting to AlmaLinux 9

