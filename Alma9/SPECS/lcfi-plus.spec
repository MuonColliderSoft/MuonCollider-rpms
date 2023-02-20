%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.10.1
%global _tagver 00-10-01

%global _sbuilddir %{_builddir}/%{name}-%{version}/LCFIPlus-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global _boostp boost

Summary: Flavor tagging code for ILC detectors
Name: lcfi-plus
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/lcfiplus/LCFIPlus
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: lcfi-vertex-devel
BuildRequires: lcfi-plus-headers
BuildRequires: root
BuildRequires: root-smatrix
BuildRequires: root-minuit2
Requires: lcfi-plus-headers
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/lcfiplus/LCFIPlus/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Flavor tagging code for ILC detectors.

%prep
%setup -c
sed -i -e 's|${PROJECT_SOURCE_DIR}/include|/usr/include/lcfiplus|g' %{_sbuilddir}/CMakeLists.txt
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
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.0.*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libLCFIPlus.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/lcfi-plus.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libLCFIPlus.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/lcfi-plus.csh

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.pcm

%changelog
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.10.0-1
- Repackaging for CentOS 8

