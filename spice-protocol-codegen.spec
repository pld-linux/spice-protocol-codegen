# NOTE: compatibility package, will most likely go away after spice 0.12.6/0.13.0
Summary:	SPICE code generator
Summary(pl.UTF-8):	Generator kodu SPICE
Name:		spice-protocol-codegen
# the only spice-protocol release containing codegen
Version:	0.12.10
Release:	1
License:	BSD
Group:		Development/Tools
Source0:	http://www.spice-space.org/download/releases/spice-protocol-%{version}.tar.bz2
# Source0-md5:	1fb9d0dcdd42dce1b476ae8aa7569bcc
URL:		http://www.spice-space.org/
BuildRequires:	python >= 2
BuildRequires:	python-pyparsing
BuildRequires:	python-six
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.446
BuildRequires:	sed >= 4.0
Requires:	python-pyparsing
Requires:	python-six
Conflicts:	spice-protocol = 0.12.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SPICE code generator.

The Spice project aims to provide a complete open source solution for
interaction with virtualized desktop devices.

%description -l pl.UTF-8
Generator kodu SPICE.

Celem projektu Spice jest dostarczenie pełnego, mającego otwarte
źródła rozwiązania do interakcji z wirtualizowanymi urządzeniami
biurkowymi.

%prep
%setup -q -n spice-protocol-%{version}

%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' spice_codegen.py

%build
# use arch-agnostic libdir
%configure \
	--libdir=%{_datadir} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_npkgconfigdir}/spice-protocol{,-codegen}.pc
%{__sed} -i -e '/^Name:/s/spice-protocol$/spice-protocol-codegen/' $RPM_BUILD_ROOT%{_npkgconfigdir}/spice-protocol-codegen.pc

%py_comp $RPM_BUILD_ROOT%{_datadir}/spice-protocol
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/spice-protocol
%py_postclean %{_datadir}/spice-protocol/python_modules

# packaged in spice-protocol
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/spice-1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING NEWS 
%dir %{_datadir}/spice-protocol
%{_datadir}/spice-protocol/spice.proto
%{_datadir}/spice-protocol/spice1.proto
%attr(755,root,root) %{_datadir}/spice-protocol/spice_codegen.py
%{_datadir}/spice-protocol/spice_codegen.py[co]
%dir %{_datadir}/spice-protocol/python_modules
%{_datadir}/spice-protocol/python_modules/*.py[co]
%{_npkgconfigdir}/spice-protocol-codegen.pc
