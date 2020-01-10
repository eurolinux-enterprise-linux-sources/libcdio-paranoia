Name: libcdio-paranoia
Version: 10.2+0.90
Release: 11%{?dist}
Summary: CD paranoia on top of libcdio
Group: System Environment/Libraries
License: GPLv2+ and LGPLv2+
URL: http://www.gnu.org/software/libcdio/
Source0: http://ftp.gnu.org/gnu/libcdio/libcdio-paranoia-%{version}.tar.gz
# Missing in tarball
Source1: https://raw.github.com/rocky/libcdio-paranoia/master/COPYING-GPL
# Missing in tarball
Source2: https://raw.github.com/rocky/libcdio-paranoia/master/COPYING-LGPL
# fixes from git
# wrong fsf address and missing pkgconfig requires
Patch0: most-of-4c30a84f7899ff63c9bbc39563099f98752c83d6.patch
# Patch1 and Patch2 fixes the license headers in the source files
Patch1: most-of-a500a7037729aaeaba9bfda9c007d598e8fa8adc.patch
Patch2: https://github.com/rocky/libcdio-paranoia/commit/5f8c33d04fcf7b4cede360e79cc3806e9139127f.patch
Patch3: libcdio-paranoia-manpage.patch
BuildRequires: pkgconfig 
BuildRequires: gettext-devel
BuildRequires: chrpath
BuildRequires: libcdio-devel


%description
This CDDA reader distribution ('libcdio-cdparanoia') reads audio from the
CDROM directly as data, with no analog step between, and writes the
data to a file or pipe as .wav, .aifc or as raw 16 bit linear PCM.

Split off from libcdio to allow more flexible licensing and to be compatible
with cdparanoia-III-10.2's license. And also, libcdio is just too large.

%package devel
Summary: Header files and libraries for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains header files and libraries for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# fix pkgconfig files
sed -i -e 's,-I${includedir},-I${includedir}/cdio,g' libcdio_paranoia.pc.in
sed -i -e 's,-I${includedir},-I${includedir}/cdio,g' libcdio_cdda.pc.in

f=doc/ja/cd-paranoia.1.in
iconv -f euc-jp -t utf-8 -o $f.utf8 $f && mv $f.utf8 $f
iconv -f ISO88591 -t utf-8 -o THANKS.utf8 THANKS && mv THANKS.utf8 THANKS

cp %{SOURCE1} .
cp %{SOURCE2} .

%build
%configure \
	--disable-dependency-tracking \
	--disable-static \
	--disable-rpath
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

mv $RPM_BUILD_ROOT%{_mandir}/{jp,ja}

# copy include files to an additional directory
# this will probably be the location for future releases see:
# https://github.com/rocky/libcdio-paranoia/commit/b2807f3c7a4126b6078d96adbd37c3760b9f41ab
mkdir -p $RPM_BUILD_ROOT%{_includedir}/cdio/paranoia
cp -a $RPM_BUILD_ROOT%{_includedir}/cdio/*.h $RPM_BUILD_ROOT%{_includedir}/cdio/paranoia

# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so.*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README THANKS COPYING-GPL COPYING-LGPL
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*


%files devel
%defattr(-,root,root,-)
%doc doc/FAQ.txt doc/overlapdef.txt
%{_includedir}/cdio/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Feb 21 2014 Frantisek Kluknavsky <fkluknav@redhat.com> - 10.2+0.90-11
- rebuilt for libcdio-0.92
- Resolves: rhbz#1065642

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 10.2+0.90-10
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 10.2+0.90-9
- Mass rebuild 2013-12-27

* Wed Jul 31 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 10.2+0.90-8
- long name in manual page caused 'whatis' to misbehave

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2+0.90-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 11 2013 Adrian Reber <adrian@lisas.de> - 10.2+0.90-6
- remove sed changes on non-installed file
- fix -devel subpackage Require

* Sat Dec 22 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-5
- provide include files also in the paranoia directory (like in upstream's git)

* Thu Nov 22 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-4
- fix pkgconfig files to point to right include directory

* Mon Nov 05 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-3
- included upstreamed patches which are changing the license
  headers to be LGPLv2+ for the library parts and GPLv2+ for the
  binaries

* Tue Oct 30 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-2
- added missing files from git: COPYING-GPL and COPYING-LGPL
- added patch from git for missing pkgconfig requires
  and fixed FSF address

* Mon Oct 29 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-1
- initial release
