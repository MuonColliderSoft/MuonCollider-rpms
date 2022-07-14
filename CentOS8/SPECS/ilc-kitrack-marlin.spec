%global _pver 1.13.1
%global _tagver v01-13-01

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost169

%global cmake_kitrmrl_dir %{_libdir}/cmake/KiTrackMarlin

Summary: KiTrack implementation classes for Marlin
Name: ilc-kitrack-marlin
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/KiTrackMarlin
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
BuildRequires: aida-dd4hep-devel
BuildRequires: gsl-devel
BuildRequires: clhep-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
KiTrack implementation classes for Marlin

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/KiTrackMarlin %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
sed -i -e '/ILCTEST_INCLUDE_DIRS/d' %{_maindir}/CMakeLists.txt
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
mkdir -p %{buildroot}%{cmake_kitrmrl_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{cmake_kitrmrl_dir}
mv %{buildroot}%{_libdir}/cmake/*.cmake %{buildroot}%{cmake_kitrmrl_dir}

sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|lib/cmake|lib64/cmake/KiTrackMarlin|g' \
       %{buildroot}%{cmake_kitrmrl_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Toolkit for tracking (development files)
Requires: %{name}
Requires: ilc-utils-devel
Requires: ilc-marlin-devel
Requires: ilc-marlin-util-devel
Requires: ilc-marlin-trk-devel
Requires: ilc-kitrack-devel
Requires: aida-dd4hep-devel
Requires: gsl-devel
Requires: clhep-devel
Requires: root

%description devel
The package consists of KiTrack (Cellular Automaton, a Hopfield Neural Network, the hit
and track classes) and Criteria (the criteria classes)

%files devel
%defattr(-,root,root)
%dir %{cmake_kitrmrl_dir}
%{cmake_kitrmrl_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/ILDImpl
%dir %{_includedir}/Tools
%{_includedir}/ILDImpl/*.h
%{_includedir}/Tools/*.h

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.13.1-1
- New version of KiTrack for Marlin
* Tue Aug 25 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.10.0-1
- Repackaging for CentOS 8







