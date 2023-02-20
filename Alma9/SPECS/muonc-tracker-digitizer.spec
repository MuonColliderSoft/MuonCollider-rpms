%global _pver 1.0.0
%global _tagver master

%global _maindir %{_builddir}/%{name}-%{version}

Summary: Marlin processors for tracker digitization
Name: muonc-tracker-digitizer
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/MuonCVXDDigitiser
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
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
AutoReqProv: yes

%description
A collection of processors for the digitization of hits
in the Muon Collider tracker.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/MuonColliderSoft/MuonCVXDDigitiser %{_maindir}
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
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libMuonCVXDDigitiser.so:%{_libdir}/libMuonCVXDRealDigitiser.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/muonc-tracker-digitizer.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMuonCVXDDigitiser.so:%{_libdir}/libMuonCVXDRealDigitiser.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/muonc-tracker-digitizer.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Mon Jan 23 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.0.0-1
- First version of Muon Collider Tracker Digitizer



