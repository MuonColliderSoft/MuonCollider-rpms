%global debug_package %{nil}

%global _pver 2.4.6
#global _pver 2.4.1
%global _prel 3

%global _sbuilddir %{_builddir}/clhep/%{_pver}.%{_prel}/CLHEP
%global _cbuilddir %{_builddir}/clhep/build

Summary: HEP-specific foundation and utility classes
Name: clhep
Version: %{_pver}
Release: %{_prel}.muonc%{?dist}
License: GPL v.3
Vendor: CERN
URL: http://proj-clhep.web.cern.ch/proj-clhep/
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%undefine _disable_source_fetch
Source: https://proj-clhep.web.cern.ch/proj-clhep/dist1/%{name}-%{version}.%{_prel}.tgz

%description
CLHEP is a set of HEP-specific foundation and utility classes such as
random generators, physics vectors, geometry and linear algebra.

%prep
%setup -c -n %{name}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DLIB_SUFFIX=64 \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
sed -i 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}/usr/bin/*-config

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so

%package devel
Summary: HEP-specific foundation and utility classes, development files
Requires: %{name}
Provides: pkgconfig(=;clhep-random)

%description devel
CLHEP is a set of HEP-specific foundation and utility classes such as
random generators, physics vectors, geometry and linear algebra.

%files devel
%defattr(-,root,root)
/usr/bin/*
%{_libdir}/*.a
%dir %{_libdir}/CLHEP-%{version}.3
%{_libdir}/CLHEP-%{version}.3/*.cmake
%dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%{_includedir}/clhep.modulemap
%dir %{_includedir}/CLHEP
%{_includedir}/CLHEP/*.h
%dir %{_includedir}/CLHEP/Cast
%{_includedir}/CLHEP/Cast/*.h
%dir %{_includedir}/CLHEP/Evaluator
%{_includedir}/CLHEP/Evaluator/*.h
%dir %{_includedir}/CLHEP/Exceptions
%{_includedir}/CLHEP/Exceptions/*.h
%{_includedir}/CLHEP/Exceptions/*.icc
%{_includedir}/CLHEP/Exceptions/*.mk
%dir %{_includedir}/CLHEP/GenericFunctions
%{_includedir}/CLHEP/GenericFunctions/*.h
%{_includedir}/CLHEP/GenericFunctions/*.hh
%{_includedir}/CLHEP/GenericFunctions/*.icc
%dir %{_includedir}/CLHEP/Geometry
%{_includedir}/CLHEP/Geometry/*.h
%{_includedir}/CLHEP/Geometry/*.icc
%dir %{_includedir}/CLHEP/Matrix
%{_includedir}/CLHEP/Matrix/*.h
%{_includedir}/CLHEP/Matrix/*.icc
%dir %{_includedir}/CLHEP/Random
%{_includedir}/CLHEP/Random/*.h
%{_includedir}/CLHEP/Random/*.icc
%dir %{_includedir}/CLHEP/RandomObjects
%{_includedir}/CLHEP/RandomObjects/*.h
%{_includedir}/CLHEP/RandomObjects/*.icc
%dir %{_includedir}/CLHEP/RefCount
%{_includedir}/CLHEP/RefCount/*.h
%{_includedir}/CLHEP/RefCount/*.icc
%dir %{_includedir}/CLHEP/Units
%{_includedir}/CLHEP/Units/*.h
%dir %{_includedir}/CLHEP/Utility
%{_includedir}/CLHEP/Utility/*.h
%dir %{_includedir}/CLHEP/Vector
%{_includedir}/CLHEP/Vector/*.h
%{_includedir}/CLHEP/Vector/*.icc


%changelog
* Thu Feb 02 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.4.6-3
- Repackaging for Alma Linux 9
* Thu Jan 30 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.4.1-3
- Repackaging for CentOS 7





