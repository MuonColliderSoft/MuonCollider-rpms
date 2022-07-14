%global _pver 2.4.1
%global _tagver v02-04-01

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost169

Summary: Processors and configurations to determine the performance of the CLIC detector model
Name: ilc-clic-performance
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/CLICPerformance
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
BuildRequires: aida-dd4hep-devel
BuildRequires: root-aida-devel
BuildRequires: root
BuildRequires: gsl-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Processors and configurations to determine the performance of the CLIC detector model.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/CLICPerformance %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
sed -i -e '/CMAKE_INSTALL_PREFIX/d' %{_maindir}/CMakeLists.txt
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
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libClicPerformance.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-clic-performance.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libClicPerformance.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-clic-performance.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Mon Mar 29 2021 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.4.1-1
- Repackaging for CentOS 8

