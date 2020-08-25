%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global _boostp boost169

%global cmake_kitrmrl_dir %{_libdir}/cmake/KiTrackMarlin

Summary: KiTrack implementation classes for Marlin
Name: ilc-kitrack-marlin
Version: 1.13.0
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/KiTrackMarlin.git
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
BuildRequires: aida-dd4hep-devel
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
KiTrack implementation classes for Marlin

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
sed -i -e '/ILCTEST_INCLUDE_DIRS/d' %{_builddir}/%{name}-%{version}/CMakeLists.txt
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
mkdir -p %{buildroot}%{cmake_kitrmrl_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{cmake_kitrmrl_dir}
mv %{buildroot}%{_libdir}/cmake/*.cmake %{buildroot}%{cmake_kitrmrl_dir}

sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|lib/cmake|lib64/cmake/KiTrackMarlin|g' \
       %{buildroot}%{cmake_kitrmrl_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

%clean
rm -rf %{buildroot}

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
* Tue Aug 25 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.10.0-1
- Repackaging for CentOS 8







