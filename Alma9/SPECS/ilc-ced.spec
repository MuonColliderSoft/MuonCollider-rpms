%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.9.4
%global _tagver 01-09-04

%global _sbuilddir %{_builddir}/%{name}-%{version}/CED-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_ced_dir %{_libdir}/cmake/CED

Summary: Application for OpenGL drawing
Name: ilc-ced
Version: %{_pver}
Release: 1%{?dist}
License: GPLv3 License
Vendor: CERN
URL: https://github.com/iLCSoft/CED
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: freeglut-devel
BuildRequires: ilc-utils-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/CED/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
CED is a server client application for OpenGL drawing

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/usr \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -Wno-dev \
      %{_sbuilddir}
make %{?_smp_mflags}

%install
cd %{_cbuilddir}
make install
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_ced_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{_libdir}/cmake/*.cmake %{buildroot}%{cmake_ced_dir}
sed -i -e 's|%{buildroot}/usr|/usr|g' \
       -e 's|lib/cmake|lib64/cmake/CED|g' \
       %{buildroot}%{cmake_ced_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.1.9.4
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/*

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_bindir}/glced
%{_bindir}/test_ced
%{_bindir}/test_ced_mhits
%{_libdir}/*.so.*

%package devel
Summary: Application for OpenGL drawing
Requires: %{name}
Requires: freeglut-devel
Requires: ilc-utils-devel

%description devel
CED is a server client application for OpenGL drawing

%files devel
%defattr(-,root,root)
%dir %{cmake_ced_dir}
%{cmake_ced_dir}/*.cmake
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.9.4-1
- New version of CED
* Fri Mar 06 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.9.3-1
- Repackaging for CentOS 8


