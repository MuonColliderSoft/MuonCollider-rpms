%global _pver 1.10.0
%global _tagver v01-10

%global _maindir %{_builddir}/%{name}-%{version}

%global cmake_kitrack_dir %{_libdir}/cmake/KiTrack

Summary: Toolkit for tracking
Name: ilc-kitrack
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/KiTrack
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
The package consists of KiTrack (Cellular Automaton, a Hopfield Neural Network, the hit
and track classes) and Criteria (the criteria classes)

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/KiTrack %{_maindir}
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
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_kitrack_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{cmake_kitrack_dir}
mv %{buildroot}%{_libdir}/cmake/*.cmake %{buildroot}%{cmake_kitrack_dir}

sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|lib/cmake|lib64/cmake/KiTrack|g' \
       %{buildroot}%{cmake_kitrack_dir}/*.cmake
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
Requires: root

%description devel
The package consists of KiTrack (Cellular Automaton, a Hopfield Neural Network, the hit
and track classes) and Criteria (the criteria classes)

%files devel
%defattr(-,root,root)
%dir %{cmake_kitrack_dir}
%{cmake_kitrack_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/Criteria
%dir %{_includedir}/KiTrack
%{_includedir}/Criteria/*.h
%{_includedir}/KiTrack/*.h

%changelog
* Tue Aug 25 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.10.0-1
- Repackaging for CentOS 8







