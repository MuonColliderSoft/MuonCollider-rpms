%global debug_package %{nil}
# see https://docs.fedoraproject.org/en-US/packaging-guidelines/#_packaging_static_libraries
%undefine _disable_source_fetch

%global _pver 1.50.0
%global _tagver 1.050

%global _maindir %{_builddir}/fjcontrib-%{_tagver}

Summary: 3rd-party add-ons for FastJet
Name: fastjet-contrib
Version: %{_pver}
Release: 1%{?dist}
License: GPLv2 License
URL: http://fastjet.hepforge.org/contrib/
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: make
BuildRequires: fastjet-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: http://fastjet.hepforge.org/contrib/downloads/fjcontrib-%{_tagver}.tar.gz

%description
3rd-party add-ons for FastJet.

%prep
%setup -n fjcontrib-%{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
cd %{_maindir}
./configure --fastjet-config=%{_bindir}/fastjet-config --prefix=%{buildroot}%{_prefix}

%install
cd %{_maindir}
make %{?_smp_mflags} fragile-shared-install
mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}/libfastjetcontribfragile.so.%{version}
ln -s %{_libdir}/libfastjetcontribfragile.so.%{version} %{buildroot}%{_libdir}/libfastjetcontribfragile.so.1
ln -s %{_libdir}/libfastjetcontribfragile.so.%{version} %{buildroot}%{_libdir}/libfastjetcontribfragile.so
make %{?_smp_mflags} install
rm -rf %{buildroot}%{_prefix}/lib

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: 3rd-party add-ons for FastJet (development files)
Requires: %{name}
Requires: fastjet-devel
Provides: libfastjetcontribfragile.so()(64bit)

%description devel
3rd-party add-ons for FastJet.

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%dir %{_includedir}/fastjet/contrib
%{_includedir}/fastjet/contrib/*.hh

%changelog
* Mon Jan 23 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.50.0-1
- New version of FastJet contribution
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.49.0-1
- New version of FastJet contribution
* Mon Jun 15 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.44-1
- Repackaging for CentOS 8


