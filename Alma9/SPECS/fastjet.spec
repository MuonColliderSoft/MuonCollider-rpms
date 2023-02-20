%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 3.4.0

%global _maindir %{_builddir}/fastjet-%{_pver}

Summary: Sequential recombination jet algorithms
Name: fastjet
Version: %{_pver}
Release: 1%{?dist}
License: GPLv2 License
URL: http://fastjet.fr/
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: make
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: https://fastjet.fr/repo/fastjet-%{_pver}.tar.gz

%description
The FastJet package provides a fast implementation of several
longitudinally invariant sequential recombination jet algorithms, in
particular the longitudinally invariant kt jet algorithm, the
inclusive longitudinally invariant version of the Cambridge/Aachen
jet-algorithm, and the inclusive anti-kt algorithm.

%prep
%setup -n fastjet-%{_pver}
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_maindir}/build
cd %{_maindir}/build
%{_maindir}/configure \
    --prefix=%{buildroot}%{_prefix} \
    --libdir=%{buildroot}%{_libdir} \
    --enable-auto-ptr=no --enable-shared
make %{?_smp_mflags}

%install
cd %{_maindir}/build
make install
sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{_bindir}/fastjet-config
sed -i -e 's|%{buildroot}/usr/lib|%{_libdir}|g' %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Sequential recombination jet algorithms (development files)
Requires: %{name}

%description devel
The FastJet package provides a fast implementation of several
longitudinally invariant sequential recombination jet algorithms, in
particular the longitudinally invariant kt jet algorithm, the
inclusive longitudinally invariant version of the Cambridge/Aachen
jet-algorithm, and the inclusive anti-kt algorithm.

%files devel
%defattr(-,root,root)
%{_bindir}/fastjet-config
%{_libdir}/*.so
%dir %{_includedir}/fastjet
%dir %{_includedir}/fastjet/internal
%dir %{_includedir}/fastjet/tools
%dir %{_includedir}/siscone
%dir %{_includedir}/siscone/spherical
%{_includedir}/fastjet/*.h
%{_includedir}/fastjet/*.hh
%{_includedir}/fastjet/internal/*.hh
%{_includedir}/fastjet/tools/*.hh
%{_includedir}/siscone/*.h
%{_includedir}/siscone/spherical/*.h

%package static
Summary: Sequential recombination jet algorithms (static libraries)

%description static
The FastJet package provides a fast implementation of several
longitudinally invariant sequential recombination jet algorithms, in
particular the longitudinally invariant kt jet algorithm, the
inclusive longitudinally invariant version of the Cambridge/Aachen
jet-algorithm, and the inclusive anti-kt algorithm.

%files static
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la

%changelog
* Mon Jan 23 2023 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 3.4.0-1
- New release of FastJet
* Fri Mar 06 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 3.2.1-1
- Repackaging for CentOS 8


