%undefine _disable_source_fetch
%global debug_package %{nil}

%global _pver 1.14.1
%global _tagver 01-14-01

%global _sbuilddir %{_builddir}/%{name}-%{version}/KalDet-%{_tagver}

Summary: Kalman filter algorithms applied to detectors
Name: ilc-kaldet-headers
Version: %{_pver}
Release: 1%{?dist}
License: GPL v.3
Vendor: INFN
URL: https://github.com/iLCSoft/KalDet
Group: Development/Libraries
BuildArch: %{_arch}
Requires: ilc-utils-devel
Requires: ilc-kaltest-devel
Requires: ilc-marlin-devel
Requires: ilc-marlin-util-devel
Requires: ilc-gear-devel
Requires: root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/iLCSoft/KalDet/archive/refs/tags/v%{_tagver}.tar.gz
AutoReqProv: yes

%description
Kalman filter algorithms applied to detectors.

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
echo "Nothing to build"

%install
mkdir -p %{buildroot}%{_includedir}/kaldet/gen
mkdir %{buildroot}%{_includedir}/kaldet/kern
mkdir -p %{buildroot}%{_includedir}/kaldet/lctpc/gearTPC

cp %{_sbuilddir}/gen/*.h %{buildroot}%{_includedir}/kaldet/gen
cp %{_sbuilddir}/kern/*.h %{buildroot}%{_includedir}/kaldet/kern
cp %{_sbuilddir}/lctpc/gearTPC/*.h %{buildroot}%{_includedir}/kaldet/lctpc/gearTPC

find %{_sbuilddir}/ild -name '*.h' -exec cp '{}' %{buildroot}%{_includedir}/kaldet \;

ln -s %{_includedir}/kaldet/gen/EXEventGen.h %{buildroot}%{_includedir}/kaldet
ln -s %{_includedir}/kaldet/kern/EXVKalDetector.h %{buildroot}%{_includedir}/kaldet
ln -s %{_includedir}/kaldet/kern/EXVMeasLayer.h %{buildroot}%{_includedir}/kaldet

for item in `ls %{buildroot}%{_includedir}/kaldet/lctpc/gearTPC/EXTPC*.h`; do 
    ln -s %{_includedir}/kaldet/lctpc/gearTPC/`basename ${item}` %{buildroot}%{_includedir}/kaldet
done

for item in `ls %{buildroot}%{_includedir}/kaldet/lctpc/gearTPC/GEAR*.h`; do 
    ln -s %{_includedir}/kaldet/lctpc/gearTPC/`basename ${item}` %{buildroot}%{_includedir}/kaldet
done


%clean
rm -rf %{buildroot}
rm -f %{SOURCE0}

%files
%defattr(-,root,root)
%dir %{_includedir}/kaldet
%dir %{_includedir}/kaldet/gen
%dir %{_includedir}/kaldet/kern
%dir %{_includedir}/kaldet/lctpc
%dir %{_includedir}/kaldet/lctpc/gearTPC
%{_includedir}/kaldet/*.h
%{_includedir}/kaldet/gen/*.h
%{_includedir}/kaldet/kern/*.h
%{_includedir}/kaldet/lctpc/gearTPC/*.h

%changelog
* Mon Jul 13 2020 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 1.14.1-1
- Repackaging for CentOS 8


