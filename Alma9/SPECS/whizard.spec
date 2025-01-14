%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 3.1.5
%global _tagver 3.1.5

%global _sbuilddir %{_builddir}/%{name}-%{version}/whizard-%{_tagver}
%global _cbuilddir %{_builddir}/%{name}-%{version}/build

%global cmake_acts_dir %{_libdir}/cmake/Acts
%global _boostp boost

Summary: Toolkit for calculation of multi-particle scattering cross sections
Name: whizard
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.2
Vendor: DESY
URL: https://whizard.hepforge.org/
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: make
BuildRequires: patch
BuildRequires: chrpath
BuildRequires: gcc-gfortran
BuildRequires: ocaml
BuildRequires: libtirpc-devel
BuildRequires: pythia8-devel
BuildRequires: lhapdf-devel
BuildRequires: yaml-cpp-devel
BuildRequires: HepMC-devel
BuildRequires: HepMC3-devel
BuildRequires: HepMC3-search-devel
BuildRequires: HepMC3-interfaces-devel
BuildRequires: python3-lhapdf
BuildRequires: ilc-lcio-devel
BuildRequires: fastjet-contrib-devel
BuildRequires: openmpi-devel
BuildRequires: mpich
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: http://whizard.hepforge.org/whizard-%{_tagver}.tar.gz
Patch0: whizard-lcio_setup.patch
AutoReqProv: yes

%description
Toolkit for efficient calculation of multi-particle scattering cross sections
and simulated event samples. 

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}
patch %{_sbuilddir}/configure %{PATCH0}

%build
mkdir %{_cbuilddir}
cd %{_cbuilddir}
PATH=$PATH:/usr/lib64/openmpi/bin \
%{_sbuilddir}/configure FC=mpifort CC=mpicc CXX=mpic++ \
    --prefix=%{buildroot}%{_prefix} \
    --libdir=%{buildroot}%{_libdir} \
    --enable-pythia8 \
    --disable-pythia6 \
    --enable-hepmc2 \
    --enable-lcio \
    --enable-fastjet \
    --enable-lhapdf \
    --enable-fc-mpi \
    --enable-fc-openmp
PATH=$PATH:/usr/lib64/openmpi/bin make %{?_smp_mflags}

%install
cd %{_cbuilddir}
PATH=$PATH:/usr/lib64/openmpi/bin make install

sed -i -e 's|%{buildroot}%{_prefix}|%{_prefix}|g' \
    %{buildroot}%{_bindir}/*config %{buildroot}%{_bindir}/*sh \
    %{buildroot}%{_bindir}/ufo-sanitizer \
    %{buildroot}%{_libdir}/*.la
chrpath --replace %{_libdir} %{buildroot}%{_bindir}/*.opt \
                             %{buildroot}%{_bindir}/whizard

rm -rf %{buildroot}/omega
# TODO re-enable
rm -rf %{buildroot}/%{_datadir}/circe1 %{buildroot}/%{_datadir}/circe2

%clean
rm -rf %{buildroot}
#rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.0*
%dir %{_libdir}/whizard
%dir %{_libdir}/whizard/models
%{_libdir}/whizard/models/*.so.0*
%dir %{_libdir}/omega
%dir %{_libdir}/omega/caml
%{_libdir}/omega/caml/*

%dir %{_datadir}/whizard
%dir %{_datadir}/whizard/SM_tt_threshold_data              
%dir %{_datadir}/whizard/beam-sim
%dir %{_datadir}/whizard/cuts
%dir %{_datadir}/whizard/examples
%dir %{_datadir}/whizard/models
%dir %{_datadir}/whizard/muli
%dir %{_datadir}/whizard/pdf_builtin
%dir %{_datadir}/whizard/susy
%{_datadir}/whizard/SM_tt_threshold_data/*
%{_datadir}/whizard/beam-sim/*
%{_datadir}/whizard/cuts/*
%{_datadir}/whizard/examples/*
%{_datadir}/whizard/models/*
%{_datadir}/whizard/muli/*
%{_datadir}/whizard/pdf_builtin/*
%{_datadir}/whizard/susy/*

%package devel
Summary: Development files for calculation of multi-particle scattering cross sections
Requires: libtirpc-devel
Requires: pythia8-devel
Requires: lhapdf-devel
Requires: HepMC3-devel
Requires: HepMC3-search-devel
Requires: HepMC3-interfaces-devel

%description devel
Toolkit for efficient calculation of multi-particle scattering cross sections
and simulated event samples (Development files). 

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/whizard/models/*.so
%{_libdir}/whizard/models/*.la
%{_libdir}/whizard/models/*.a
%{_libdir}/whizard/libtool
%{_includedir}/whizard.h

%changelog
* Mon Jan 13 2025 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 3.1.5-1
- Repackaging for Alma Linux 9

