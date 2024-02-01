%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.34.0
%global _tagver 01-34

%global _sbuilddir %{_builddir}/%{name}-%{version}/MarlinReco-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global _boostp boost

Summary: Assembly of various Marlin processor for reconstruction
Name: ilc-marlin-reco
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinReco
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: root
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-marlin-kinfit-devel
BuildRequires: ilc-marlin-trk-devel
BuildRequires: gsl-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: ilc-root-aida-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/MarlinReco/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Assembly of various Marlin processor for reconstruction.

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
      -DMARLINRECO_FORTRAN=OFF \
      -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
      -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\${MARLIN_DLL:+\${MARLIN_DLL}:}%{_libdir}/libMarlinReco.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-reco.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMarlinReco.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-reco.csh

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Wed Jan 31 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.34.0-1
- New version of MarlinReco
* Mon Jan 23 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.33.1-1
- New version of MarlinReco
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.33.0-1
- New version of MarlinReco
* Fri Oct 02 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.28.0-1
- New version of MarlinReco
* Mon Jul 13 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.27.0-1
- Repackaging for CentOS 8

