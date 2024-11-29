%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.15.2
%global _tagver MuSICv2-pre02

%global _sbuilddir %{_builddir}/%{name}-%{version}/LCTuple-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

Summary: Marlin package that creates a ROOT TTree with a column wise ntuple from LCIO collections
Name: ilc-lctuple
Version: %{_pver}
Release: 1.exper%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/LCTuple
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/LCTuple/archive/refs/tags/%{_tagver}.tar.gz
AutoReqProv: yes

%description
Marlin package that creates a ROOT TTree with a column wise ntuple from LCIO collections.

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
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\${MARLIN_DLL:+\${MARLIN_DLL}:}%{_libdir}/libLCTuple.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-lctuple.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libLCTuple.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-lctuple.csh

mkdir -p %{buildroot}%{_includedir}/LCTuple
cp %{_sbuilddir}/include/*.h %{buildroot}%{_includedir}/LCTuple

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so

%package devel
Summary: Marlin package that creates a ROOT TTree (header files).
Requires: %{name}

%description devel
Header files for marlin package that creates a ROOT TTree
with a column wise ntuple from LCIO collections.

%files devel
%defattr(-,root,root)
%dir %{_includedir}/LCTuple
%{_includedir}/LCTuple/*.h

%changelog
* Tue Feb 28 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.15.0-1
- New version of LCtuple
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.14.0-1
- New version of LCtuple
* Fri Dec 04 2020 Alessio Gianelle <gianelle@pd.infn.it> - 1.13.0-1
- Added track hits to the tracks branches
- Fixed the index assignment to the track hits
* Mon Sep 21 2020 Alessio Gianelle <gianelle@pd.infn.it> - 1.12.2-1
- Add branches for the time of the hits
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.12.1-1
- Repackaging for CentOS 8

