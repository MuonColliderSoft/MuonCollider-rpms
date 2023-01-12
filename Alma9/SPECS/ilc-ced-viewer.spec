%global _pver 1.19.1
%global _tagver v01-19-01

%global _maindir %{_builddir}/%{name}-%{version}

%global _pypkg python2

%global _boostp boost
%global _cedv_datadir %{_datadir}/ilc-ced-viewer

Summary: CEDViewer processor for the CED event display
Name: ilc-ced-viewer
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/CEDViewer
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: git
BuildRequires: cmake
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

%description
CEDViewer processor for the CED event display.

%prep
[ -e %{_maindir} ] && rm -rf %{_maindir}
git clone https://github.com/iLCSoft/CEDViewer %{_maindir}
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
      -DBOOST_INCLUDEDIR=%{_includedir}/%{_boostp} \
      -DBOOST_LIBRARYDIR=%{_libdir}/%{_boostp}  \
      -Wno-dev \
      %{_maindir}
make %{?_smp_mflags}

%install
cd %{_maindir}/build
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
rm -rf %{_maindir}

%files
%defattr(-,root,root)
%dir %{_cedv_datadir}
%{_sysconfdir}/profile.d/*
%{_bindir}/extractdetector
%{_bindir}/ced2go
%{_libdir}/*.so*
%{_cedv_datadir}/*.xml

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.19.1-1
- New version of CED viewer
* Mon Aug 24 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.17.1-1
- Repackaging for CentOS 8


