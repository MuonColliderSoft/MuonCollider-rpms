%global _pver 1.33.0
%global _tagver v01-33

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost

Summary: Assembly of various Marlin processor for reconstruction
Name: ilc-marlin-reco
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinReco
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: root
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-marlin-kinfit-devel
BuildRequires: ilc-marlin-trk-devel
BuildRequires: gsl-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: root-aida-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Assembly of various Marlin processor for reconstruction.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/MarlinReco %{_maindir}
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
      -DMARLINRECO_FORTRAN=OFF \
      -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
      -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libMarlinReco.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-reco.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMarlinReco.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-reco.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.33.0-1
- New version of MarlinReco
* Fri Oct 02 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.28.0-1
- New version of MarlinReco
* Mon Jul 13 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.27.0-1
- Repackaging for CentOS 8

