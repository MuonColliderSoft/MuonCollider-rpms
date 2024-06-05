%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.2.0
%global _tagver 00-02-RC1

%global _sbuilddir %{_builddir}/%{name}-%{version}/MuonCVXDDigitiser-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

Summary: Marlin processors for tracker digitization
Name: muonc-tracker-digitizer
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/MuonCVXDDigitiser
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: libgomp
BuildRequires: boost-devel
BuildRequires: root
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: gsl-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: ilc-root-aida-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/MuonCVXDDigitiser/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
A collection of processors for the digitization of hits
in the Muon Collider tracker.

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
printf "export MARLIN_DLL=\${MARLIN_DLL:+\${MARLIN_DLL}:}%{_libdir}/libMuonCVXDDigitiser.so:%{_libdir}/libMuonCVXDRealDigitiser.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/muonc-tracker-digitizer.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMuonCVXDDigitiser.so:%{_libdir}/libMuonCVXDRealDigitiser.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/muonc-tracker-digitizer.csh

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Fri May 31 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.2.0-1
- New version of Muon Collider Tracker Digitizer
* Wed Apr 26 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.1.0-1
- First version of Muon Collider Tracker Digitizer



