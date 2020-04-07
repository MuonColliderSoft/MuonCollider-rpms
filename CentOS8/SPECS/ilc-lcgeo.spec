%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global _boostp boost169

Summary: Implementation of Linear Collider detector models in DD4hep.
Name: ilc-lcgeo
Version: 0.16.5
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/MuonColliderSoft/lcgeo
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: aida-dd4hep-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source0: %{name}-%{version}.tar.gz

%description
Implementation of Linear Collider detector models in DD4hep.

%prep
%setup -c
sed -i -e 's|VERSION 3.12|VERSION 3.11|g' %{_builddir}/%{name}-%{version}/CMakeLists.txt
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=14 \
             -DBUILD_TESTING=OFF \
             -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
             -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/thislcgeo.sh
%{_libdir}/*.so
%{_libdir}/*.components

%changelog
* Fri Apr 03 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.16.5-1
- Repackaging for CentOS 8

