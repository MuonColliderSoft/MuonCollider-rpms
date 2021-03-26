%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global _boostp boost169

%global cmake_marlutil_dir %{_libdir}/cmake/MarlinUtil

Summary: Classes and functions used by Marlin processors
Name: ilc-marlin-util
Version: 1.15.1
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinUtil
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-ced-devel
BuildRequires: gsl-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: %{_boostp}-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
This library that containes classes and functions that are used by
more than one processor.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=17 \
             -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
             -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_marlutil_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{cmake_marlutil_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_marlutil_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Classes and functions used by Marlin processors (development files)
Requires: %{name}
Requires: ilc-marlin-devel
Requires: ilc-ced-devel
Requires: gsl-devel
Requires: aida-dd4hep-devel
Requires: %{_boostp}-devel

%description devel
This library that containes classes and functions that are used by
more than one processor.

%files devel
%defattr(-,root,root)
%dir %{cmake_marlutil_dir}
%{cmake_marlutil_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/marlinutil
%dir %{_includedir}/marlinutil/ANN
%dir %{_includedir}/marlinutil/mille
%{_includedir}/marlinutil/*.h
%{_includedir}/marlinutil/ANN/*.h
%{_includedir}/marlinutil/mille/*.h

%changelog
* Mon Jun 15 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.15.1-1
- Repackaging for CentOS 8


