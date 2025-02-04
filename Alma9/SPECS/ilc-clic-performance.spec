%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 2.5.1
%global _tagver 02-05-01-MC

%global _sbuilddir %{_builddir}/%{name}-%{version}/CLICPerformance-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

Summary: Processors and configurations to determine the performance of the CLIC detector model
Name: ilc-clic-performance
Version: %{_pver}
Release: 1.exper%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/CLICPerformance
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: boost-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-marlin-trk-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: ilc-root-aida-devel
BuildRequires: root
BuildRequires: gsl-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/CLICPerformance/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Processors and configurations to determine the performance of the CLIC detector model.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
sed -i -e '/CMAKE_INSTALL_PREFIX/d' %{_sbuilddir}/CMakeLists.txt
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DINSTALL_DOC=OFF \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\${MARLIN_DLL:+\${MARLIN_DLL}:}%{_libdir}/libClicPerformance.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-clic-performance.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libClicPerformance.so\n" \
       | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-clic-performance.csh

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Wed Jan 15 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.5.1-1
- Forked version for MuonCollider
* Wed Jan 31 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.5.0-1
- New version of CLICPerformance
* Mon Mar 29 2021 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.4.1-1
- Repackaging for CentOS 8

