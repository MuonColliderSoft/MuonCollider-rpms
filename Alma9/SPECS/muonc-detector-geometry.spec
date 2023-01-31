%global _pver 1.3.0
%global _taglabel 01-03-MC
%global _tagver v%{_taglabel}

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

%description
The Muon Collider detector geometry.

%prep
cd %{_builddir}
wget -O %{_tagver}.tar.gz https://github.com/MuonColliderSoft/detector-simulation/archive/refs/tags/%{_tagver}.tar.gz
tar zxf %{_tagver}.tar.gz
rm -f %{_tagver}.tar.gz
mv detector-simulation-%{_taglabel} %{name}-%{version}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
echo "Nothing to compile"

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -R  %{_builddir}/%{name}-%{version}/geometries/MuColl_v1 %{buildroot}%{_datadir}/%{name}
rm %{buildroot}%{_datadir}/%{name}/MuColl_v1/*.md %{buildroot}%{_datadir}/%{name}/MuColl_v1/.DS_Store

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

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


