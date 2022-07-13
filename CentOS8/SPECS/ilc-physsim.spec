%global _pver 0.4.2
%global _tagver v00-04-02

%global _maindir %{_builddir}/%{name}-%{version}

Summary: Matrix element package
Name: ilc-physsim
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/Physsim
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
BuildRequires: make
BuildRequires: chrpath
BuildRequires: ilc-utils-devel
BuildRequires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes

%description
Matrix element package.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/Physsim %{_maindir}
cd %{_maindir}
git checkout %{_tagver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_maindir}/build
cd %{_maindir}/build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
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
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.pcm

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.4.2-1
- New version of Physsim
* Thu Aug 27 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 0.4.1-1
- Repackaging for CentOS 8

