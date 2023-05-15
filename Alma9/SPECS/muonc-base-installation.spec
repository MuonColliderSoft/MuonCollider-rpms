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
Requires: ilc-lcio-tools
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
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -R %{_sbuilddir}/SoftCheck %{buildroot}%{_datadir}/%{name}
sed -i -e 's|opt/ilcsoft/muonc/detector-simulation/geometries|usr/share/muonc-detector-geometry|g' \
       %{buildroot}%{_datadir}/%{name}/SoftCheck/ced2go_steering.xml \
       %{buildroot}%{_datadir}/%{name}/SoftCheck/confile/InitDD4hep.xml \
       %{buildroot}%{_datadir}/%{name}/SoftCheck/sim_steer.py
sed -i -e 's|opt/ilcsoft/muonc/ACTSTracking/v1.1.0|usr/share/ACTSTracking|g' \
       %{buildroot}%{_datadir}/%{name}/SoftCheck/confile/Tracking.xml

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/SoftCheck
%dir %{_datadir}/%{name}/SoftCheck/confile
%dir %{_datadir}/%{name}/SoftCheck/confile/PandoraSettings
%{_datadir}/%{name}/SoftCheck/*.xml
%{_datadir}/%{name}/SoftCheck/*.py
%{_datadir}/%{name}/SoftCheck/confile/*.xml
%{_datadir}/%{name}/SoftCheck/confile/PandoraSettings/*.xml

%changelog
* Thu Apr 27 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.8.0-1
- First release of the base installation



