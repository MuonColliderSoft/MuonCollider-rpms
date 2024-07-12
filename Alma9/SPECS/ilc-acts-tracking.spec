# workaround QA_SKIP_BUILD_ROOT=1
%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.2.2
%global _tagver 01-02-02-MC

%global _sbuilddir %{_builddir}/%{name}-%{version}/ACTSTracking-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

Summary: Marlin processor for running track reconstructions using the ACTS library
Name: ilc-acts-tracking
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/ACTSTracking
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: acts-toolkit-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/ACTSTracking/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Marlin processor for running track reconstructions using the ACTS library

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

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\${MARLIN_DLL:+\${MARLIN_DLL}:}%{_libdir}/libACTSTracking.so
export ACTS_MatFile=%{_datadir}/ACTSTracking/data/material-maps.json
export ACTS_TGeoFile=%{_datadir}/ACTSTracking/data/MuColl_v1.root\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libACTSTracking.so
setenv ACTS_MatFile %{_datadir}/ACTSTracking/data/material-maps.json
setenv ACTS_TGeoFile %{_datadir}/ACTSTracking/data/MuColl_v1.root\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/%{name}.csh

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so
%dir %{_datadir}/ACTSTracking
%dir %{_datadir}/ACTSTracking/data
%{_datadir}/ACTSTracking/data/*
%dir %{_datadir}/ACTSTracking/example
%{_datadir}/ACTSTracking/example/*

%package devel
Summary: Marlin processor for track reconstructions using the ACTS library (header files).
Requires: %{name}

%description devel
Marlin processor for track reconstructions using the ACTS library (header files).

%files devel
%defattr(-,root,root)
%dir %{_includedir}/ACTSTracking
%{_includedir}/ACTSTracking/*.hxx

%changelog
* Fri Jul 12 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.2.2-1
- New release of ACTS Tracking processor
* Wed Jan 25 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.1.0-1
- New release of ACTS Tracking processor
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.0.0-1
- Repackaging for CentOS 8


