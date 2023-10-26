%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.16.5
%global _tagver 00-16-05

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
BuildRequires: root
BuildRequires: root-tpython
BuildRequires: python3-devel
BuildRequires: python3-rpm-macros

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
      -DCMAKE_CXX_STANDARD=17 \
      -DBUILD_TESTING=OFF \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

rm %{buildroot}/%{_prefix}/python/EventStore.py

mkdir -p %{buildroot}/%{_datadir}/podio
mv %{buildroot}/%{_prefix}/python/templates %{buildroot}/%{_datadir}/podio
mkdir -p %{buildroot}/%{python3_sitelib}
mv %{buildroot}/%{_prefix}/python/* %{buildroot}/%{python3_sitelib}

sed -i 's|^TEMPLATE_DIR.*|TEMPLATE_DIR = "%{_datadir}/podio/templates"|g' \
    %{buildroot}/%{python3_sitelib}/podio_class_generator.py

sed -i 's|^set_and_check(podio_PYTHON_DIR.*|set_and_check(podio_PYTHON_DIR "%{python3_sitelib}")|g' \
    %{buildroot}/%{cmake_podio_dir}/podioConfig.cmake

sed -i 's|${podio_PYTHON_DIR}/templates/CMakeLists.txt|%{_datadir}/podio/templates/CMakeLists.txt|g' \
    %{buildroot}/%{cmake_podio_dir}/podioMacros.cmake

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.pcm
%{_libdir}/*.rootmap
%{_bindir}/*
%dir %{_datadir}/doc/podio
%{_datadir}/doc/podio/NOTICE


%package devel
Summary: Library handling data models in particle physics (development files).
Requires: %{name}
Requires: root
Requires: root-tpython
Requires: python3-devel

%description devel
PODIO is a C++ library to support the creation and handling of data models in particle physics.

%files devel
%defattr(-,root,root)
%dir %{cmake_podio_dir}
%{cmake_podio_dir}/*.cmake
%dir %{_includedir}/podio
%dir %{_includedir}/podio/utilities
%{_includedir}/podio/*.h
%{_includedir}/podio/utilities/*.h


%package -n python3-podio
Summary: Library handling data models in particle physics (python modules).
BuildArch: noarch
Requires: %{name}

%description -n python3-podio
PODIO is a C++ library to support the creation and handling of data models in particle physics.

%files -n python3-podio
%defattr(-,root,root)
%dir %{python3_sitelib}/podio
%dir %{python3_sitelib}/podio/__pycache__
%{python3_sitelib}/podio/*.py
%{python3_sitelib}/podio/__pycache__/*

%package -n python3-podio-utils
Summary: Library handling data models in particle physics (tools and models).
BuildArch: noarch
Requires: %{name}
Requires: python3-podio

%description -n python3-podio-utils
PODIO is a C++ library to support the creation and handling of data models in particle physics.

%files -n python3-podio-utils
%defattr(-,root,root)
%{python3_sitelib}/podio_class_generator.py
%{python3_sitelib}/podio_schema_evolution.py
%{python3_sitelib}/__pycache__
%{python3_sitelib}/__pycache__/*
%dir %{_datadir}/podio
%dir %{_datadir}/podio/templates
%dir %{_datadir}/podio/templates/macros
%dir %{_datadir}/podio/templates/schemaevolution
%{_datadir}/podio/templates/CMakeLists.txt
%{_datadir}/podio/templates/*.jinja2
%{_datadir}/podio/templates/macros/*.jinja2
%{_datadir}/podio/templates/schemaevolution/*.jinja2

%changelog
* Fri Oct 20 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.16.5-1
- Porting to AlmaLinux 9


