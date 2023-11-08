%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.5.3
%global _tagver 00-05-03

%global _sbuilddir %{_builddir}/%{name}-%{version}/MarlinFastJet-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global _boostp boost

Summary: Interface between Marlin and FastJet
Name: ilc-marlin-fastjet
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinFastJet
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-marlin-devel
BuildRequires: fastjet-contrib-devel
BuildRequires: %{_boostp}-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/MarlinFastJet/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Interface between Marlin and FastJet.

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
printf "export MARLIN_DLL=\${MARLIN_DLL:+\${MARLIN_DLL}:}%{_libdir}/libMarlinFastJet.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-fastjet.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMarlinFastJet.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-fastjet.csh

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.5.3-1
- New version of Marlin FastJet
* Tue Jun 16 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.5.2-1
- Repackaging for CentOS 8

