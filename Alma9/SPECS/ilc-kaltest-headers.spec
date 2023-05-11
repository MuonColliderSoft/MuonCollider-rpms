%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 2.5.1
%global _tagver 02-05-01

%global _sbuilddir %{_builddir}/%{name}-%{version}/KalTest-%{_tagver}

Summary: Classes and utilities for Kalman filter algorithms (header files)
Name: ilc-kaltest-headers
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/KalTest
Group: Development/Libraries
BuildArch: %{_arch}
Requires: root
Requires: root-graf3d-eve
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/KalTest/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Classes and utilities for Kalman filter algorithms.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
echo "Nothing to build"

%install
mkdir -p %{buildroot}%{_includedir}/kaltest/bfield
mkdir %{buildroot}%{_includedir}/kaltest/geomlib
mkdir %{buildroot}%{_includedir}/kaltest/kallib
mkdir %{buildroot}%{_includedir}/kaltest/kaltracklib
mkdir %{buildroot}%{_includedir}/kaltest/utils
cp %{_sbuilddir}/src/bfield/*.h %{buildroot}%{_includedir}/kaltest/bfield
cp %{_sbuilddir}/src/geomlib/*.h %{buildroot}%{_includedir}/kaltest/geomlib
cp %{_sbuilddir}/src/kallib/*.h %{buildroot}%{_includedir}/kaltest/kallib
cp %{_sbuilddir}/src/kaltracklib/*.h %{buildroot}%{_includedir}/kaltest/kaltracklib
cp %{_sbuilddir}/src/utils/*.h %{buildroot}%{_includedir}/kaltest/utils

for item in `ls %{buildroot}%{_includedir}/kaltest/bfield/T*.h`; do 
    ln -s %{_includedir}/kaltest/bfield/`basename ${item}` %{buildroot}%{_includedir}/kaltest
done
for item in `ls %{buildroot}%{_includedir}/kaltest/geomlib/T*.h`; do 
    ln -s %{_includedir}/kaltest/geomlib/`basename ${item}` %{buildroot}%{_includedir}/kaltest
done
for item in `ls %{buildroot}%{_includedir}/kaltest/kallib/T*.h`; do 
    ln -s %{_includedir}/kaltest/kallib/`basename ${item}` %{buildroot}%{_includedir}/kaltest
done
for item in `ls %{buildroot}%{_includedir}/kaltest/kaltracklib/T*.h`; do 
    ln -s %{_includedir}/kaltest/kaltracklib/`basename ${item}` %{buildroot}%{_includedir}/kaltest
done
ln -s %{_includedir}/kaltest/kaltracklib/KalTrackDim.h %{buildroot}%{_includedir}/kaltest

for item in `ls %{buildroot}%{_includedir}/kaltest/utils/T*.h`; do 
    ln -s %{_includedir}/kaltest/utils/`basename ${item}` %{buildroot}%{_includedir}/kaltest
done

%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%dir %{_includedir}/kaltest
%dir %{_includedir}/kaltest/bfield
%dir %{_includedir}/kaltest/geomlib
%dir %{_includedir}/kaltest/kallib
%dir %{_includedir}/kaltest/kaltracklib
%dir %{_includedir}/kaltest/utils
%{_includedir}/kaltest/*.h
%{_includedir}/kaltest/bfield/*.h
%{_includedir}/kaltest/geomlib/*.h
%{_includedir}/kaltest/kallib/*.h
%{_includedir}/kaltest/kaltracklib/*.h
%{_includedir}/kaltest/utils/*.h

%changelog
* Wed Jul 13 2022 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.5.1-1
- New version of KalTest
* Thu Jun 18 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.5.0-1
- Repackaging for CentOS 8


