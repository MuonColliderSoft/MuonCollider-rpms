%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.12.1
%global _tagver 01-12-01-MC

%global _sbuilddir %{_builddir}/%{name}-%{version}/ConformalTracking-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global _boostp boost

Summary: Conformal Tracking for all-silicon trackers at future electron-positron colliders
Name: ilc-conformal-tracking
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/ConformalTracking
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-marlin-trk-devel
BuildRequires: root
BuildRequires: ilc-root-aida-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/ConformalTracking/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
This package is suitable for running pattern recognition based on conformal mapping and cellular automaton.
This is not tied to a given geometry, but has been developed for the CLIC detector model 2015.

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
      -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
      -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.1.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\${MARLIN_DLL:+\${MARLIN_DLL}:}%{_libdir}/libConformalTracking.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-conformal-tracking.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libConformalTracking.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-conformal-tracking.csh

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Fri Jul 05 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.12.1-1
* New version of Conformal tracking
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.12.0-1
- New version of Conformal tracking
* Fri Nov 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.11.0-1
- Fork for MuonColliderSoft

* Mon Aug 24 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.10.0-1
- Repackaging for CentOS 8


