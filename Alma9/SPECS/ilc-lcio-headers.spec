%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 2.20.2
%global _tagver 02-20-02-RC1

%global _sbuilddir %{_builddir}/%{name}-%{version}/LCIO-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

Summary: Event data model and persistency for Linear Collider detector (header files)
Name: ilc-lcio-headers
Version: %{_pver}
Release: 1%{?dist}
License: BSD v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/LCIO
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: root
Requires: root
Requires: zlib-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/MuonColliderSoft/LCIO/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
LCIO (Linear Collider I/O) provides the event data model (EDM)
and persistency solution for Linear Collider detector R&D studies.

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
      -DBUILD_ROOTDICT=ON  \
      -Wno-dev \
      %{_sbuilddir}

%install
mkdir -p %{buildroot}%{_includedir}/lcio
cp -r %{_sbuilddir}/src/cpp/include/* %{buildroot}%{_includedir}/lcio
cp -r %{_sbuilddir}/sio/include/sio %{buildroot}%{_includedir}
rm %{buildroot}%{_includedir}/lcio/DATA/README
ln -s %{_includedir}/lcio/pre-generated/EVENT %{buildroot}%{_includedir}/lcio/EVENT
ln -s %{_includedir}/lcio/pre-generated/IO %{buildroot}%{_includedir}/lcio/IO

%clean
rm -rf %{buildroot}
rm -rf %{SOURCE0}

%files
%defattr(-,root,root)
%dir %{_includedir}/lcio
%dir %{_includedir}/lcio/DATA
%dir %{_includedir}/lcio/IMPL
%dir %{_includedir}/lcio/IOIMPL
%dir %{_includedir}/lcio/MT
%dir %{_includedir}/lcio/UTIL
%dir %{_includedir}/lcio/rootDict
%dir %{_includedir}/lcio/SIO
%dir %{_includedir}/lcio/pre-generated
%dir %{_includedir}/lcio/pre-generated/EVENT
%dir %{_includedir}/lcio/pre-generated/IO
%dir %{_includedir}/sio
%dir %{_includedir}/sio/compression
%{_includedir}/lcio/*.h
%{_includedir}/lcio/DATA/*.h
%{_includedir}/lcio/IMPL/*.h
%{_includedir}/lcio/IOIMPL/*.h
%{_includedir}/lcio/MT/*.h
%{_includedir}/lcio/UTIL/*.h
%{_includedir}/lcio/UTIL/*.icc
%{_includedir}/lcio/UTIL/*.hh
%{_includedir}/lcio/rootDict/*.h
%{_includedir}/lcio/SIO/*.h
%{_includedir}/lcio/pre-generated/EVENT/*.h
%{_includedir}/lcio/pre-generated/IO/*.h
%{_includedir}/sio/*.h
%{_includedir}/sio/compression/*.h
%{_includedir}/lcio/EVENT
%{_includedir}/lcio/IO

%changelog
* Wed Jan 31 2024 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.20.2-1
- New version of LCIO
* Tue Feb 28 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.17.0-1
- New version of LCIO














