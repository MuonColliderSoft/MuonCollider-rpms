%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.5.0
%global _tagver 00-05

%global _sbuilddir %{_builddir}/%{name}-%{version}/MarlinKinfitProcessors-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

Summary: Marlin Processors based on MarlinKinfit
Name: ilc-marlin-kinfit-processors
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinKinfitProcessors
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-kinfit-devel
BuildRequires: ilc-root-aida-devel
BuildRequires: clhep-devel
BuildRequires: gsl-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/MarlinKinfitProcessors/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Marlin Processors based on MarlinKinfit.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

# development files are not required
rm -rf %{buildroot}/usr/include %{buildroot}/usr/lib/cmake

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libMarlinKinfitProcessors.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-kinfit-processors.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMarlinKinfitProcessors.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-kinfit-processors.csh

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.5.0-1
- New version of Marlin Kinfit processors
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.4.2-1
- Repackaging for CentOS 8

