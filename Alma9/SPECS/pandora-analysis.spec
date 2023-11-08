%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 2.0.1
%global _tagver 02-00-01

%global _sbuilddir %{_builddir}/%{name}-%{version}/LCPandoraAnalysis-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

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
Source0: https://github.com/PandoraPFA/LCPandoraAnalysis/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Pandora calibration and analysis tools for the Marlin framework.

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
      -DINSTALL_DOC=OFF \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\${MARLIN_DLL:+\${MARLIN_DLL}:}%{_libdir}/libPandoraAnalysis.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/pandora-analysis.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libPandoraAnalysis.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/pandora-analysis.csh

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_bindir}/*
%{_libdir}/*.so*

%changelog
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.0.1-1
- Repackaging for CentOS 8

