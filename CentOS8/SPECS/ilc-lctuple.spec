%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

Summary: Marlin package that creates a ROOT TTree with a column wise ntuple from LCIO collections
Name: ilc-lctuple
Version: 1.13.0
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/LCTuple
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
Marlin package that creates a ROOT TTree with a column wise ntuple from LCIO collections.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=17 \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.1.12.0

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libLCTuple.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-lctuple.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libLCTuple.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-lctuple.csh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so

%changelog
* Fri Dec 04 2020 Alessio Gianelle <gianelle@pd.infn.it> - 1.13.0-1
- Added track hits to the tracks branches
- Fixed the index assignment to the track hits
* Mon Sep 21 2020 Alessio Gianelle <gianelle@pd.infn.it> - 1.12.2-1
- Add branches for the time of the hits
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.12.1-1
- Repackaging for CentOS 8

