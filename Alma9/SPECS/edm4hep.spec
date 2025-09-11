%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.99.2
%global _tagver 00-99-02

%global _sbuilddir %{_builddir}/%{name}-%{version}/EDM4hep-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_edm4hep_dir %{_libdir}/cmake/EDM4HEP

Summary: A generic event data model for future HEP collider experiments.
Name: edm4hep
Version: %{_pver}
Release: 1%{?dist}
License: Apache License 2.0
URL: https://github.com/key4hep/EDM4hep
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: podio-devel
BuildRequires: python3-podio-utils
BuildRequires: python3-jinja2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/key4hep/EDM4hep/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
A generic event data model for future HEP collider experiments.

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
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
chrpath --delete %{buildroot}%{_libdir}/*.so
chrpath --delete %{buildroot}%{_bindir}/edm4hep2json

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.pcm
%{_libdir}/*.rootmap
%{_bindir}/edm4hep2json
%dir %{_datadir}/doc/EDM4HEP
%{_datadir}/doc/EDM4HEP/*
%dir %{_datadir}/edm4hep
%{_datadir}/edm4hep/*

%package devel
Summary: A generic event data model for future HEP collider experiments (development files).
Requires: %{name}
Requires: podio-devel

%description devel
A generic event data model for future HEP collider experiments.

%files devel
%defattr(-,root,root)
%dir %{cmake_edm4hep_dir}
%{cmake_edm4hep_dir}/*.cmake
%dir %{_includedir}/edm4hep
%dir %{_includedir}/edm4hep/utils
%{_includedir}/edm4hep/*.h
%{_includedir}/edm4hep/utils/*.h

%package -n python3-edm4hep
Summary: A generic event data model for future HEP collider experiments (python modules).
BuildArch: noarch
Requires: %{name}
Requires: python3-podio

%description -n python3-edm4hep
A generic event data model for future HEP collider experiments.

%files -n python3-edm4hep
%defattr(-,root,root)
%dir %{python3_sitearch}/edm4hep
%dir %{python3_sitearch}/edm4hep/__pycache__
%{python3_sitearch}/edm4hep/*.py
%{python3_sitearch}/edm4hep/__pycache__/*.pyc

%changelog
* Mon Aug 04 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.99.2-1
- New version
* Fri Jan 10 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.99.0-1
- New version
* Wed May 22 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.10.5-1
- Porting to AlmaLinux 9




