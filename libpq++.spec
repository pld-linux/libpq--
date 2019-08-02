Summary:	Older implementation of C++ interface to PostgreSQL
Summary(pl.UTF-8):	Starsza implementacja interfejsu C++ do PostgreSQL
Name:		libpq++
Version:	4.0
Release:	5
License:	BSD
Group:		Libraries
Source0:	https://ftp.postgresql.org/pub/projects/gborg/libpqpp/stable/%{name}-%{version}.tar.gz
# Source0-md5:	da71cb79ef45cef55f4bc97a33a0857d
Patch0:		%{name}-make.patch
Patch1:		%{name}-libdir.patch
Patch2:		include.patch
URL:		https://www.postgresql.org/docs/7.0/libpqplusplus.htm
BuildRequires:	libstdc++-devel
BuildRequires:	postgresql-devel >= 7.3
Provides:	postgresql-c++
Obsoletes:	postgresql-c++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package includes library for C++ interface to PostgreSQL. It's
an older implementation, included with PostgreSQL up to 7.2.x.

%description -l pl.UTF-8
Pakiet ten zawiera biblioteki dla interfejsu C++ do PostgreSQL. Jest
to starsza implementacja, dołączana do PostgreSQL-a aż do 7.2.x.

%package devel
Summary:	Older C++ interface to PostgreSQL - development part
Summary(pl.UTF-8):	Starszy interfejs C++ do PostgreSQL - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	postgresql-devel
Provides:	postgresql-c++-devel
Obsoletes:	postgresql-c++-devel

%description devel
This package includes header files for older C++ interface.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki nagłówkowe dla starszego interfejsu C++.

%package static
Summary:	Older C++ interface to PostgreSQL - static libraries
Summary(pl.UTF-8):	Starszy interfejs C++ do PostgreSQL - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	postgresql-c++-static
Obsoletes:	postgresql-c++-static

%description static
This package includes static library for older interface C++.

%description static -l pl.UTF-8
Pakiet ten zawiera biblioteki statyczne dla starszego interfejsu C++.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1

%build
%{__make} static \
	POSTGRES_HOME=%{_prefix} \
	LIBDIR=%{_libdir} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} -Wall"

%{__rm} *.o
%{__make} \
	POSTGRES_HOME=%{_prefix} \
	LIBDIR=%{_libdir} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} -Wall -fPIC" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir} \
	POSTGRES_HOME=%{_prefix}

ln -sf libpq++.so.4.0 $RPM_BUILD_ROOT%{_libdir}/libpq++.so.4

install examples/*.* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_libdir}/libpq++.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libpq++.so.4

%files devel
%defattr(644,root,root,755)
%doc docs/*.html
%attr(755,root,root) %{_libdir}/libpq++.so
%{_includedir}/libpq++.h
%{_includedir}/libpq++
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libpq++.a
