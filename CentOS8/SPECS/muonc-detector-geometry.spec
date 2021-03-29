Summary: The Muon Collider detector geometry
Name: muonc-detector-geometry
Version: 1.1.0
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/detector-simulator
Group: Development/Libraries
BuildArch: noarch
Requires: ilc-lcgeo

%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

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
cp -R  %{_builddir}/%{name}-%{version}/geometries/MuColl_v1 %{buildroot}%{_datadir}/%{name}
rm %{buildroot}%{_datadir}/%{name}/MuColl_v1/*.md %{buildroot}%{_datadir}/%{name}/MuColl_v1/.DS_Store

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/MuColl_v1
%{_datadir}/%{name}/MuColl_v1/*.xml

%changelog
* Wed Dec 09 2020 Nazar Bartosik <nazar.bartosik@cern.ch> - 1.1.0-1
- geometry with fixed endcap tracker support asymmetry
* Fri Nov 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.0.0-1
- First release of the detectory geometry


