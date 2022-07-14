%global _pver 0.8.0
%global _tagver v00-08

%global _maindir %{_builddir}/%{name}-%{version}

%global _boostp boost169

%global cmake_lcfivtx_dir %{_libdir}/cmake/LCFIVertex

Summary: Package for vertex finding
Name: ilc-lcfi-vertex
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/LCFIVertex
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
BuildRequires: ilc-lcio-devel
BuildRequires: root-aida-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Package for vertex finding as well as vertex charge determination in b- and c-jets.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/LCFIVertex %{_maindir}
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
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
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
rm -rf %{_maindir}

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

