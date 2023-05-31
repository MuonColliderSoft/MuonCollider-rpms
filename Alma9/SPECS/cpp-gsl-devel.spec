%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 4.0.0
%global _tagver 4.0.0

%global _sbuilddir %{_builddir}/%{name}-%{version}/GSL-%{_tagver}
%global _gsldir /opt/GSL

Summary: Guidelines Support Library
Name: cpp-gsl-devel
Version: %{_pver}
Release: 1%{?dist}
License: MIT License
Vendor: Microsoft Corporation
URL: https://github.com/microsoft/GSL
Group: Development/Libraries
BuildArch: %{_arch}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/microsoft/GSL/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
The Guidelines Support Library (GSL) contains functions and types
that are suggested for use by the C++ Core Guidelines maintained
by the Standard C++ Foundation. 

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
echo "Nothing to build"

%install
mkdir -p %{buildroot}%{_gsldir}/include
cp -r %{_sbuilddir}/include/gsl %{buildroot}%{_gsldir}/include

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%dir %{_gsldir}
%dir %{_gsldir}/include
%dir %{_gsldir}/include/gsl
%{_gsldir}/include/gsl/*

%changelog
* Tue May 30 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 4.0.0-1
- Porting to AlmaLinux 9


