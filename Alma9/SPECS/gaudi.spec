%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.36.16
%global _tagver v36r16

%global _sbuilddir %{_builddir}/%{name}-%{version}/Gaudi-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_gaudi_dir %{_libdir}/cmake/Gaudi

Summary: Interfaces and services for building HEP experiment frameworks
Name: gaudi
Version: %{_pver}
Release: 1%{?dist}
License: APL CERNINFN
URL: https://gitlab.cern.ch/gaudi/Gaudi
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: python3
BuildRequires: python3-rpm-macros
BuildRequires: root
BuildRequires: root-genvector
BuildRequires: root-smatrix
BuildRequires: root-io-xml
BuildRequires: root-io-xmlparser
BuildRequires: root-tpython
BuildRequires: boost-devel
BuildRequires: boost-python3
BuildRequires: tbb-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel
BuildRequires: libuuid-devel
BuildRequires: range-v3-devel
BuildRequires: fmt-devel
BuildRequires: xerces-c-devel
BuildRequires: jemalloc-devel
BuildRequires: libunwind-devel
BuildRequires: ilc-root-aida-devel
BuildRequires: clhep-devel
BuildRequires: cpp-gsl-devel
BuildRequires: python3-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://gitlab.cern.ch/gaudi/Gaudi/-/archive/%{_tagver}/Gaudi-%{_tagver}.tar.gz
AutoReqProv: yes

%description
The Gaudi project is an open project for providing the necessary interfaces
and services for building HEP experiment frameworks in the domain of event data
processing applications.

%prep
%setup -c
sed -i -e 's|CONFIG REQUIRED system filesystem|REQUIRED system filesystem|g' \
       -e 's|thread python unit_test|thread python39 unit_test|g' \
    %{_sbuilddir}/cmake/GaudiDependencies.cmake
sed -i -e 's|Boost::python|Boost::python39|g' \
    %{_sbuilddir}/GaudiCoreSvc/CMakeLists.txt \
    %{_sbuilddir}/GaudiExamples/CMakeLists.txt \
    %{_sbuilddir}/GaudiProfiling/CMakeLists.txt
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DGAUDI_USE_AIDA=ON \
      -DGAUDI_USE_HEPPDT=OFF \
      -DGAUDI_USE_CLHEP=ON \
      -DGAUDI_USE_GPERFTOOLS=OFF \
      -DGAUDI_USE_CPPUNIT=OFF \
      -DGAUDI_USE_UNWIND=ON \
      -DGAUDI_USE_INTELAMPLIFIER=OFF \
      -DGAUDI_USE_JEMALLOC=ON \
      -DGAUDI_USE_DOXYGEN=OFF \
      -DGAUDI_USE_XERCESC=ON \
      -DBUILD_TESTING=OFF \
      -DCPPGSL_ROOT_DIR=/opt/GSL/include \
      -DCMAKE_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
      -DGAUDI_INSTALL_PYTHONDIR=%{buildroot}%{python3_sitelib} \
      -DGAUDI_INSTALL_CONFIGDIR=%{buildroot}%{cmake_gaudi_dir} \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_gaudi_dir}/*.cmake
sed -i -e 's|env python|python3|g' \
       %{buildroot}%{_bindir}/quick-merge \
       %{buildroot}%{_bindir}/GaudiProfiler

rm -f %{buildroot}%{_bindir}/*.bat
rm -rf %{buildroot}%{python3_sitelib}/GaudiConfig/__pycache__ \
       %{buildroot}%{python3_sitelib}/GaudiKernel/__pycache__ \
       %{buildroot}%{python3_sitelib}/Gaudi/__pycache__

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.pcm
%{_libdir}/*.rootmap
%{_libdir}/Gaudi.confdb*
%{_libdir}/Gaudi.components

%package devel
Summary: Interfaces and services for building HEP experiment frameworks (development files)
Requires: %{name}
Requires: root
Requires: root-genvector
Requires: root-smatrix
Requires: root-io-xml
Requires: root-io-xmlparser
Requires: root-tpython
Requires: boost-devel
Requires: boost-python3
Requires: tbb-devel
Requires: xz-devel
Requires: zlib-devel
Requires: libuuid-devel
Requires: range-v3-devel
Requires: fmt-devel
Requires: xerces-c-devel
Requires: jemalloc-devel
Requires: libunwind-devel
Requires: ilc-root-aida-devel
Requires: clhep-devel
Requires: cpp-gsl-devel
Requires: python3-devel

%description devel
The Gaudi project is an open project for providing the necessary interfaces
and services for building HEP experiment frameworks in the domain of event data
processing applications.

%files devel
%defattr(-,root,root)
%dir %{cmake_gaudi_dir}
%dir %{cmake_gaudi_dir}/modules
%{cmake_gaudi_dir}/*.cmake
%{cmake_gaudi_dir}/extract_qmtest_metadata.py
%{cmake_gaudi_dir}/header_build_test.tpl
%{cmake_gaudi_dir}/headers_db.csv
%{cmake_gaudi_dir}/scan_dict_deps.py
%{cmake_gaudi_dir}/modules/*.cmake
%dir %{_includedir}/Gaudi
%dir %{_includedir}/Gaudi/Accumulators
%dir %{_includedir}/Gaudi/Allocator
%dir %{_includedir}/Gaudi/Arena
%dir %{_includedir}/Gaudi/Chrono
%dir %{_includedir}/Gaudi/Details
%dir %{_includedir}/Gaudi/Histograming
%dir %{_includedir}/Gaudi/Histograming/Sink
%dir %{_includedir}/Gaudi/Interfaces
%dir %{_includedir}/Gaudi/Parsers
%dir %{_includedir}/Gaudi/Timers
%dir %{_includedir}/GaudiAlg
%dir %{_includedir}/GaudiCommonSvc
%dir %{_includedir}/GaudiKernel
%dir %{_includedir}/GaudiMP
%dir %{_includedir}/GaudiPython
%dir %{_includedir}/GaudiUtils
%dir %{_includedir}/RootCnv
%{_includedir}/GAUDI_VERSION.h
%{_includedir}/Gaudi/*.h
%{_includedir}/Gaudi/Accumulators/*.h
%{_includedir}/Gaudi/Allocator/*.h
%{_includedir}/Gaudi/Arena/*.h
%{_includedir}/Gaudi/Chrono/*.h
%{_includedir}/Gaudi/Details/*.h
%{_includedir}/Gaudi/Histograming/Sink/*.h
%{_includedir}/Gaudi/Interfaces/*.h
%{_includedir}/Gaudi/Parsers/*.h
%{_includedir}/Gaudi/Timers/*.h
%{_includedir}/GaudiAlg/*.h
%{_includedir}/GaudiAlg/*.icpp
%{_includedir}/GaudiCommonSvc/*.h
%{_includedir}/GaudiKernel/*.h
%{_includedir}/GaudiKernel/*.icpp
%{_includedir}/GaudiMP/*.h
%{_includedir}/GaudiPython/*.h
%{_includedir}/GaudiUtils/*.h
%{_includedir}/RootCnv/*.h

%package -n python3-gaudi
Summary: Interfaces and services for building HEP experiment frameworks (python modules)
Requires: %{name}

%description -n python3-gaudi
The Gaudi project is an open project for providing the necessary interfaces
and services for building HEP experiment frameworks in the domain of event data
processing applications.

%files -n python3-gaudi
%defattr(-,root,root)
%dir %{python3_sitelib}/GaudiPluginService
%dir %{python3_sitelib}/GaudiTesting
%dir %{python3_sitelib}/GaudiTesting/pytest
%dir %{python3_sitelib}/GaudiConfig
%dir %{python3_sitelib}/GaudiKernel
%dir %{python3_sitelib}/GaudiConfig2
%dir %{python3_sitelib}/GaudiCoreSvc
%dir %{python3_sitelib}/GaudiUtils
%dir %{python3_sitelib}/Gaudi
%dir %{python3_sitelib}/GaudiAlg
%dir %{python3_sitelib}/GaudiAud
%dir %{python3_sitelib}/GaudiCommonSvc
%dir %{python3_sitelib}/GaudiHive
%dir %{python3_sitelib}/GaudiMonitor
%dir %{python3_sitelib}/GaudiMP
%dir %{python3_sitelib}/GaudiPartProp
%dir %{python3_sitelib}/GaudiProfiling
%dir %{python3_sitelib}/GaudiPython
%dir %{python3_sitelib}/GaudiSvc
%dir %{python3_sitelib}/RootCnv
%dir %{python3_sitelib}/RootHistCnv
%{python3_sitelib}/*.py
%{python3_sitelib}/GaudiPluginService/*.py
%{python3_sitelib}/GaudiTesting/*.py
%{python3_sitelib}/GaudiTesting/pytest/*.py
%{python3_sitelib}/GaudiConfig/*.py
%{python3_sitelib}/GaudiKernel/*.py
%{python3_sitelib}/GaudiConfig2/*.py
%{python3_sitelib}/GaudiCoreSvc/*.py
%{python3_sitelib}/GaudiUtils/*.py
%{python3_sitelib}/Gaudi/*.py
%{python3_sitelib}/GaudiAlg/*.py
%{python3_sitelib}/GaudiAud/*.py
%{python3_sitelib}/GaudiCommonSvc/*.py
%{python3_sitelib}/GaudiHive/*.py
%{python3_sitelib}/GaudiMonitor/*.py
%{python3_sitelib}/GaudiMP/*.py
%{python3_sitelib}/GaudiPartProp/*.py
%{python3_sitelib}/GaudiProfiling/*.py
%{python3_sitelib}/GaudiProfiling/*.so
%{python3_sitelib}/GaudiPython/*.py
%{python3_sitelib}/GaudiSvc/*.py
%{python3_sitelib}/RootCnv/*.py
%{python3_sitelib}/RootHistCnv/*.py
%dir %{python3_sitelib}/GaudiPluginService/__pycache__
%dir %{python3_sitelib}/GaudiTesting/__pycache__
%dir %{python3_sitelib}/GaudiTesting/pytest/__pycache__
%dir %{python3_sitelib}/GaudiConfig/__pycache__
%dir %{python3_sitelib}/GaudiKernel/__pycache__
%dir %{python3_sitelib}/GaudiConfig2/__pycache__
%dir %{python3_sitelib}/GaudiCoreSvc/__pycache__
%dir %{python3_sitelib}/GaudiUtils/__pycache__
%dir %{python3_sitelib}/Gaudi/__pycache__
%dir %{python3_sitelib}/GaudiAlg/__pycache__
%dir %{python3_sitelib}/GaudiAud/__pycache__
%dir %{python3_sitelib}/GaudiCommonSvc/__pycache__
%dir %{python3_sitelib}/GaudiHive/__pycache__
%dir %{python3_sitelib}/GaudiMonitor/__pycache__
%dir %{python3_sitelib}/GaudiMP/__pycache__
%dir %{python3_sitelib}/GaudiPartProp/__pycache__
%dir %{python3_sitelib}/GaudiProfiling/__pycache__
%dir %{python3_sitelib}/GaudiPython/__pycache__
%dir %{python3_sitelib}/GaudiSvc/__pycache__
%dir %{python3_sitelib}/RootCnv/__pycache__
%dir %{python3_sitelib}/RootHistCnv/__pycache__
%{python3_sitelib}/__pycache__/*.pyc
%{python3_sitelib}/GaudiPluginService/__pycache__/*.pyc
%{python3_sitelib}/GaudiTesting/__pycache__/*.pyc
%{python3_sitelib}/GaudiTesting/pytest/__pycache__/*.pyc
%{python3_sitelib}/GaudiConfig/__pycache__/*.pyc
%{python3_sitelib}/GaudiKernel/__pycache__/*.pyc
%{python3_sitelib}/GaudiConfig2/__pycache__/*.pyc
%{python3_sitelib}/GaudiCoreSvc/__pycache__/*.pyc
%{python3_sitelib}/GaudiUtils/__pycache__/*.pyc
%{python3_sitelib}/Gaudi/__pycache__/*.pyc
%{python3_sitelib}/GaudiAlg/__pycache__/*.pyc
%{python3_sitelib}/GaudiAud/__pycache__/*.pyc
%{python3_sitelib}/GaudiCommonSvc/__pycache__/*.pyc
%{python3_sitelib}/GaudiHive/__pycache__/*.pyc
%{python3_sitelib}/GaudiMonitor/__pycache__/*.pyc
%{python3_sitelib}/GaudiMP/__pycache__/*.pyc
%{python3_sitelib}/GaudiPartProp/__pycache__/*.pyc
%{python3_sitelib}/GaudiProfiling/__pycache__/*.pyc
%{python3_sitelib}/GaudiPython/__pycache__/*.pyc
%{python3_sitelib}/GaudiSvc/__pycache__/*.pyc
%{python3_sitelib}/RootCnv/__pycache__/*.pyc
%{python3_sitelib}/RootHistCnv/__pycache__/*.pyc


%package tools
Summary: Interfaces and services for building HEP experiment frameworks (tools)
Requires: %{name}
Requires: python3-gaudi

%description tools
The Gaudi project is an open project for providing the necessary interfaces
and services for building HEP experiment frameworks in the domain of event data
processing applications.

%files tools
%defattr(-,root,root)
%{_bindir}/*


%description tools
The Gaudi project is an open project for providing the necessary interfaces
and services for building HEP experiment frameworks in the domain of event data
processing applications.

%changelog
* Tue May 30 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.36.12-1
- Porting to AlmaLinux 9


