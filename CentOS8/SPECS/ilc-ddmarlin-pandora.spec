%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global _boostp boost169

Summary: Interface between Marlin and PandoraPFA
Name: ilc-ddmarlin-pandora
Version: 0.11.0
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/DDMarlinPandora
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
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
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
Interface between Marlin and PandoraPFA.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=17 \
             -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
             -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libDDMarlinPandora.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-ddmarlin-pandora.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libDDMarlinPandora.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-ddmarlin-pandora.csh

%clean
rm -rf %{buildroot}

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
* Mon Jul 13 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.11.0-1
- Repackaging for CentOS 8


