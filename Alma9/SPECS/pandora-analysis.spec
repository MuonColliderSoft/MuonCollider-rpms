%global _pver 2.0.1
%global _tagver v02-00-01

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost

Summary: Pandora calibration and analysis tools for the Marlin framework
Name: pandora-analysis
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/PandoraPFA/LCPandoraAnalysis
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-lcio-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Pandora calibration and analysis tools for the Marlin framework.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/PandoraPFA/LCPandoraAnalysis %{_maindir}
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
      -DINSTALL_DOC=OFF \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libPandoraAnalysis.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/pandora-analysis.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libPandoraAnalysis.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/pandora-analysis.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_bindir}/*
%{_libdir}/*.so*

%changelog
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.0.1-1
- Repackaging for CentOS 8

