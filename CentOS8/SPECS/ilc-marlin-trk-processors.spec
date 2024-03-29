%global _pver 2.13.0
%global _tagver v02-13-MC

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost173

Summary: A collection of tracking related processors based on MarlinTrk
Name: ilc-marlin-trk-processors
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/MarlinTrkProcessors
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-marlin-trk-devel
BuildRequires: ilc-kitrack-devel
BuildRequires: ilc-kitrack-marlin-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
A collection of tracking related processors based on MarlinTrk.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/MuonColliderSoft/MarlinTrkProcessors %{_maindir}
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
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libMarlinTrkProcessors.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-trk-processors.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMarlinTrkProcessors.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-trk-processors.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.13.0-1
- New version of MarlinTrk processor
* Fri Nov 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.12.0-1
- Fork for MuonColliderSoft

