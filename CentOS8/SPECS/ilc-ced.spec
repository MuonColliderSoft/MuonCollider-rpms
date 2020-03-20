%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global cmake_ced_dir %{_libdir}/cmake/%{name}-%{version}

Summary: Application for OpenGL drawing
Name: ilc-ced
Version: 1.9.3
Release: 1%{?dist}
License: GPLv3 License
Vendor: CERN
URL: https://github.com/iLCSoft/CED.git
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: chrpath
BuildRequires: freeglut-devel
BuildRequires: ilc-utils-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz

%description
CED is a server client application for OpenGL drawing

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}/usr \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=14 \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{cmake_ced_dir}
mv %{buildroot}/usr/*.cmake %{buildroot}%{_libdir}/cmake/*.cmake %{buildroot}%{cmake_ced_dir}
sed -i -e 's|%{buildroot}/usr|/usr|g' %{buildroot}%{cmake_ced_dir}/*.cmake
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.1.9.3
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/glced
%{_bindir}/test_ced
%{_bindir}/test_ced_mhits
%{_libdir}/*.so.*

%package devel
Summary: Application for OpenGL drawing
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
* Fri Mar 06 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.9.3-1
- Repackaging for CentOS 8


