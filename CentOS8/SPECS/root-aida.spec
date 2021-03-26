%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_aida_dir %{_libdir}/cmake/AIDA
%global cmake_raida_dir %{_libdir}/cmake/RAIDA


Summary: ROOT implementation of AIDA
Name: root-aida
Version: 1.9.0
Release: 1%{?dist}
License: GPLv3 License
Vendor: INFN
URL: https://github.com/iLCSoft/RAIDA.git
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: root
BuildRequires: ilc-utils-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
The motivation for the development of RAIDA was to offer the possibility to create
and fill n-tuple or histograms using standard ROOT objects with AIDA. All ROOT objects
created with AIDA are stored in a ROOT file. Since our main application of RAIDA is to
create ROOT output to be analysed using the ROOT program, the current version can not
read in the root files created. Furthermore only objects, which exist within ROOT can
be created.

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
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_aida_dir}
mkdir -p %{buildroot}%{cmake_raida_dir}
mv %{buildroot}%{_libdir}/cmake/*.cmake %{buildroot}%{cmake_raida_dir}
mv %{buildroot}/usr/RAIDA*.cmake %{buildroot}%{cmake_raida_dir}
mv %{buildroot}/usr/AIDA*.cmake %{buildroot}%{cmake_aida_dir}

sed -i -e 's|%{buildroot}/usr|%{cmake_raida_dir}|g' %{buildroot}%{cmake_aida_dir}/AIDAConfig.cmake
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|lib/cmake|lib64/cmake/RAIDA|g' \
       %{buildroot}%{cmake_raida_dir}/RAIDAConfig.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: ROOT implementation of AIDA (development files)
Requires: %{name}
Requires: root

%description devel
The motivation for the development of RAIDA was to offer the possibility to create
and fill n-tuple or histograms using standard ROOT objects with AIDA. All ROOT objects
created with AIDA are stored in a ROOT file. Since our main application of RAIDA is to
create ROOT output to be analysed using the ROOT program, the current version can not
read in the root files created. Furthermore only objects, which exist within ROOT can
be created.

%files devel
%defattr(-,root,root)
%{_bindir}/*
%dir %{cmake_aida_dir}
%dir %{cmake_raida_dir}
%{cmake_aida_dir}/*.cmake
%{cmake_raida_dir}/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/AIDA
%dir %{_includedir}/RAIDA
%{_includedir}/AIDA/*h
%{_includedir}/RAIDA/*.h

%changelog
* Mon Jun 08 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.9.0-1
- Repackaging for CentOS 8


