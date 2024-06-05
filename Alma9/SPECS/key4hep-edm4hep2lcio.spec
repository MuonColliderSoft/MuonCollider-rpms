%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.8.2
%global _tagver 00-08-02

%global _sbuilddir %{_builddir}/%{name}-%{version}/k4EDM4hep2LcioConv-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_edm2lcio_dir %{_libdir}/cmake/k4EDM4hep2LcioConv

Summary: Tools and libraries for the conversion between EDM4hep and LCIO.
Name: key4hep-edm4hep2lcio
Version: %{_pver}
Release: 1%{?dist}
License: Apache License 2.0
URL: https://github.com/key4hep/k4EDM4hep2LcioConv
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: ilc-lcio-devel
BuildRequires: edm4hep-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/key4hep/k4EDM4hep2LcioConv/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Tools and libraries for the conversion between EDM4hep and LCIO.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
sed -i '1i include_directories(${LCIO_INCLUDE_DIRS})' \
       %{_sbuilddir}/k4EDM4hep2LcioConv/CMakeLists.txt \
       %{_sbuilddir}/standalone/CMakeLists.txt
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_bindir}/lcio2edm4hep

%package devel
Summary: Tools and libraries for the conversion between EDM4hep and LCIO (development files).
Requires: %{name}
Requires: edm4hep-devel
Requires: ilc-lcio-devel

%description devel
Tools and libraries for the conversion between EDM4hep and LCIO.

%files devel
%defattr(-,root,root)
%dir %{cmake_edm2lcio_dir}
%{cmake_edm2lcio_dir}/*.cmake
%dir %{_includedir}/k4EDM4hep2LcioConv
%{_includedir}/k4EDM4hep2LcioConv/*.h
%{_includedir}/k4EDM4hep2LcioConv/*.ipp

%changelog
* Tue May 28 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.8.2-1
- Porting to AlmaLinux 9


