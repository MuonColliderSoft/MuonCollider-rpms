%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

Summary: Matrix element package
Name: ilc-physsim
Version: 0.4.1
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/Physsim
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
Matrix element package.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=17 \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

# Development files are not required
rm -rf %{buildroot}%{_prefix}/include %{buildroot}%{_prefix}/lib/cmake

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libPhyssim.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-physsim.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libPhyssim.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-physsim.csh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.pcm

%changelog
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.4.1-1
- Repackaging for CentOS 8

