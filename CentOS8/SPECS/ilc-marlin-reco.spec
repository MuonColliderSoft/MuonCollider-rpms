%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global _boostp boost169

Summary: Assembly of various Marlin processor for reconstruction
Name: ilc-marlin-reco
Version: 1.27.0
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/MarlinReco
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: root
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: ilc-marlin-kinfit-devel
BuildRequires: ilc-marlin-trk-devel
BuildRequires: gsl-devel
BuildRequires: aida-dd4hep-devel
BuildRequires: root-aida-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz

%description
Assembly of various Marlin processor for reconstruction.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_cmakecmd} -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
             -DCMAKE_BUILD_TYPE=RelWithDebInfo \
             -DCMAKE_CXX_STANDARD=14 \
             -DMARLINRECO_FORTRAN=OFF \
             -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
             -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so*

%changelog
* Mon Jul 13 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.27.0-1
- Repackaging for CentOS 8

