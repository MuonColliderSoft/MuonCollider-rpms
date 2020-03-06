Summary: 3rd-party add-ons for FastJet
Name: ilc-fastjet-contrib-devel
Version: 1.025
Release: 1%{?dist}
License: GPLv2 License
URL: http://fastjet.hepforge.org/contrib/
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: make
BuildRequires: ilc-fastjet-devel
# see https://docs.fedoraproject.org/en-US/packaging-guidelines/#_packaging_static_libraries
Provides: ilc-fastjet-contrib-static = %{version}-%{release}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: ilc-fastjet-contrib.%{version}.tar.gz

%description
3rd-party add-ons for FastJet

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
cd %{_builddir}/%{name}-%{version}
./configure --fastjet-config=%{_bindir}/fastjet-config --prefix=%{buildroot}/usr
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}
make install
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.a
%dir /usr/include/fastjet/contrib
/usr/include/fastjet/contrib/*.hh

%changelog
* Fri Mar 06 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.025-1
- Repackaging for CentOS 8


