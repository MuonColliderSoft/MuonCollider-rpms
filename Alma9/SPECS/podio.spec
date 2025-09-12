%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.3.0
%global _tagver 01-03

%global _sbuilddir %{_builddir}/%{name}-%{version}/podio-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_podio_dir %{_libdir}/cmake/podio

Summary: Library handling data models in particle physics.
Name: podio
Version: %{_pver}
Release: 1%{?dist}
License: Apache License 2.0
URL: https://github.com/AIDASoft/podio
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: root
BuildRequires: root-tpython
BuildRequires: python3-devel
BuildRequires: python3-rpm-macros
BuildRequires: fmt-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/AIDASoft/podio/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
PODIO is a C++ library to support the creation and handling of data models in particle physics.

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

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.pcm
%{_libdir}/*.rootmap
%dir %{_datadir}/doc/podio
%{_datadir}/doc/podio/*


%package devel
Summary: Library handling data models in particle physics (development files).
Requires: %{name}
Requires: root
Requires: root-tpython
Requires: python3-devel
Requires: fmt-devel

%description devel
PODIO is a C++ library to support the creation and handling of data models in particle physics.

%files devel
%defattr(-,root,root)
%dir %{cmake_podio_dir}
%{cmake_podio_dir}/*.cmake
%dir %{_includedir}/podio
%dir %{_includedir}/podio/detail
%dir %{_includedir}/podio/utilities
%{_includedir}/podio/*.h
%{_includedir}/podio/detail/*.h
%{_includedir}/podio/utilities/*.h


%package -n python3-podio
Summary: Library handling data models in particle physics (python modules).
BuildArch: noarch
Requires: %{name}

%description -n python3-podio
PODIO is a C++ library to support the creation and handling of data models in particle physics.

%files -n python3-podio
%defattr(-,root,root)
%dir %{python3_sitearch}/podio
%dir %{python3_sitearch}/podio_gen
%dir %{python3_sitearch}/podio/pythonizations
%dir %{python3_sitearch}/podio/pythonizations/utils
%dir %{python3_sitearch}/podio/__pycache__
%dir %{python3_sitearch}/podio_gen/__pycache__
%dir %{python3_sitearch}/podio/pythonizations/__pycache__
%dir %{python3_sitearch}/podio/pythonizations/utils/__pycache__
%{python3_sitearch}/podio_version.py
%{python3_sitearch}/__pycache__/podio_version.*
%{python3_sitearch}/podio/*.py
%{python3_sitearch}/podio/__pycache__/*
%{python3_sitearch}/podio_gen/*.py
%{python3_sitearch}/podio_gen/__pycache__/*
%{python3_sitearch}/podio/pythonizations/*.py
%{python3_sitearch}/podio/pythonizations/__pycache__/*
%{python3_sitearch}/podio/pythonizations/utils/*.py
%{python3_sitearch}/podio/pythonizations/utils/__pycache__/*

%package -n python3-podio-utils
Summary: Library handling data models in particle physics (tools and models).
Requires: %{name}
Requires: python3-podio
Requires: python3-tabulate+widechars
Requires: python3-pyyaml
Requires: python3-graphviz

%description -n python3-podio-utils
PODIO is a C++ library to support the creation and handling of data models in particle physics.

%files -n python3-podio-utils
%defattr(-,root,root)
%{_bindir}/*
%{python3_sitearch}/podio_class_generator.py
%{python3_sitearch}/podio_schema_evolution.py
%{python3_sitearch}/__pycache__/podio_class_generator.*
%{python3_sitearch}/__pycache__/podio_schema_evolution.*
%{python3_sitearch}/templates/CMakeLists.txt
%{python3_sitearch}/templates/*.jinja2
%{python3_sitearch}/templates/macros/*.jinja2
%{python3_sitearch}/templates/schemaevolution/*.jinja2
%{python3_sitearch}/templates/.clang-format

%changelog
* Mon Aug 04 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.3.0-1
- New version
* Fri Jan 10 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.1.0-1
- New version
* Fri Feb 09 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.17.3-1
- Porting to AlmaLinux 9


