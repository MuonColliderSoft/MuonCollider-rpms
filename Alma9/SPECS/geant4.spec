# Conditional parameters
# see https://rpm.org/user_doc/conditional_builds.html
%bcond_with g4mt
%bcond_with OpenGL
%bcond_with Qt5

%if %{with g4mt}
%global _g4mtopt ON
%else
%global _g4mtopt OFF
%endif

%if %{with OpenGL}
%global _glopt ON
%else
%global _glopt OFF
%endif

%if %{with Qt5}
%global _qtopt ON
%else
%global _qtopt OFF
%endif

Summary: GEometry ANd Tracking framework
Name: geant4
Version: 10.6.3
Release: 1.muonc%{?dist}
License: Geant4 Software License
Vendor: INFN
URL: http://geant4.web.cern.ch/
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: zlib-devel
BuildRequires: expat-devel
BuildRequires: xerces-c-devel
BuildRequires: clhep-devel
%if %{with Qt5}
BuildRequires: qt5-devel
%endif
%if %{with OpenGL}
BuildRequires: libX11-devel
BuildRequires: libXmu-devel
%endif
Requires: python3
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%undefine _disable_source_fetch
Source0: https://nexus.pd.infn.it/artifacts/repository/geant-sources/%{name}-%{version}.tar.gz
Source1: geant4-dataset-download.in
Source2: geant4-setup.sh.in
Source3: geant4-setup.csh.in

%description
Geant4 is a toolkit for the simulation of the passage of particles
through matter. Its areas of application include high energy, nuclear
and accelerator physics, as well as studies in medical and space
science. The two main reference papers for Geant4 are published in
Nuclear Instruments and Methods in Physics Research A 506 (2003)
250-303, and IEEE Transactions on Nuclear Science 53 No. 1 (2006)
270-278.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DGEANT4_INSTALL_EXAMPLES=OFF \
      -DGEANT4_USE_GDML=ON \
      -DGEANT4_BUILD_MULTITHREADED=%{_g4mtopt} \
      -DGEANT4_BUILD_TLS_MODEL=global-dynamic \
      -DGEANT4_USE_SYSTEM_ZLIB=ON \
      -DGEANT4_USE_SYSTEM_EXPAT=ON \
      -DGEANT4_USE_SYSTEM_CLHEP=ON \
      -DGEANT4_USE_OPENGL_X11=%{_glopt} \
      -DGEANT4_USE_QT=%{_qtopt} \
      %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|Geant4_INCLUDE_DIR .* ABSOLUTE|Geant4_INCLUDE_DIR "%{_includedir}/Geant4" ABSOLUTE|g' \
       %{buildroot}%{_libdir}/Geant4-%{version}/Geant4Config.cmake
sed -i 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{_bindir}/*-config \
                                         %{buildroot}%{_bindir}/*.sh \
                                         %{buildroot}%{_bindir}/*.csh
mkdir -p %{buildroot}%{_sbindir}
cp %{SOURCE1} %{buildroot}%{_sbindir}/geant4-dataset-download
sed -i -e 's|@PYTHON@|python3|g' -e 's|@VERSION@|%{version}|g' %{buildroot}%{_sbindir}/geant4-dataset-download
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/geant4-setup.sh
sed -i -e 's|@VERSION@|%{version}|g' %{buildroot}%{_sysconfdir}/profile.d/geant4-setup.sh
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/profile.d/geant4-setup.csh
sed -i -e 's|@VERSION@|%{version}|g' %{buildroot}%{_sysconfdir}/profile.d/geant4-setup.csh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/geant4-setup.*
%{_bindir}/*
%attr(0740,root,root) %{_sbindir}/geant4-dataset-download
%{_libdir}/*.so

%package devel
Summary: GEometry ANd Tracking framework, development files
Requires: %{name}
Requires: expat-devel
Requires: zlib-devel
Requires: xerces-c-devel
Requires: clhep-devel
%if %{with Qt5}
Requires: qt5-devel
%endif
%if %{with X11}
Requires: libX11-devel
Requires: libXmu-devel
%endif

%description devel
Geant4 is a toolkit for the simulation of the passage of particles
through matter. Its areas of application include high energy, nuclear
and accelerator physics, as well as studies in medical and space
science. The two main reference papers for Geant4 are published in
Nuclear Instruments and Methods in Physics Research A 506 (2003)
250-303, and IEEE Transactions on Nuclear Science 53 No. 1 (2006)
270-278.

%files devel
%defattr(-,root,root)
%dir %{_libdir}/Geant4-%{version}
%dir %{_libdir}/Geant4-%{version}/Modules
%{_libdir}/Geant4-%{version}/*.cmake
%{_libdir}/Geant4-%{version}/Linux-g++
%{_libdir}/Geant4-%{version}/Modules/*.cmake
%dir %{_includedir}/Geant4
%dir %{_includedir}/Geant4/tools
%dir %{_includedir}/Geant4/tools/glutess
%dir %{_includedir}/Geant4/tools/hdf5
%dir %{_includedir}/Geant4/tools/histo
%dir %{_includedir}/Geant4/tools/io
%dir %{_includedir}/Geant4/tools/lina
%dir %{_includedir}/Geant4/tools/mpi
%dir %{_includedir}/Geant4/tools/rroot
%dir %{_includedir}/Geant4/tools/sg
%dir %{_includedir}/Geant4/tools/store
%dir %{_includedir}/Geant4/tools/waxml
%dir %{_includedir}/Geant4/tools/wroot
%dir %{_includedir}/Geant4/tools/xml
%dir %{_includedir}/Geant4/tools/zb
%{_includedir}/Geant4/*.h
%{_includedir}/Geant4/*.hh
%{_includedir}/Geant4/*.hpp
%{_includedir}/Geant4/*.icc
%{_includedir}/Geant4/tools/*
%{_includedir}/Geant4/tools/glutess/*
%{_includedir}/Geant4/tools/hdf5/*
%{_includedir}/Geant4/tools/histo/*
%{_includedir}/Geant4/tools/io/*
%{_includedir}/Geant4/tools/lina/*
%{_includedir}/Geant4/tools/mpi/*
%{_includedir}/Geant4/tools/rroot/*
%{_includedir}/Geant4/tools/sg/*
%{_includedir}/Geant4/tools/store/*
%{_includedir}/Geant4/tools/waxml/*
%{_includedir}/Geant4/tools/wroot/*
%{_includedir}/Geant4/tools/xml/*
%{_includedir}/Geant4/tools/zb/*
%dir %{_datadir}/Geant4-%{version}
%dir %{_datadir}/Geant4-%{version}/geant4make
%dir %{_datadir}/Geant4-%{version}/geant4make/config
%dir %{_datadir}/Geant4-%{version}/geant4make/config/sys
%{_datadir}/Geant4-%{version}/tools.license
%{_datadir}/Geant4-%{version}/geant4make/*
%{_datadir}/Geant4-%{version}/geant4make/config/*
%{_datadir}/Geant4-%{version}/geant4make/config/sys/*


%changelog
* Wed Nov 25 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 10.6.3-1
- Packaged patch 3

* Mon Feb 17 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 10.6.1-1
- Repackaging for CentOS 8

* Thu Jan 30 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 10.5.1-1
- Repackaging for CentOS 7

* Tue Dec 04 2018 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 10.4.2-1
- Repackaging for CentOS 7


