%global _pver 0.13.0
%global _tagver v00-13-MC

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost173

Summary: Interface between Marlin and PandoraPFA
Name: ilc-ddmarlin-pandora
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/DDMarlinPandora
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-trk-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: pandora-pfa-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Interface between Marlin and PandoraPFA.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/MuonColliderSoft/DDMarlinPandora %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_maindir}/build
cd %{_maindir}/build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
      -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.0.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libDDMarlinPandora.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-ddmarlin-pandora.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libDDMarlinPandora.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-ddmarlin-pandora.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so

%package devel
Summary: Interface between Marlin and PandoraPFA files)
Requires: %{name}
Requires: root
Requires: %{_boostp}-devel
Requires: aida-dd4hep-devel
Requires: ilc-utils-devel
Requires: ilc-marlin-devel
Requires: ilc-marlin-trk-devel
Requires: ilc-marlin-util-devel
Requires: pandora-pfa-devel

%description devel
Interface between Marlin and PandoraPFA.

%files devel
%defattr(-,root,root)
%dir %{_includedir}
%{_includedir}/*.h

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.13.0-1
- New version of Marlin Pandora PFA
* Wed Dec 16 2020 Alessio Gianelle <gianelle@pd.infn.it> - 0.12.0-1
- New processor DDCaloDigi_BIB
* Mon Jul 13 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.11.0-1
- Repackaging for CentOS 8


