%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 3.1.0
%global _tagver 03-01

%global _sbuilddir %{_builddir}/%{name}-%{version}/Garlic-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global _boostp boost

Summary: Marlin Processor that identifies photons and electrons
Name: ilc-garlic
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/Garlic
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: root
BuildRequires: root-tmva
BuildRequires: ilc-utils-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/Garlic/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Marlin Processor that identifies photons and electrons.

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
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libGarlic.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-garlic.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libGarlic.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-garlic.csh

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so*

%changelog
* Mon Jul 13 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 3.1.0-1
- Repackaging for CentOS 8


