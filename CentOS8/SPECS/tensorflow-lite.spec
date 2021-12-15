%define debug_package %{nil}

Summary: Tensorflow library for inference on mobile
Name: tensorflow-lite
Version: 2.7.0
Release: 1.muonc%{?dist}
License: Apache License Version 2.0
Vendor: INFN
URL: https://www.tensorflow.org/lite
Group: Development/Libraries
BuildArch: %{_arch}
BuildRequires: cmake
BuildRequires: make
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
%if ! ("x%{mc_source_url}" == "x")
%undefine _disable_source_fetch
Source0: %{mc_source_url}/tensorflow-%{version}.tar.gz
%else
Source0: tensorflow-%{version}.tar.gz
%endif
Source1: tensorflow-lite-CMakeLists.txt
Source2: tensorflow-liteConfig.cmake.in
Source3: tensorflow-liteConfigVersion.cmake.in


%global tflitelib_src_dir %{_builddir}/%{name}-%{version}/tensorflow/lite/examples/tflitelib
%global tflite_cmake_dir %{_libdir}/cmake/%{name}

%description
Tensorflow library for inference on mobile

%prep
%setup -c
rm -rf %{buildroot}
mkdir -p %{buildroot}

%build
mkdir -p %{tflitelib_src_dir}/build
cp %{SOURCE1} %{tflitelib_src_dir}/CMakeLists.txt
cp %{SOURCE2} %{SOURCE3} %{tflitelib_src_dir}

cd %{tflitelib_src_dir}/build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_CXX_STANDARD=17 \
      -DINSTALL_LIB_DIR=%{buildroot}%{_libdir} \
      -Wno-dev \
      ..
make %{?_smp_mflags} tensorflow-lite

%install
cd %{tflitelib_src_dir}/build
make install

sed -i -e 's|%{buildroot}/usr|%{_prefix}|g' %{buildroot}%{tflite_cmake_dir}/*.cmake


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.a


%package devel
Summary: Tensorflow library for inference on mobile (development files)
Requires: %{name}

%description devel
Tensorflow library for inference on mobile

%files devel
%defattr(-,root,root)
%dir %{_includedir}/tensorflow
%dir %{_includedir}/tensorflow/core
%dir %{_includedir}/tensorflow/core/public
%{_includedir}/tensorflow/core/public/*.h
%dir %{_includedir}/tensorflow/lite
%{_includedir}/tensorflow/lite/*.h
%dir %{_includedir}/tensorflow/lite/c
%{_includedir}/tensorflow/lite/c/*.h
%dir %{_includedir}/tensorflow/lite/core
%{_includedir}/tensorflow/lite/core/*.h
%dir %{_includedir}/tensorflow/lite/core/api
%{_includedir}/tensorflow/lite/core/api/*.h
%dir %{_includedir}/tensorflow/lite/core/shims
%dir %{_includedir}/tensorflow/lite/core/shims/c
%{_includedir}/tensorflow/lite/core/shims/c/*.h
%dir %{_includedir}/tensorflow/lite/core/shims/c/experimental/
%dir %{_includedir}/tensorflow/lite/core/shims/c/experimental/acceleration/
%dir %{_includedir}/tensorflow/lite/core/shims/c/experimental/acceleration/configuration/
%{_includedir}/tensorflow/lite/core/shims/c/experimental/acceleration/configuration/*.h
%dir %{_includedir}/tensorflow/lite/core/shims/cc
%{_includedir}/tensorflow/lite/core/shims/cc/*.h
%dir %{_includedir}/tensorflow/lite/core/shims/cc/experimental/
%dir %{_includedir}/tensorflow/lite/core/shims/cc/experimental/acceleration/
%dir %{_includedir}/tensorflow/lite/core/shims/cc/experimental/acceleration/configuration/
%{_includedir}/tensorflow/lite/core/shims/cc/experimental/acceleration/configuration/*.h
%dir %{_includedir}/tensorflow/lite/core/shims/cc/kernels
%{_includedir}/tensorflow/lite/core/shims/cc/kernels/*.h
%dir %{_includedir}/tensorflow/lite/core/shims/jni
%{_includedir}/tensorflow/lite/core/shims/jni/*.h
%dir %{_includedir}/tensorflow/lite/experimental
%dir %{_includedir}/tensorflow/lite/experimental/acceleration
%dir %{_includedir}/tensorflow/lite/experimental/acceleration/compatibility
%{_includedir}/tensorflow/lite/experimental/acceleration/compatibility/*.h
%dir %{_includedir}/tensorflow/lite/experimental/acceleration/configuration
%{_includedir}/tensorflow/lite/experimental/acceleration/configuration/*.h
%dir %{_includedir}/tensorflow/lite/experimental/acceleration/configuration/c
%{_includedir}/tensorflow/lite/experimental/acceleration/configuration/c/*.h
%dir %{_includedir}/tensorflow/lite/experimental/acceleration/mini_benchmark
%{_includedir}/tensorflow/lite/experimental/acceleration/mini_benchmark/*.h
%dir %{_includedir}/tensorflow/lite/experimental/microfrontend
%{_includedir}/tensorflow/lite/experimental/microfrontend/*.h
%dir %{_includedir}/tensorflow/lite/experimental/microfrontend/lib
%{_includedir}/tensorflow/lite/experimental/microfrontend/lib/*.h
%dir %{_includedir}/tensorflow/lite/experimental/resource
%{_includedir}/tensorflow/lite/experimental/resource/*.h
%dir %{_includedir}/tensorflow/lite/internal
%{_includedir}/tensorflow/lite/internal/*.h
%dir %{_includedir}/tensorflow/lite/kernels
%{_includedir}/tensorflow/lite/kernels/*.h
%dir %{_includedir}/tensorflow/lite/kernels/ctc
%{_includedir}/tensorflow/lite/kernels/ctc/*.h
%dir %{_includedir}/tensorflow/lite/kernels/shim
%{_includedir}/tensorflow/lite/kernels/shim/*.h
%dir %{_includedir}/tensorflow/lite/kernels/shim/test_op
%{_includedir}/tensorflow/lite/kernels/shim/test_op/*.h
%dir %{_includedir}/tensorflow/lite/kernels/gradient
%{_includedir}/tensorflow/lite/kernels/gradient/*.h
%dir %{_includedir}/tensorflow/lite/kernels/internal
%{_includedir}/tensorflow/lite/kernels/internal/*.h
%dir %{_includedir}/tensorflow/lite/kernels/internal/optimized
%{_includedir}/tensorflow/lite/kernels/internal/optimized/*.h
%dir %{_includedir}/tensorflow/lite/kernels/internal/optimized/integer_ops
%{_includedir}/tensorflow/lite/kernels/internal/optimized/integer_ops/*.h
%dir %{_includedir}/tensorflow/lite/kernels/internal/optimized/sparse_ops
%{_includedir}/tensorflow/lite/kernels/internal/optimized/sparse_ops/*.h
%dir %{_includedir}/tensorflow/lite/kernels/internal/reference
%{_includedir}/tensorflow/lite/kernels/internal/reference/*.h
%dir %{_includedir}/tensorflow/lite/kernels/internal/reference/integer_ops
%{_includedir}/tensorflow/lite/kernels/internal/reference/integer_ops/*.h
%dir %{_includedir}/tensorflow/lite/kernels/internal/reference/sparse_ops
%{_includedir}/tensorflow/lite/kernels/internal/reference/sparse_ops/*.h
%dir %{_includedir}/tensorflow/lite/kernels/internal/utils
%{_includedir}/tensorflow/lite/kernels/internal/utils/*.h
%dir %{_includedir}/tensorflow/lite/kernels/parse_example
%{_includedir}/tensorflow/lite/kernels/parse_example/*.h
%dir %{_includedir}/tensorflow/lite/kernels/perception
%{_includedir}/tensorflow/lite/kernels/perception/*.h
%dir %{_includedir}/tensorflow/lite/profiling
%{_includedir}/tensorflow/lite/profiling/*.h
%dir %{_includedir}/tensorflow/lite/schema
%{_includedir}/tensorflow/lite/schema/*.h
%dir %{_includedir}/tensorflow/lite/schema/builtin_ops_header
%{_includedir}/tensorflow/lite/schema/builtin_ops_header/*.h
%dir %{_includedir}/tensorflow/lite/schema/builtin_ops_list
%{_includedir}/tensorflow/lite/schema/builtin_ops_list/*.h
%dir %{_includedir}/flatbuffers
%{_includedir}/flatbuffers/*.h
%dir %{tflite_cmake_dir}
%{tflite_cmake_dir}/*.cmake

%changelog
* Tue Dec 07 2021 Paolo Andreetto <paolo.andreetto@pd.infn.it> - 2.7.0-1
- Repackaging for CentOS 8

