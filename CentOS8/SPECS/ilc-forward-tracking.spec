%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global _boostp boost169

Summary: Track Reconstruction for the Forward Direction (for the FTD)
Name: ilc-forward-tracking
Version: 1.14.0
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/ForwardTracking.git
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-marlin-trk-devel
BuildRequires: ilc-kitrack-devel
BuildRequires: ilc-kitrack-marlin-devel
BuildRequires: root-aida-devel
BuildRequires: gsl-devel
BuildRequires: clhep-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
Track Reconstruction for the Forward Direction (for the FTD)

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
sed -i -e '/ILCTEST_INCLUDE_DIRS/d' \
       -e '/simple_circle/d' \
       %{_builddir}/%{name}-%{version}/CMakeLists.txt
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
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libForwardTracking.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-forward-tracking.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libForwardTracking.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-forward-tracking.csh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Tue Aug 25 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.14.0-1
- Repackaging for CentOS 8

