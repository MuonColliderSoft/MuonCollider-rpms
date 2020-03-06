Summary: Sequential recombination jet algorithms
Name: ilc-fastjet
Version: 3.2.1
Release: 1%{?dist}
License: GPLv2 License
URL: http://fastjet.fr/
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: make
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz

%description
The FastJet package provides a fast implementation of several
longitudinally invariant sequential recombination jet algorithms, in
particular the longitudinally invariant kt jet algorithm, the
inclusive longitudinally invariant version of the Cambridge/Aachen
jet-algorithm, and the inclusive anti-kt algorithm.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir %{_builddir}/%{name}-%{version}/build
cd %{_builddir}/%{name}-%{version}/build
%{_builddir}/%{name}-%{version}/configure \
    --prefix=%{buildroot}/usr \
    --enable-auto-ptr=no --enable-shared
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}-%{version}/build
make install
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
sed -i -e 's|%{buildroot}/usr|/usr|g' %{buildroot}%{_bindir}/fastjet-config
sed -i -e 's|%{buildroot}/usr/lib|%{_libdir}|g' %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%package devel
Summary: Sequential recombination jet algorithms (development files)

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
%dir /usr/include/fastjet
%dir /usr/include/fastjet/internal
%dir /usr/include/fastjet/tools
%dir /usr/include/siscone
%dir /usr/include/siscone/spherical
/usr/include/fastjet/*.h
/usr/include/fastjet/*.hh
/usr/include/fastjet/internal/*.hh
/usr/include/fastjet/tools/*.hh
/usr/include/siscone/*.h
/usr/include/siscone/spherical/*.h

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
* Fri Mar 06 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 3.2.1-1
- Repackaging for CentOS 8


