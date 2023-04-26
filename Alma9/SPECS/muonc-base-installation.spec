%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 2.8.0
%global _tagver 02-08-MC

%global _sbuilddir %{_builddir}/%{name}-%{version}/MuonCutil-%{_tagver}

Summary: Base installation for the Muon Collider framework
Name: muonc-base-installation
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/MuonCutil
Group: Development/Libraries
BuildArch: noarch
Requires: python3-dd4hep
Requires: muonc-detector-geometry
Requires: ilc-marlin-dd4hep
Requires: ilc-marlin-fastjet
Requires: ilc-marlin-kinfit-processors
Requires: ilc-overlay
Requires: lcfi-plus
Requires: ilc-conformal-tracking
Requires: ilc-marlin-reco
Requires: ilc-forward-tracking
Requires: ilc-marlin-trk-processors
Requires: ilc-ced-viewer
Requires: ilc-ddmarlin-pandora
Requires: ilc-lctuple
Requires: ilc-clic-performance
Requires: ilc-acts-tracking
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/MuonCutil/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Base installation for the Muon Collider framework.

%prep
%setup -c

%build
echo "Nothing to compile"

%install
mkdir -p %{buildroot}%{_datadir}/%{name}/tests
cp -R %{_sbuilddir}/SoftCheck %{buildroot}%{_datadir}/%{name}/tests

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/tests
%dir %{_datadir}/%{name}/tests/SoftCheck
%dir %{_datadir}/%{name}/tests/SoftCheck/confile
%dir %{_datadir}/%{name}/tests/SoftCheck/PandoraSettings
%{_datadir}/%{name}/tests/SoftCheck/*.xml
%{_datadir}/%{name}/tests/SoftCheck/*.py
%{_datadir}/%{name}/tests/SoftCheck/confile/*.xml
%{_datadir}/%{name}/tests/SoftCheck/PandoraSettings/*.xml

%changelog
* Fri Feb 03 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.8.0-1
- First release of the base installation



