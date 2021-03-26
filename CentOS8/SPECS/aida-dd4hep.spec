%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_dd4hep_dir %{_datadir}/DD4hep/cmake
%global _pypkg python36
%global _pycmd python3
%global _pylibdir %{_prefix}/lib/python3.6/site-packages
%global _boostp boost169

Summary: Detector description and life cycle framework
Name: aida-dd4hep
Version: 1.13.1
Release: 1%{?dist}
License: GPL v.3
Vendor: CERN
URL: https://github.com/AIDASoft/DD4hep
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg} >= 3.14.5-1
BuildRequires: make
BuildRequires: %{_pypkg}
BuildRequires: %{_pypkg}-rpm-macros
BuildRequires: python3-root
BuildRequires: python36-devel
BuildRequires: ilc-gear-devel
BuildRequires: ilc-lcio-devel
BuildRequires: %{_boostp}-devel
BuildRequires: geant4-devel
BuildRequires: root-genvector
BuildRequires: root-tpython
BuildRequires: root-graf3d-eve7
BuildRequires: root-gui-browserv7
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source0: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source0: %{name}-%{version}.tar.gz
%endif
Source1: aida-setup.sh
Source2: aida-setup.csh

%description
DD4hep is a software framework for providing a complete solution
for full detector description (geometry, materials, visualization,
readout, alignment, calibration, etc.) for the full experiment life
cycle (detector concept development, detector optimization, construction, operation).

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=17 \
             -DDD4HEP_USE_GEANT4=ON \
             -DDD4HEP_USE_LCIO=ON \
             -DDD4HEP_USE_XERCESC=OFF \
             -DDD4HEP_USE_GEAR=ON \
             -DBUILD_TESTING=OFF \
             -DDD4HEP_SET_RPATH=OFF \
             -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
             -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

rm -rf %{buildroot}%{_pylibdir}/DDSim/bin

mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}%{_prefix}/lib/*.so* \
   %{buildroot}%{_prefix}/lib/*.pcm \
   %{buildroot}%{_prefix}/lib/*.components %{buildroot}%{_libdir}

mkdir -p %{buildroot}%{_datadir}/DD4hep
mv %{buildroot}%{_prefix}/DDDetectors %{buildroot}%{_prefix}/examples %{buildroot}%{_datadir}/DD4hep

mv %{buildroot}%{_prefix}/cmake %{buildroot}%{_datadir}/DD4hep
sed -i -e 's|/include|/include/dd4hep|g' %{buildroot}%{cmake_dd4hep_dir}/DD4hepConfig-targets.cmake

mv %{buildroot}%{_prefix}/include %{buildroot}%{_prefix}/dd4hep
mkdir -p %{buildroot}%{_includedir}
mv %{buildroot}%{_prefix}/dd4hep %{buildroot}%{_includedir}

sed -i -e 's|env python|env %{_pycmd}|g' %{buildroot}%{_bindir}/check* \
                                         %{buildroot}%{_bindir}/ddsim \
                                         %{buildroot}%{_bindir}/g4MaterialScan
sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' %{buildroot}%{_bindir}/run_test.sh

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d

#workaround for cmake
ln -sf %{_bindir}     %{buildroot}%{_datadir}/DD4hep/bin
ln -sf %{_libdir}     %{buildroot}%{_datadir}/DD4hep/lib
ln -sf %{_includedir} %{buildroot}%{_datadir}/DD4hep/include

#workaround for bad default option
sed -i -e 's|@DD4HEP_USE_HEPMC3@|OFF|g' %{buildroot}%{_pylibdir}/DDSim/Helper/HepMC3.py

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/aida-setup.*
%{_bindir}/ddeve
%{_bindir}/dumpBfield
%{_bindir}/dumpdetector
%{_bindir}/g4FromXML
%{_bindir}/g4gdmlDisplay
%{_bindir}/geoConverter
%{_bindir}/geoDisplay
%{_bindir}/geoPluginRun
%{_bindir}/graphicalScan
%{_bindir}/listcomponents
%{_bindir}/materialBudget
%{_bindir}/print_materials
%{_bindir}/pyddg4
%{_bindir}/materialScan
%{_bindir}/teveDisplay
%{_bindir}/teveLCIO
%{_libdir}/*.so.*
%{_libdir}/*.pcm
%{_libdir}/*.components
%dir %{_datadir}/DD4hep
%dir %{_datadir}/DD4hep/DDDetectors/
%dir %{_datadir}/DD4hep/DDDetectors/compact/
%dir %{_datadir}/DD4hep/DDDetectors/compact/SiD
%dir %{_datadir}/DD4hep/examples
%dir %{_datadir}/DD4hep/examples/DDEve
%dir %{_datadir}/DD4hep/examples/DDG4
%dir %{_datadir}/DD4hep/examples/DDG4/examples
%{_datadir}/DD4hep/DDDetectors/compact/*.xml
%{_datadir}/DD4hep/DDDetectors/compact/SiD/*.xml
%{_datadir}/DD4hep/examples/DDEve/*
%{_datadir}/DD4hep/examples/DDG4/examples/*

%package devel
Summary: Detector description and life cycle framework (development files)
Requires: %{name}
Requires: ilc-gear-devel
Requires: ilc-lcio-devel
Requires: %{_boostp}-devel
Requires: geant4-devel
Requires: root-genvector
Requires: root-tpython
Requires: root-graf3d-eve7
Requires: root-gui-browserv7

%description devel
DD4hep is a software framework for providing a complete solution
for full detector description (geometry, materials, visualization,
readout, alignment, calibration, etc.) for the full experiment life
cycle (detector concept development, detector optimization, construction, operation).

%files devel
%defattr(-,root,root)
%{_bindir}/*.sh
%{_libdir}/*.so
%dir %{_includedir}/dd4hep
%dir %{_includedir}/dd4hep/DD4hep
%dir %{_includedir}/dd4hep/DD4hep/detail
%dir %{_includedir}/dd4hep/DDAlign
%dir %{_includedir}/dd4hep/DDCond
%dir %{_includedir}/dd4hep/DDCond/Type1
%dir %{_includedir}/dd4hep/DDDigi
%dir %{_includedir}/dd4hep/DDDigi/segmentations
%dir %{_includedir}/dd4hep/DDEve
%dir %{_includedir}/dd4hep/DDG4
%dir %{_includedir}/dd4hep/DDG4/Python
%dir %{_includedir}/dd4hep/DDRec
%dir %{_includedir}/dd4hep/DDSegmentation
%dir %{_includedir}/dd4hep/Evaluator
%dir %{_includedir}/dd4hep/JSON
%dir %{_includedir}/dd4hep/Parsers
%dir %{_includedir}/dd4hep/Parsers/spirit
%dir %{_includedir}/dd4hep/Parsers/detail
%dir %{_includedir}/dd4hep/ROOT
%dir %{_includedir}/dd4hep/XML
%{_includedir}/dd4hep/DD4hep/*.h
%{_includedir}/dd4hep/DD4hep/detail/*.h
%{_includedir}/dd4hep/DD4hep/detail/*.inl
%{_includedir}/dd4hep/DDAlign/*.h
%{_includedir}/dd4hep/DDCond/*.h
%{_includedir}/dd4hep/DDCond/Type1/*.h
%{_includedir}/dd4hep/DDDigi/*.h
%{_includedir}/dd4hep/DDDigi/segmentations/*.h
%{_includedir}/dd4hep/DDEve/*.h
%{_includedir}/dd4hep/DDG4/*.h
%{_includedir}/dd4hep/DDG4/*.inl
%{_includedir}/dd4hep/DDG4/Python/*.h
%{_includedir}/dd4hep/DDRec/*.h
%{_includedir}/dd4hep/DDSegmentation/*.h
%{_includedir}/dd4hep/Evaluator/*.h
%{_includedir}/dd4hep/JSON/*.h
%{_includedir}/dd4hep/JSON/*.inl
%{_includedir}/dd4hep/Parsers/*.h
%{_includedir}/dd4hep/Parsers/spirit/*.h
%{_includedir}/dd4hep/Parsers/detail/*.h
%{_includedir}/dd4hep/Parsers/detail/*.imp
%{_includedir}/dd4hep/Parsers/detail/*.inl
%{_includedir}/dd4hep/Parsers/detail/*.txt
%{_includedir}/dd4hep/ROOT/*.h
%{_includedir}/dd4hep/XML/*.h
%{_includedir}/dd4hep/XML/*.inl
%dir %{cmake_dd4hep_dir}
%{cmake_dd4hep_dir}/*
#workaround for cmake
%{_datadir}/DD4hep/bin
%{_datadir}/DD4hep/lib
%{_datadir}/DD4hep/include

%package -n python3-dd4hep
Summary: Event data model and persistency for Linear Collider detector (python files)
BuildArch: noarch
Requires: %{name}
Requires: %{name}-devel
Requires: %{_pypkg}
Requires: python3-root

%description -n python3-dd4hep
DD4hep is a software framework for providing a complete solution
for full detector description (geometry, materials, visualization,
readout, alignment, calibration, etc.) for the full experiment life
cycle (detector concept development, detector optimization, construction, operation).

%files -n python3-dd4hep
%defattr(-,root,root)
%{_bindir}/checkGeometry
%{_bindir}/checkOverlaps
%{_bindir}/ddsim
%{_bindir}/g4MaterialScan
%dir %{_pylibdir}/DDSim
%dir %{_pylibdir}/DDSim/Helper
%{_pylibdir}/*.py
%{_pylibdir}/*.C
%{_pylibdir}/DDSim/*.py
%{_pylibdir}/DDSim/Helper/*.py


%changelog
* Wed Sep 23 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.13.1-1
- New version with ROOT 6.22 support
* Fri May 29 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.12.1-1
- Repackaging for CentOS 8


