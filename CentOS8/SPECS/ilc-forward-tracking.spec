%global _pver 1.14.1
%global _tagver v01-14-mucoll-01

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost169

Summary: Track Reconstruction for the Forward Direction (for the FTD)
Name: ilc-forward-tracking
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/ForwardTracking
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
BuildRequires: ilc-marlin-trk-devel
BuildRequires: ilc-kitrack-devel
BuildRequires: ilc-kitrack-marlin-devel
BuildRequires: root-aida-devel
BuildRequires: gsl-devel
BuildRequires: clhep-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Track Reconstruction for the Forward Direction (for the FTD)

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/MuonColliderSoft/ForwardTracking %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
sed -i -e '/ILCTEST_INCLUDE_DIRS/d' \
       -e '/simple_circle/d' \
       %{_maindir}/CMakeLists.txt
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
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libForwardTracking.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-forward-tracking.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libForwardTracking.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-forward-tracking.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.14.1-1
- Repackaging for CentOS 8

