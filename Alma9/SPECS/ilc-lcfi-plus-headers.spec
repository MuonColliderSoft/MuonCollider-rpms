%global _pver 0.10.1
%global _tagver v00-10-01

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost

Summary: Flavor tagging code for ILC detectors (header files)
Name: ilc-lcfi-plus-headers
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/lcfiplus/LCFIPlus
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Flavor tagging code for ILC detectors (header files).

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/lcfiplus/LCFIPlus %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
echo "Nothing to build"

%install
mkdir -p %{buildroot}%{_prefix}/include/lcfiplus
cp %{_maindir}/include/*.h %{buildroot}%{_prefix}/include/lcfiplus

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_prefix}/include/lcfiplus
%{_prefix}/include/lcfiplus/*.h

%changelog
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.10.0-1
- Repackaging for CentOS 8

