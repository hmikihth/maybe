%define name 		maybe
%define Summary		See what a program does before deciding whether you really want it to happen.
%define sourcetype      tar.gz
%define version         0.4.0

Name:         %name
Summary:       %Summary
Summary(hu):   %Summary_hu
Version:       %version
Release:       %mkrel 1
License:       GPL3
Distribution: blackPanther OS
Vendor:       blackPanther Europe
Packager:     Miklos Horvath
Group:        Development/Tools
Source0:      %name-%version.%sourcetype
Buildroot:     %_tmppath/%name-%version-%release-root

Requires:     python3 >= 3.4
Requires:     python3-ptrace >= 0.8.1
Requires:     glibc >= 2.19.2

%description
maybe runs processes under the control of ptrace (with the help of 
the excellent python-ptrace library). 
When it intercepts a system call that is about to make changes to 
the file system, it logs that call, and then modifies CPU registers 
to both redirect the call to an invalid syscall ID (effectively 
turning it into a no-op) and set the return value of that no-op call 
to one indicating success of the original call.

As a result, the process believes that everything it is trying to do 
is actually happening, when in reality nothing is.

%files
%defattr(-,root,root)
%_bindir/
%_datadir/
%python3_sitelib

%prep
%setup -q 

%build
%{__python3} setup.py build
%{__python3} setup.py build_scripts

%install
%{__python3} setup.py install --skip-build --root %{buildroot}
%{__python3} setup.py install --skip-build --no-compile --root %{buildroot}


%clean
rm -rf %buildroot


%changelog
* Sun Apr 03 2016 Miklos Horvath <hmiki@blackpantheros.eu> 
- initial version
