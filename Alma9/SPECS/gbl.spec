%global _pver 2.2.1
%global _tagver V02-02-01

%global _maindir %{_builddir}/%{name}-%{version}

%global cmake_gbl_dir %{_libdir}/cmake/GBL

Summary: General broken lines suite
Name: gbl
Version: %{_pver}
Release: 1%{?dist}
License: GPLv3 License
Vendor: INFN
URL: https://github.com/GeneralBrokenLines/GeneralBrokenLines
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: eigen3-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Track refitting with broken lines in 3D.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/GeneralBrokenLines/GeneralBrokenLines %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_maindir}/build
cd %{_maindir}/build
sed -i -e 's|Eigen3 REQUIRED|Eigen3 CONFIG REQUIRED|g' %{_maindir}/CMakeLists.txt
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DSUPPORT_ROOT=ON \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_gbl_dir}
mv %{buildroot}%{_prefix}/GBLConfig.cmake %{buildroot}%{cmake_gbl_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_gbl_dir}/GBLConfig.cmake
sed -i -e 's|PATH_SUFFIXES lib|PATH_SUFFIXES lib64|g' \
       -e 's|usr/lib |usr/lib64 |g' %{buildroot}%{cmake_gbl_dir}/GBLConfig.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/GBLpp

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_bindir}/GBLpp
%{_libdir}/*.so

%package devel
Summary: General broken lines suite (development files)
Requires: %{name}
Requires: eigen3-devel
Requires: root

%description devel
Track refitting with broken lines in 3D.

%files devel
%defattr(-,root,root)
%dir %{cmake_gbl_dir}
%{cmake_gbl_dir}/GBLConfig.cmake
%{_includedir}/*.h


%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.2.1-1
- New version of GBL
* Fri Jul 03 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.2.0-1
- Repackaging for CentOS 8


