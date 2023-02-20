%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.3.0
%global _tagver 01-03-MC

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
BuildRequires: wget
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
rm %{buildroot}%{_datadir}/%{name}/MuColl_v1/*.md %{buildroot}%{_datadir}/%{name}/MuColl_v1/.DS_Store

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/MuColl_v1
%{_datadir}/%{name}/MuColl_v1/*.xml

%changelog
* Tue Jan 31 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.3.0-1
- New version of the geometry
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.2.0-1
- New version of the geometry
* Wed Dec 09 2020 Nazar Bartosik <nazar.bartosik@cern.ch> - 1.1.0-1
- geometry with fixed endcap tracker support asymmetry
* Fri Nov 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.0.0-1
- First release of the detectory geometry


