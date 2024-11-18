%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 2.15.3
%global _tagver MuSICv2-pre01

%global _sbuilddir %{_builddir}/%{name}-%{version}/MarlinTrkProcessors-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

Summary: A collection of tracking related processors based on MarlinTrk
Name: ilc-marlin-trk-processors
Version: %{_pver}
Release: 1.exper%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/MarlinTrkProcessors
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: boost-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-marlin-trk-devel
BuildRequires: ilc-kitrack-devel
BuildRequires: ilc-kitrack-marlin-devel
BuildRequires: ilc-ddkaltest-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/MarlinTrkProcessors/archive/refs/tags/%{_tagver}.tar.gz
AutoReqProv: yes

%description
A collection of tracking related processors based on MarlinTrk.

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
printf "export MARLIN_DLL=\${MARLIN_DLL:+\${MARLIN_DLL}:}%{_libdir}/libMarlinTrkProcessors.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-trk-processors.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMarlinTrkProcessors.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-trk-processors.csh

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so

%changelog
* Wed Jul 10 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.15.2-1
- New version of MarlinTrk processor
* Wed Apr 26 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.15.0-1
- New version of MarlinTrk processor
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.13.0-1
- New version of MarlinTrk processor
* Fri Nov 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.12.0-1
- Fork for MuonColliderSoft

