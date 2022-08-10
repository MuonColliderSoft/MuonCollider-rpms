%global _pver 1.0.3
%global _tagver v01-00-03

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost173

Summary: Reconstruction for the forward calorimeters of future colliders
Name: ilc-fcal-clusterer
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/FCALSW/FCalClusterer
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-lcio-devel
BuildRequires: ilc-gear-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: root
BuildRequires: root-minuit2
BuildRequires: root-unuran
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Reconstruction for the forward calorimeters of future colliders.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/FCALSW/FCalClusterer %{_maindir}
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
      -DBUILD_TESTING=OFF \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/*

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libFCalClusterer.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-fcal-clusterer.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libFCalClusterer.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-fcal-clusterer.csh

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_bindir}/*
%{_libdir}/*.so

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.0.3-1
- New version of FCal clusterer
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.0.1-1
- Repackaging for CentOS 8

