Summary: Application for OpenGL drawing
Name: ilc-ced
Version: 1.9.3
Release: 1%{?dist}
License: GPLv3 License
Vendor: CERN
URL: https://github.com/iLCSoft/CED.git
Group: Development/Libraries
BuildArch: %{_arch}
%if %{?rhel}%{!?rhel:0} >= 8
BuildRequires: cmake
%else
BuildRequires: cmake3
%endif
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
%cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/usr \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCMAKE_CXX_STANDARD=14 \
       -Wno-dev \
       %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/cmake/%{name}-%{version}
mv %{buildroot}/usr/*.cmake %{buildroot}%{_libdir}/cmake/*.cmake %{buildroot}%{_libdir}/cmake/%{name}-%{version}
sed -i -e 's|%{buildroot}/usr|/usr|g' %{buildroot}%{_libdir}/cmake/%{name}-%{version}/*.cmake
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
%dir %{_libdir}/cmake/%{name}-%{version}
%{_libdir}/cmake/%{name}-%{version}/*.cmake
%{_libdir}/*.so
/usr/include/*.h

%changelog
* Fri Mar 06 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.9.3-1
- Repackaging for CentOS 8


