%global _pver 0.5.3
%global _tagver v00-05-03

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost173

Summary: Interface between Marlin and FastJet
Name: ilc-marlin-fastjet
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinFastJet
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-fastjet-contrib-devel
BuildRequires: %{_boostp}-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Interface between Marlin and FastJet.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/MarlinFastJet %{_maindir}
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
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libMarlinFastJet.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-fastjet.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMarlinFastJet.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-fastjet.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.5.3-1
- New version of Marlin FastJet
* Tue Jun 16 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.5.2-1
- Repackaging for CentOS 8

