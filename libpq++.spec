Summary:	Older implementation of C++ interface to PostgreSQL
Summary(pl):	Starsza implementacja interfejsu C++ do PostgreSQL
Name:		libpq++
Version:	4.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	ftp://gborg.postgresql.org/pub/libpqpp/stable/%{name}-%{version}.tar.gz
# Source0-md5:	da71cb79ef45cef55f4bc97a33a0857d
Patch0:		%{name}-make.patch
Patch1:		%{name}-libdir.patch
URL:		http://gborg.postgresql.org/project/libpqpp/projdisplay.php
BuildRequires:	postgresql-devel >= 7.3
Obsoletes:	postgresql-c++
Provides:	postgresql-c++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package includes library for C++ interface to PostgreSQL. It's
an older implementation, included with PostgreSQL up to 7.2.x.

%description -l pl
Pakiet ten zawiera biblioteki dla interfejsu C++ do PostgreSQL. Jest
to starsza implementacja, do³±czana do PostgreSQL-a a¿ do 7.2.x.

%package devel
Summary:	Older C++ interface to PostgreSQL - development part
Summary(pl):	Starszy interfejs C++ do PostgreSQL - czê¶æ programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	postgresql-devel
Obsoletes:	postgresql-c++-devel
Provides:	postgresql-c++-devel

%description devel
This package includes header files for older C++ interface.

%description devel -l pl
Pakiet ten zawiera pliki nag³ówkowe dla starszego interfejsu C++.

%package static
Summary:	Older C++ interface to PostgreSQL - static libraries
Summary(pl):	Starszy interfejs C++ do PostgreSQL - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Obsoletes:	postgresql-c++-static
Provides:	postgresql-c++-static

%description static
This package includes static library for older interface C++.

%description static -l pl
Pakiet ten zawiera biblioteki statyczne dla starszego interfejsu C++.

%prep
%setup -q
%patch0 -p1
%patch1 -p0

%build
%{__make} static \
	POSTGRES_HOME=%{_prefix} \
	LIBDIR=%{_libdir} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} -Wall"

rm -f *.o
%{__make} \
	POSTGRES_HOME=%{_prefix} \
	LIBDIR=%{_libdir} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} -Wall -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir} \
	POSTGRES_HOME=%{_prefix}

install examples/*.* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc docs/*.html
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h
%{_includedir}/libpq++
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
