%define	module	pyopencl

%define %define __noautoreq libOpenCL.*

Summary:	Python wrapper for OpenCL

Name:		python-%{module}
Version:	2012.1
Release:	4
Source0:	%{module}-%{version}.tar.gz
License:	MIT
Group:		Development/Python
Url:		http://mathema.tician.de/software/pyopencl
Requires:	nvidia-current-cuda-opencl
BuildRequires:	nvidia-cuda-toolkit-devel
BuildRequires:	nvidia-current-cuda-opencl
BuildRequires:	nvidia-current-devel
BuildRequires:	python-sphinx
BuildRequires:	python-setuptools >= 0.6c9
BuildRequires:	python-numpy-devel >= 1.0.4
BuildRequires:	boost-devel
BuildRequires:	python-mako
BuildRequires:	python-devel

%description
PyOpenCL gives you easy, Pythonic access to the OpenCL parallel
computation API. What makes PyOpenCL special?

* Object cleanup tied to lifetime of objects. This idiom, often called
  RAII in C++, makes it much easier to write correct, leak- and
  crash-free code.
* Completeness. PyOpenCL puts the full power of OpenCL’s API at your
  disposal, if you wish. Every obscure get_info() query and all CL
  calls are accessible.
* Automatic Error Checking. All errors are automatically translated
  into Python exceptions.
* Speed. PyOpenCL's base layer is written in C++, so all the niceties
  above are virtually free.
* Helpful Documentation.

This package has been build against NVIDIA's OpenCL implementation.

%prep
%setup -q -n %{module}-%{version}

%build

%__python ./configure.py --cl-lib-dir=/usr/lib/nvidia-current,/usr/lib64/nvidia-current \
--boost-inc-dir=/usr/include/,/usr/include/boost \
--boost-lib-dir=/usr/lib,/usr/lib64 --boost-python-libname=boost_python 
%__python setup.py build

pushd doc/
export PYTHONPATH=`dir -d ../build/lib.linux*`
make PAPER=letter html
find -name .buildinfo | xargs rm -f
popd

%install
PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot}

%clean

%files
%doc doc/build/html/ examples/ README
%{_includedir}/pyopencl/*
%{py_platsitedir}/pyopencl*

