%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 0.2.0
%global _tagver 00-02

%global _sbuilddir %{_builddir}/%{name}-%{version}/SIO-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_sio_dir %{_libdir}/cmake/SIO

Summary: Persistency solution for storing SIO structures
Name: ilc-sio
Version: %{_pver}
Release: 1%{?dist}
License: BSD v.3
Vendor: INFN
URL: https://github.com/iLCSoft/SIO
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/SIO/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Persistency solution for reading and writing binary data in SIO structures

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DSIO_EXAMPLES=OFF \
      -DSIO_SET_RPATH=OFF \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install


%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%{_bindir}/sio-dump
%{_libdir}/*.so*

%package devel
Summary: Persistency solution for storing SIO structures (development files)
Requires: %{name}

%description devel
Persistency solution for reading and writing binary data
in SIO structures (development files)

%files devel
%defattr(-,root,root)
%dir %{cmake_sio_dir}
%{cmake_sio_dir}/*.cmake
%dir %{_includedir}/sio
%dir %{_includedir}/sio/compression
%{_includedir}/sio/*.h
%{_includedir}/sio/compression/*.h

%changelog
* Tue Jun 04 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.2.0-1
- First release for AlmaLinux9

