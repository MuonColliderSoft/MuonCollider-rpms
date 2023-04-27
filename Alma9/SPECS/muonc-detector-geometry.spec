%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.4.0
%global _tagver 01-04-MC

%global _sbuilddir %{_builddir}/%{name}-%{version}/detector-simulation-%{_tagver}

Summary: The Muon Collider detector geometry
Name: muonc-detector-geometry
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/detector-simulator
Group: Development/Libraries
BuildArch: noarch
Requires: ilc-lcgeo
Source0: https://github.com/MuonColliderSoft/detector-simulation/archive/refs/tags/v%{_tagver}.tar.gz

%description
The Muon Collider detector geometry.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
echo "Nothing to compile"

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -R %{_sbuilddir}/geometries/MuColl_v1 %{buildroot}%{_datadir}/%{name}
cp -R %{_sbuilddir}/geometries/MuColl_v1.0.1 %{buildroot}%{_datadir}/%{name}
cp -R %{_sbuilddir}/geometries/MuColl_v1.1.1 %{buildroot}%{_datadir}/%{name}
cp -R %{_sbuilddir}/geometries/MuColl_v1.2.1 %{buildroot}%{_datadir}/%{name}
cp -R %{_sbuilddir}/geometries/MuColl_v1.3.1 %{buildroot}%{_datadir}/%{name}
rm %{buildroot}%{_datadir}/%{name}/MuColl_v1/*.md \
   %{buildroot}%{_datadir}/%{name}/MuColl_v1/.DS_Store \
   %{buildroot}%{_datadir}/%{name}/MuColl_v1.0.1/*.md \
   %{buildroot}%{_datadir}/%{name}/MuColl_v1.1.1/*.md \
   %{buildroot}%{_datadir}/%{name}/MuColl_v1.2.1/*.md \
   %{buildroot}%{_datadir}/%{name}/MuColl_v1.3.1/*.md

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/MuColl_v1
%{_datadir}/%{name}/MuColl_v1/*.xml
%dir %{_datadir}/%{name}/MuColl_v1.0.1
%dir %{_datadir}/%{name}/MuColl_v1.0.1/include
%{_datadir}/%{name}/MuColl_v1.0.1/*.xml
%{_datadir}/%{name}/MuColl_v1.0.1/include/*.xml
%dir %{_datadir}/%{name}/MuColl_v1.1.1
%dir %{_datadir}/%{name}/MuColl_v1.1.1/include
%{_datadir}/%{name}/MuColl_v1.1.1/*.xml
%{_datadir}/%{name}/MuColl_v1.1.1/include/*.xml
%dir %{_datadir}/%{name}/MuColl_v1.2.1
%dir %{_datadir}/%{name}/MuColl_v1.2.1/include
%{_datadir}/%{name}/MuColl_v1.2.1/*.xml
%{_datadir}/%{name}/MuColl_v1.2.1/include/*.xml
%dir %{_datadir}/%{name}/MuColl_v1.3.1
%dir %{_datadir}/%{name}/MuColl_v1.3.1/include
%{_datadir}/%{name}/MuColl_v1.3.1/*.xml
%{_datadir}/%{name}/MuColl_v1.3.1/include/*.xml

%changelog
* Tue Feb 28 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.4.0-1
- New version of the geometry
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.2.0-1
- New version of the geometry
* Wed Dec 09 2020 Nazar Bartosik <nazar.bartosik@cern.ch> - 1.1.0-1
- geometry with fixed endcap tracker support asymmetry
* Fri Nov 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.0.0-1
- First release of the detectory geometry


