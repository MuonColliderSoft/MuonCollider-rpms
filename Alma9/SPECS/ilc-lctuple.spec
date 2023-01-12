%global _pver 1.14.0
%global _tagver v01-14-MC

%global _maindir %{_builddir}/%{name}-%{version}

Summary: Marlin package that creates a ROOT TTree with a column wise ntuple from LCIO collections
Name: ilc-lctuple
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/LCTuple
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Marlin package that creates a ROOT TTree with a column wise ntuple from LCIO collections.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/MuonColliderSoft/LCTuple %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_maindir}/build
cd %{_maindir}/build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libLCTuple.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-lctuple.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libLCTuple.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-lctuple.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.14.0-1
- New version of LCtuple
* Fri Dec 04 2020 Alessio Gianelle <gianelle@pd.infn.it> - 1.13.0-1
- Added track hits to the tracks branches
- Fixed the index assignment to the track hits
* Mon Sep 21 2020 Alessio Gianelle <gianelle@pd.infn.it> - 1.12.2-1
- Add branches for the time of the hits
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.12.1-1
- Repackaging for CentOS 8

