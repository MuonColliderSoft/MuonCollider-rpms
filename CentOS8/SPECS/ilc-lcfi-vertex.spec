%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global _boostp boost169

%global cmake_lcfivtx_dir %{_libdir}/cmake/LCFIVertex

Summary: Package for vertex finding
Name: ilc-lcfi-vertex
Version: 0.8.0
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/LCFIVertex
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-lcio-devel
BuildRequires: root-aida-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
Package for vertex finding as well as vertex charge determination in b- and c-jets.

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
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install
rm -rf %{_builddir}/%{_prefix}/include/src \
       %{_builddir}/%{_prefix}/include/algo/src \
       %{_builddir}/%{_prefix}/include/nnet/src \
       %{_builddir}/%{_prefix}/include/util/src \
       %{_builddir}/%{_prefix}/include/zvtop/src
       

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_lcfivtx_dir}

mv %{buildroot}/usr/*.cmake %{buildroot}%{cmake_lcfivtx_dir}
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{cmake_lcfivtx_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libLCFIVertexProcessors.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-lcfi-vertex.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libLCFIVertexProcessors.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-lcfi-vertex.csh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so

%package devel
Summary: Package for vertex finding (development files)
Requires: %{name}
Requires: %{_boostp}-devel
Requires: root
Requires: ilc-utils-devel
Requires: ilc-marlin-devel
Requires: ilc-marlin-util-devel
Requires: ilc-lcio-devel
Requires: root-aida-devel

%description devel
Package for vertex finding as well as vertex charge determination in b- and c-jets.

%files devel
%defattr(-,root,root)
%dir %{cmake_lcfivtx_dir}
%{cmake_lcfivtx_dir}/*.cmake
%dir %{_includedir}/vertex_lcfi
%dir %{_includedir}/vertex_lcfi/algo
%dir %{_includedir}/vertex_lcfi/algo/inc
%dir %{_includedir}/vertex_lcfi/inc
%dir %{_includedir}/vertex_lcfi/nnet
%dir %{_includedir}/vertex_lcfi/nnet/inc
%dir %{_includedir}/vertex_lcfi/util
%dir %{_includedir}/vertex_lcfi/util/inc
%dir %{_includedir}/vertex_lcfi/zvtop
%dir %{_includedir}/vertex_lcfi/zvtop/include
%{_includedir}/vertex_lcfi/algo/inc/*.h
%{_includedir}/vertex_lcfi/inc/*.h
%{_includedir}/vertex_lcfi/nnet/inc/*.h
%{_includedir}/vertex_lcfi/util/inc/*.h
%{_includedir}/vertex_lcfi/zvtop/include/*.h

%changelog
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.8.0-1
- Repackaging for CentOS 8

