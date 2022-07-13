%global _pver 0.10.0
%global _tagver v00-10

%global _maindir %{_builddir}/%{name}-%{version}

%global cmake_aidatt_dir %{_libdir}/cmake/aidaTT
%global _boostp boost169

Summary: Tracking Toolkit from the AIDA project
Name: aida-tracking-toolkit
Version: %{_pver}
Release: 1%{?dist}
License: GPLv3 License
Vendor: INFN
URL: https://github.com/AIDASoft/aidaTT
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: gbl-devel
BuildRequires: aida-dd4hep
BuildRequires: ilc-lcio-devel
BuildRequires: eigen3-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Tracking Toolkit from the AIDA project.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/AIDASoft/aidaTT %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_maindir}/build
cd %{_maindir}/build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
      -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
      -Dstreamlog_DIR=%{_libdir}/cmake/ilcutil/ \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install

mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_aidatt_dir}
mv %{buildroot}%{_prefix}/aidaTTConfig.cmake %{buildroot}%{cmake_aidatt_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|/lib |/lib64 |g' \
    %{buildroot}%{cmake_aidatt_dir}/aidaTTConfig.cmake

%clean
rm -rf %{buildroot}
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Tracking Toolkit from the AIDA project (development files)
Requires: %{name}
Requires: ilc-utils-devel
Requires: gbl-devel
Requires: aida-dd4hep
Requires: ilc-lcio-devel
Requires: eigen3-devel

%description devel
Tracking Toolkit from the AIDA project.

%files devel
%defattr(-,root,root)
%dir %{cmake_aidatt_dir}
%{cmake_aidatt_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/aidaTT
%{_includedir}/aidaTT/*.hh

%changelog
* Fri Jul 03 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.10.0-1
- Repackaging for CentOS 8

