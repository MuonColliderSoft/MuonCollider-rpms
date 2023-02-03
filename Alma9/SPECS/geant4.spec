%global debug_package %{nil}

# Conditional parameters
%bcond_with g4mt
%bcond_with OpenGL
#bcond_with Qt5

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

#if #{with Qt5}
#global _qtopt ON
#else
#global _qtopt OFF
#endif

#global _pver 10.6.3
#global _pname geant4.10.06.p03

%global _pver 11.1.0
%global _pname geant4-v11.1.0

%global _sbuilddir %{_builddir}/geant4/%{_pname}
%global _cbuilddir %{_builddir}/geant4/build


Summary: GEometry ANd Tracking framework
Name: geant4
Version: %{_pver}
Release: 1.muonc%{?dist}
License: Geant4 Software License
Vendor: INFN
URL: http://geant4.web.cern.ch/
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: pkgconf-pkg-config
BuildRequires: zlib-devel
BuildRequires: expat-devel
BuildRequires: xerces-c-devel
BuildRequires: clhep-devel
##if #{with Qt5}
#BuildRequires: qt5-devel
#endif
%if %{with OpenGL}
BuildRequires: libX11-devel
BuildRequires: libXmu-devel
%endif
Requires: python3
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%undefine _disable_source_fetch
Source0: http://cern.ch/geant4-data/releases/%{_pname}.tar.gz
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
%setup -c -n %{name}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
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
      %{_sbuilddir}
#      -DGEANT4_USE_QT=%{_qtopt} \
#      #{_sbuilddir}

make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

rm -f %{buildroot}%{_bindir}/*.sh %{buildroot}%{_bindir}/*.csh

sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' \
       -e 's|Geant4_INCLUDE_DIR .* ABSOLUTE|Geant4_INCLUDE_DIR "%{_includedir}/Geant4" ABSOLUTE|g' \
       %{buildroot}%{_libdir}/cmake/Geant4/Geant4Config.cmake

sed -i 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{_bindir}/geant4-config

sed -i 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{_libdir}/pkgconfig/*.pc

mkdir -p %{buildroot}%{_sbindir}
cp %{SOURCE1} %{buildroot}%{_sbindir}/geant4-dataset-download
sed -i -e 's|@VERSION@|%{version}|g' %{buildroot}%{_sbindir}/geant4-dataset-download
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/geant4-setup.sh
sed -i -e 's|@VERSION@|%{version}|g' %{buildroot}%{_sysconfdir}/profile.d/geant4-setup.sh
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/profile.d/geant4-setup.csh
sed -i -e 's|@VERSION@|%{version}|g' %{buildroot}%{_sysconfdir}/profile.d/geant4-setup.csh

mkdir -p %{buildroot}%{_datadir}/Geant4/data

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/geant4-setup.*
%{_bindir}/geant4-config
%attr(0740,root,root) %{_sbindir}/geant4-dataset-download
%{_libdir}/*.so*

%package devel
Summary: GEometry ANd Tracking framework, development files
Requires: %{name}
Requires: expat-devel
Requires: zlib-devel
Requires: xerces-c-devel
Requires: clhep-devel
#if #{with Qt5}
#Requires: qt5-devel
#endif
%if %{with OpenGL}
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
%{_libdir}/Geant4-%{version}/Linux-g++
%dir %{_libdir}/cmake/Geant4
%dir %{_libdir}/cmake/Geant4/Modules
%dir %{_libdir}/cmake/Geant4/PTL
%dir %{_libdir}/cmake/Geant4/PTL/Modules
%{_libdir}/cmake/Geant4/*.cmake
%{_libdir}/cmake/Geant4/Modules/*.cmake
%{_libdir}/cmake/Geant4/PTL/*.cmake
%{_libdir}/cmake/Geant4/PTL/Modules/*.cmake
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/Geant4
%dir %{_includedir}/Geant4/tools
%dir %{_includedir}/Geant4/tools/font
%dir %{_includedir}/Geant4/tools/glutess
%dir %{_includedir}/Geant4/tools/histo
%dir %{_includedir}/Geant4/tools/io
%dir %{_includedir}/Geant4/tools/lina
%dir %{_includedir}/Geant4/tools/offscreen
%dir %{_includedir}/Geant4/tools/rroot
%dir %{_includedir}/Geant4/tools/sg
%dir %{_includedir}/Geant4/tools/store
%dir %{_includedir}/Geant4/tools/waxml
%dir %{_includedir}/Geant4/tools/wroot
%dir %{_includedir}/Geant4/tools/xml
%dir %{_includedir}/Geant4/tools/zb
%dir %{_includedir}/Geant4/toolx
%dir %{_includedir}/Geant4/toolx
%dir %{_includedir}/Geant4/toolx/Qt
%dir %{_includedir}/Geant4/toolx/Windows
%dir %{_includedir}/Geant4/toolx/X11
%dir %{_includedir}/Geant4/toolx/Xt
%dir %{_includedir}/Geant4/toolx/hdf5
%dir %{_includedir}/Geant4/toolx/mpi
%dir %{_includedir}/Geant4/toolx/sg
%dir %{_includedir}/Geant4/toolx/xml
%dir %{_includedir}/Geant4/PTL
%{_includedir}/Geant4/*.h
%{_includedir}/Geant4/*.hh
%{_includedir}/Geant4/*.hpp
%{_includedir}/Geant4/*.icc
%{_includedir}/Geant4/*.in
%{_includedir}/Geant4/tools/*
%{_includedir}/Geant4/tools/font/*
%{_includedir}/Geant4/tools/glutess/*
%{_includedir}/Geant4/tools/histo/*
%{_includedir}/Geant4/tools/io/*
%{_includedir}/Geant4/tools/lina/*
%{_includedir}/Geant4/tools/offscreen/*
%{_includedir}/Geant4/tools/rroot/*
%{_includedir}/Geant4/tools/sg/*
%{_includedir}/Geant4/tools/store/*
%{_includedir}/Geant4/tools/waxml/*
%{_includedir}/Geant4/tools/wroot/*
%{_includedir}/Geant4/tools/xml/*
%{_includedir}/Geant4/tools/zb/*
%{_includedir}/Geant4/toolx/*
%{_includedir}/Geant4/toolx/Qt/*
%{_includedir}/Geant4/toolx/Windows/*
%{_includedir}/Geant4/toolx/X11/*
%{_includedir}/Geant4/toolx/Xt/*
%{_includedir}/Geant4/toolx/hdf5/*
%{_includedir}/Geant4/toolx/mpi/*
%{_includedir}/Geant4/toolx/sg/*
%{_includedir}/Geant4/toolx/xml/*
%{_includedir}/Geant4/PTL/*
%dir %{_datadir}/Geant4
%dir %{_datadir}/Geant4/data
%dir %{_datadir}/Geant4/fonts
%dir %{_datadir}/Geant4/geant4make
%dir %{_datadir}/Geant4/geant4make/config
%dir %{_datadir}/Geant4/geant4make/config/sys
%{_datadir}/Geant4/tools.license
%{_datadir}/Geant4/fonts/*
%{_datadir}/Geant4/geant4make/*
%{_datadir}/Geant4/geant4make/config/*
%{_datadir}/Geant4/geant4make/config/sys/*

%changelog
* Thu Feb 02 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 11.1.0-3
- Repackaging for Alma Linux 9

* Wed Nov 25 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 10.6.3-1
- Packaged patch 3

* Mon Feb 17 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 10.6.1-1
- Repackaging for CentOS 8

* Thu Jan 30 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 10.5.1-1
- Repackaging for CentOS 7

* Tue Dec 04 2018 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 10.4.2-1
- Repackaging for CentOS 7


