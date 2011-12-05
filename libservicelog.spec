Name:           libservicelog
Version:        1.1.9
Release:        4%{?dist}
Summary:        Servicelog Database and Library

Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://linux-diag.sourceforge.net/servicelog
Source0:        http://downloads.sourceforge.net/linux-diag/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre):       shadow-utils

BuildRequires:  sqlite-devel autoconf libtool flex bison librtas-devel

# because of librtas-devel
ExclusiveArch: ppc ppc64

# Don't use non existin group during install 
Patch0: libservicelog-1.1.9-install.patch

# Added missing include
Patch1: libservicelog-1.1.9-include.patch

# Link with needed libraries
Patch2: libservicelog-1.1.9-libs.patch

%description
The libservicelog package contains a library to create and maintain a
database for storing events related to system service.  This database
allows for the logging of serviceable and informational events, and for
the logging of service procedures that have been performed upon the system.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig sqlite-devel

%description    devel
Contains header files for building with libservicelog.


%prep
%setup -q -n %{name}-1.1
%patch0 -p1 -b .install
%patch1 -p1 -b .include
%patch2 -p1 -b .libs

%build
autoreconf -fiv
%configure --disable-static
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__rm} -f %{buildroot}%{_libdir}/*.la


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group service >/dev/null || /usr/sbin/groupadd service

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING NEWS AUTHORS
%{_libdir}/libservicelog-*.so.*
%ghost %verify(not md5 size mtime) %attr(644,root,service) %dir /var/lib/servicelog/servicelog.db
%dir /var/lib/servicelog

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/servicelog-1
%{_libdir}/pkgconfig/servicelog-1.pc


%changelog
* Fri Jun 04 2010 Roman Rakus <rrakus@redhat.com> - 1.1.9-4
- Properly handle servicelog.db (PW review)
  Resolves: #590023

* Tue May 18 2010 Roman Rakus <rrakus@redhat.com> - 1.1.9-3
- Removed executable bit from servicelog.db file (PW review)
- fixed postun scriptlet (PW review)
  Resolves: #590023

* Tue May 18 2010 Roman Rakus <rrakus@redhat.com> - 1.1.9-2
- Link with needed libraries (sqlite, rtas, rtasevent)
  Resolves: #590023

* Fri May 14 2010 Roman Rakus <rrakus@redhat.com> - 1.1.9-1
- Update to 1.1.9
  Resolves: #590023

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.0.1-3.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 31 2009 Roman Rakus <rrakus@redhat.com> - 1.0.1-2
- Added missing requires sqlite-devel in devel subpackage

* Fri Feb 20 2009 Roman Rakus <rrakus@redhat.com> - 1.0.1-1
- Initial packaging
