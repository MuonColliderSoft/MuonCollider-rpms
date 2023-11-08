%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.6.2
%global _tagver 00-06-02

%global _sbuilddir %{_builddir}/%{name}-%{version}/MarlinDD4hep-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global _boostp boost

Summary: Marlin processor for DD4hep detector geometry
Name: ilc-marlin-dd4hep
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinDD4hep
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/MarlinDD4hep/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Marlin processor to initialize a DD4hep detector geometry
from a compact file for a Marlin job.

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
       -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
      -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\${MARLIN_DLL:+\${MARLIN_DLL}:}%{_libdir}/libMarlinDD4hep.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-dd4hep.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMarlinDD4hep.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-dd4hep.csh

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.6.1-1
- New version of Marlin DD4hep
* Fri Jul 10 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.6.0-1
- Repackaging for CentOS 8


