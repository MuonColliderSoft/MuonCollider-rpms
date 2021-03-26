%if %{?rhel}%{!?rhel:0} >= 8
%global _cmakecmd cmake
%global _cmakepkg cmake
%else
%global _cmakecmd cmake3
%global _cmakepkg cmake3
%endif

%global _pypkg python2

%global _boostp boost169
%global _cedv_datadir %{_datadir}/ilc-ced-viewer

Summary: CEDViewer processor for the CED event display
Name: ilc-ced-viewer
Version: 1.17.1
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/CEDViewer.git
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: %{_cmakepkg}
BuildRequires: make
BuildRequires: chrpath
BuildRequires: %{_boostp}-devel
BuildRequires: ilc-utils-devel
BuildRequires: ilc-marlin-devel
BuildRequires: ilc-marlin-util-devel
BuildRequires: root
BuildRequires: aida-dd4hep-devel
Requires: %{_pypkg}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source: %{mc_source_url}/%{name}-%{version}.tar.gz
%else
Source: %{name}-%{version}.tar.gz
%endif

%description
CEDViewer processor for the CED event display.

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
             -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
             -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
             -Wno-dev \
             %{_builddir}/%{name}-%{version}
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install

sed -i -e 's|bin/python|usr/bin/python2|g' \
       -e 's|sys.path\[0\]|"%{_cedv_datadir}"|g' \
       %{buildroot}%{_bindir}/ced2go

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
chrpath --replace %{_libdir} %{buildroot}%{_libdir}/*.so.%{version}
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/extractdetector
mkdir -p %{buildroot}%{_cedv_datadir}
mv %{buildroot}/usr/bin/*.xml %{buildroot}%{_cedv_datadir}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
printf "export MARLIN_DLL=\$MARLIN_DLL:%{_libdir}/libCEDViewer.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-ced-viewer.sh
printf "setenv MARLIN_DLL \$MARLIN_DLL:%{_libdir}/libCEDViewer.so\n" | tee %{buildroot}%{_sysconfdir}/profile.d/ilc-ced-viewer.csh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_cedv_datadir}
%{_sysconfdir}/profile.d/*
%{_bindir}/extractdetector
%{_bindir}/ced2go
%{_libdir}/*.so*
%{_cedv_datadir}/*.xml

%changelog
* Mon Aug 24 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.17.1-1
- Repackaging for CentOS 8


