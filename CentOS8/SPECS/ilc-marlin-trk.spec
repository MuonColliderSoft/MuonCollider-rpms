%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global _boostp boost169
%global cmake_martrk_dir %{_libdir}/cmake/MarlinTrk

Summary: Tracking Package for Marlin
Name: ilc-marlin-trk
Version: 2.8.0
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinTrk
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: root
BuildRequires: ilc-utils-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-gear-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-kaltest-devel
BuildRequires: ilc-kaldet-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: aida-tracking-toolkit-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
Tracking Package based on LCIO and GEAR, primarily aimed at providing
track fitting in Marlin.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=14 \
             -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
             -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_martrk_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{cmake_martrk_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_martrk_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so*

%package devel
Summary: Tracking Package for Marlin (development files)
Requires: %{name}
Requires: root
Requires: ilc-utils-devel
Requires: ilc-lcio-devel
Requires: ilc-gear-devel
Requires: ilc-marlin-devel
Requires: ilc-marlin-util-devel
Requires: ilc-kaltest-devel
Requires: ilc-kaldet-devel
Requires: aida-dd4hep-devel
Requires: aida-tracking-toolkit-devel

%description devel
Tracking Package based on LCIO and GEAR, primarily aimed at providing
track fitting in Marlin.

%files devel
%defattr(-,root,root)
%dir %{cmake_martrk_dir}
%{cmake_martrk_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/MarlinTrk
%{_includedir}/MarlinTrk/*.h

%changelog
* Mon Jul 13 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.8.0-1
- Repackaging for CentOS 8


