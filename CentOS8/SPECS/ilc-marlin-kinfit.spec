%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_marlkin_dir %{_libdir}/cmake/MarlinKinfit

Summary: Kinematic fitting library for MarlinKinfit
Name: ilc-marlin-kinfit
Version: 0.6.0
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinKinfit
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: root
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: gsl-devel
BuildRequires: root-aida-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
Kinematic fitting library for MarlinKinfit.

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
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

mkdir -p %{buildroot}%{_includedir}/MarlinKinfit
mv %{buildroot}/usr/include/*.h %{buildroot}%{_includedir}/MarlinKinfit

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_marlkin_dir}

mv %{buildroot}/usr/*.cmake \
   %{buildroot}%{_libdir}/cmake/*.cmake \
   %{buildroot}%{cmake_marlkin_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|/include|/include/MarlinKinfit|g' \
       -e 's|lib/cmake|lib64/cmake/MarlinKinfit|g' \
    %{buildroot}%{cmake_marlkin_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libMarlinKinfit.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-kinfit.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libMarlinKinfit.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-marlin-kinfit.csh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so

%package devel
Summary: Kinematic fitting library for MarlinKinfit (development files)
Requires: %{name}
Requires: root
Requires: ilc-utils-devel
Requires: ilc-marlin-devel
Requires: gsl-devel
Requires: root-aida-devel

%description devel
Kinematic fitting library for MarlinKinfit.

%files devel
%defattr(-,root,root)
%dir %{cmake_marlkin_dir}
%{cmake_marlkin_dir}/*.cmake
%dir %{_includedir}/MarlinKinfit
%{_includedir}/MarlinKinfit/*.h

%changelog
* Mon Jul 13 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.6.0-1
- Repackaging for CentOS 8


