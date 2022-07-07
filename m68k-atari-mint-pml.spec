# we are cross-compiled libraries
%global debug_package %{nil}

%global patchdate 20110207
%global __strip /bin/true

Name:           m68k-atari-mint-pml
Summary:        Portable Math Library
Version:        2.03
Release:        1.%{patchdate}%{?dist}
License:        Public Domain
URL:            https://github.com/freemint/pml
Source0:        %{url}/archive/pml-%{version}/pml-%{version}.tar.gz
Patch0:         http://vincent.riviere.free.fr/soft/m68k-atari-mint/archives/pml-%{version}-mint-%{patchdate}.patch.bz2
BuildArch:      noarch
BuildRequires:  m68k-atari-mint-gcc
BuildRequires:  m68k-atari-mint-mintlib
Requires:       m68k-atari-mint-filesystem


%description
PML, the Portable Math Library for Atari MiNT.
This package is primarily for Atari MiNT developers and is
not needed by normal users or developers.


%prep
%setup -q -n pml-pml-%{version}
%patch0 -p1


%build
cp -a pmlsrc pmlsrc-m68020-60
pushd pmlsrc-m68020-60
sed -i "s:^\(CFLAGS =.*\):\1 -m68020-60:g" Makefile.32 Makefile.16
sed -i "s:^\(CROSSLIB =.*\):\1/m68020-60:g" Makefile
popd

cp -a pmlsrc pmlsrc-m5475
pushd pmlsrc-m5475
sed -i "s:^\(CFLAGS =.*\):\1 -mcpu=5475:g" Makefile.32 Makefile.16
sed -i "s:^\(CROSSLIB =.*\):\1/m5475:g" Makefile
popd

for d in pmlsrc*
do
    ( cd $d; make CROSSDIR=%{mint_prefix} CC=m68k-atari-mint-gcc AR=m68k-atari-mint-ar CPPFLAGS=-I%{mint_includedir} )
done


%install
for d in pmlsrc*
do
    ( cd $d; make install CROSSDIR=%{buildroot}%{mint_prefix} )
done

# cleanup
rm -rf %{buildroot}%{mint_mandir}


%files
%doc README pmlsrc/README.MJR
%{mint_includedir}/*
%{mint_libdir}/*


%changelog
* Thu Jul 07 2022 Dan Horák <dan[at]danny.cz> - 2.03-1.20110207
- initial Fedora release
