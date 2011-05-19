%define	module	pyopencl
%define name	python-%{module}
%define version 2011.1
%define rel	beta3
%define release %mkrel 0.%{rel}

%define _requires_exceptions libOpenCL.*

Summary:	Python wrapper for OpenCL
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{module}-%{version}%{rel}.tar.gz
License:	MIT
Group:		Development/Python
Url:		http://mathema.tician.de/software/pyopencl
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	nvidia-cuda-toolkit-devel
BuildRequires:	nvidia-current-cuda-opencl
BuildRequires:	python-sphinx
BuildRequires:	python-setuptools >= 0.6c9
BuildRequires:	python-numpy-devel >= 1.0.4
BuildRequires:	boost-devel
%if %mdkversion < 201100
BuildRequires: 	python-virtualenv
%endif
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
%setup -q -n %{module}-%{version}%{rel}

%build

%if %mdkversion < 201100
virtualenv --distribute CL
./CL/bin/python ./configure.py --cl-lib-dir=/usr/lib/nvidia-current,/usr/lib64/nvidia-current \
--boost-inc-dir=/usr/include/,/usr/include/boost \
--boost-lib-dir=/usr/lib,/usr/lib64 --boost-python-libname=boost_python 
./CL/bin/python setup.py build
%else
%__python ./configure.py --cl-lib-dir=/usr/lib/nvidia-current,/usr/lib64/nvidia-current \
--boost-inc-dir=/usr/include/,/usr/include/boost \
--boost-lib-dir=/usr/lib,/usr/lib64 --boost-python-libname=boost_python 
%__python setup.py build
%endif

pushd doc/
export PYTHONPATH=`dir -d ../build/lib.linux*`
make PAPER=letter html
find -name .buildinfo | xargs rm -f
popd

%install
%__rm -rf %{buildroot}
%if %mdkversion < 201100
PYTHONDONTWRITEBYTECODE= ./CL/bin/python setup.py install --root=tmp/
PYOPENCLROOT=`find tmp/ -name pyopencl-%{version}%{rel}`
echo $PYOPENCLROOT
%__install -d -m 755 %{buildroot}/usr
mv -f $PYOPENCLROOT/CL/* %{buildroot}/usr/
%else
PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot}
%endif

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/build/html/ examples/ README
%py_platsitedir/pyopencl*
