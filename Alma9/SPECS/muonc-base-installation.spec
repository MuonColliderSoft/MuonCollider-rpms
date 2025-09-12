%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 2.9.1
%global _tagver 02-09-01

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
Requires: ilc-marlin-acts
Requires: ilc-lcio-tools
Requires: muonc-tracker-digitizer
Requires: ilc-marlin-muon-id
Requires: python3-k4marlin-wrapper
Requires: python3-k4reco
Requires: python3-edm4hep
Requires: python3-k4GaudiPandora
Requires: python3-k4actstracking
Requires: gaudi-tools
Requires: gaudi-devel
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
mkdir -p %{buildroot}%{_datadir}/%{name}/examples
cp -R %{_sbuilddir}/Tests/marlin %{buildroot}%{_datadir}/%{name}/examples

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/examples/marlin
%dir %{_datadir}/%{name}/examples/marlin/config-files
%dir %{_datadir}/%{name}/examples/marlin/config-files/PandoraSettings
%{_datadir}/%{name}/examples/marlin/*.xml
%{_datadir}/%{name}/examples/marlin/*.py
%{_datadir}/%{name}/examples/marlin/config-files/*.xml
%{_datadir}/%{name}/examples/marlin/config-files/PandoraSettings/*.xml

%changelog
* Fri Aug 29 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.9.1-1
- New examples
* Mon Aug 04 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.8.1-1
- New version
* Thu Apr 27 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.8.0-1
- First release of the base installation



