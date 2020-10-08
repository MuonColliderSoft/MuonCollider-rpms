%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_aidatt_dir %{_libdir}/cmake/aidaTT
%global _boostp boost169

Summary: Tracking Toolkit from the AIDA project
Name: aida-tracking-toolkit
Version: 0.10.0
Release: 1%{?dist}
License: GPLv3 License
Vendor: INFN
URL: https://github.com/AIDASoft/aidaTT
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: gbl-devel
BuildRequires: aida-dd4hep
BuildRequires: ilc-lcio-devel
BuildRequires: eigen3-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
Tracking Toolkit from the AIDA project.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=14 \
             -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
             -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
             -Dstreamlog_DIR=%{_libdir}/cmake/ilcutil/ \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_aidatt_dir}
mv %{buildroot}%{_prefix}/aidaTTConfig.cmake %{buildroot}%{cmake_aidatt_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|/lib |/lib64 |g' \
    %{buildroot}%{cmake_aidatt_dir}/aidaTTConfig.cmake

%clean
rm -rf %{buildroot}

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

