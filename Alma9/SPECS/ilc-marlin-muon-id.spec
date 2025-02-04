%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.0.1
%global _tagver 00-00-01

%global _sbuilddir %{_builddir}/%{name}-%{version}/MarlinMuonID-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

Summary: Simple muon identification processor for Marlin
Name: ilc-marlin-muon-id
Version: %{_pver}
Release: 1.exper%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/MarlinMuonID
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/MarlinMuonID/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
This Marlin processor implements a simple muon identification algorithm,
matching tracks to hits in the outer muon detectors.

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
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\${MARLIN_DLL:+\${MARLIN_DLL}:}%{_libdir}/libMarlinMuonID.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-muon-id.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMarlinMuonID.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-muon-id.csh

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so

%changelog
* Wed Jan 15 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.0.1-1
- First release

