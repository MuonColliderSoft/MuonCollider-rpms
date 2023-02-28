%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.24.0
%global _tagver 00-24-MC

%global _sbuilddir %{_builddir}/%{name}-%{version}/Overlay-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

Summary: Event overlay with Marlin
Name: ilc-overlay
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/Overlay
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: boost-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-root-aida-devel
BuildRequires: clhep-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/Overlay/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
The Overlay processor can be used to overlay background events
from an additonal set of LCIO files in a Marlin job.

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
      -DBOOST_INCLUDEDIR=%{_includedir}/boost \
      -DBOOST_LIBRARYDIR=%{_libdir}/boost  \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.0.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libOverlay.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-overlay.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libOverlay.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-overlay.csh

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Tue Feb 28 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.24.0-1
- New version of Overlay
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.23.0-1
- New version of Overlay
* Mon Sep 21 2020 Nazar Bartosik <nazar.bartosik@cern.ch> - 0.22.2-1
- Added support for lower/upper integration time boundaries in OverlayTimingGeneric
- OverlayTimingGeneric: Added option to make integration times symmetric
- OverlayTiming: Skipping merging of collections that have no integration times configured
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.22.1-1
- Repackaging for CentOS 8


