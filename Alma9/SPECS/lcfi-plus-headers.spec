%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.10.1
%global _tagver 00-10-01

%global _sbuilddir %{_builddir}/%{name}-%{version}/LCFIPlus-%{_tagver}

%global _boostp boost

Summary: Flavor tagging code for ILC detectors (header files)
Name: lcfi-plus-headers
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/lcfiplus/LCFIPlus
Group: Development/Libraries
BuildArch: %{_arch}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/lcfiplus/LCFIPlus/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Flavor tagging code for ILC detectors (header files).

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
echo "Nothing to build"

%install
mkdir -p %{buildroot}%{_prefix}/include/lcfiplus
cp %{_sbuilddir}/include/*.h %{buildroot}%{_prefix}/include/lcfiplus

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%dir %{_prefix}/include/lcfiplus
%{_prefix}/include/lcfiplus/*.h

%changelog
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.10.0-1
- Repackaging for CentOS 8

