# %global debug_package %{nil}
# see https://docs.fedoraproject.org/en-US/packaging-guidelines/#_packaging_static_libraries

Summary: 3rd-party add-ons for FastJet
Name: ilc-fastjet-contrib
Version: 1.44
Release: 1%{?dist}
License: GPLv2 License
URL: http://fastjet.hepforge.org/contrib/
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: make
BuildRequires: ilc-fastjet-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: ilc-fastjet-contrib-%{version}.tar.gz

%description
3rd-party add-ons for FastJet.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
cd %{_builddir}/%{name}-%{version}
./configure --fastjet-config=%{_bindir}/fastjet-config --prefix=%{buildroot}%{_prefix}

%install
cd %{_builddir}/%{name}-%{version}
make fragile-shared-install
mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}/libfastjetcontribfragile.so.%{version}
ln -s %{_libdir}/libfastjetcontribfragile.so.%{version} %{buildroot}%{_libdir}/libfastjetcontribfragile.so.1
ln -s %{_libdir}/libfastjetcontribfragile.so.%{version} %{buildroot}%{_libdir}/libfastjetcontribfragile.so
make install
rm -rf %{buildroot}%{_prefix}/lib

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: 3rd-party add-ons for FastJet (development files)
Requires: %{name}
Requires: ilc-fastjet-devel

%description devel
3rd-party add-ons for FastJet.

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%dir %{_includedir}/fastjet/contrib
%{_includedir}/fastjet/contrib/*.hh

%changelog
* Mon Jun 15 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.44-1
- Repackaging for CentOS 8


