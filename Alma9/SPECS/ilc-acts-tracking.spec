# workaround QA_SKIP_BUILD_ROOT=1

%global _pver 1.1.0
%global _tagver v1.1.0

%global _maindir %{_builddir}/%{name}-%{version}

Summary: Marlin processor for running track reconstructions using the ACTS library
Name: ilc-acts-tracking
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/ACTSTracking
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: acts-toolkit-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Marlin processor for running track reconstructions using the ACTS library

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/MuonColliderSoft/ACTSTracking %{_maindir}
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

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libACTSTracking.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-acts-tracking.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libACTSTracking.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-acts-tracking.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so
%dir %{_datadir}/ACTSTracking
%dir %{_datadir}/ACTSTracking/data
%{_datadir}/ACTSTracking/data/*
%dir %{_datadir}/ACTSTracking/example
%{_datadir}/ACTSTracking/example/*

%changelog
* Wed Jan 25 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.1.0-1
- New release of ACTS Tracking processor
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.0.0-1
- Repackaging for CentOS 8


