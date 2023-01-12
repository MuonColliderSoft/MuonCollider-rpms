%global _pver 0.23.0
%global _tagver v00-23-MC

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost

Summary: Event overlay with Marlin
Name: ilc-overlay
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/Overlay
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: root-aida-devel
BuildRequires: clhep-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
The Overlay processor can be used to overlay background events
from an additonal set of LCIO files in a Marlin job.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/MuonColliderSoft/Overlay %{_maindir}
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
      -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
      -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.0.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libOverlay.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-overlay.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libOverlay.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-overlay.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.23.0-1
- New version of Overlay
* Mon Sep 21 2020 Nazar Bartosik <nazar.bartosik@cern.ch> - 0.22.2-1
- Added support for lower/upper integration time boundaries in OverlayTimingGeneric
- OverlayTimingGeneric: Added option to make integration times symmetric
- OverlayTiming: Skipping merging of collections that have no integration times configured
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.22.1-1
- Repackaging for CentOS 8


