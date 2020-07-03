%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_gbl_dir %{_libdir}/cmake/GBL

Summary: General broken lines suite
Name: gbl
Version: 2.2.0
Release: 1%{?dist}
License: GPLv3 License
Vendor: INFN
URL: https://github.com/GeneralBrokenLines/GeneralBrokenLines
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: eigen3-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz

%description
Track refitting with broken lines in 3D.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
sed -i -e 's|Eigen3 REQUIRED|Eigen3 CONFIG REQUIRED|g' %{_builddir}/%{name}-%{version}/CMakeLists.txt
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=14 \
             -DSUPPORT_ROOT=ON \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
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
* Fri Jul 03 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.2.0-1
- Repackaging for CentOS 8


