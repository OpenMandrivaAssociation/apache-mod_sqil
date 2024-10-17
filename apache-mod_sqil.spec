#Module-Specific definitions
%define mod_name mod_sqil
%define mod_conf A72_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Structured Query Interface Language (SQIL) module for Apache2
Name:		apache-%{mod_name}
Version:	1.0
Release:	%mkrel 11
Group:		System/Servers
License:	Apache License
URL:		https://www.heute-morgen.de/modules/mod_sqil/
Source0:	%{mod_name}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_sqil-format_not_a_string_literal_and_no_format_arguments.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Requires:	apache-mod_xmlns
Requires:	apache-mod_form
Requires:	apache-mod_delay
BuildRequires:  apache-devel >= 2.2.0
BuildRequires:	apache-mod_xmlns-devel
BuildRequires:	apache-mod_form-devel
BuildRequires:	apache-mod_delay-devel
BuildRequires:	librecode-devel
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_sqil is an output filter module that generates XML from database content
based on the queries it gets as input. The input format is Structured Query
Interface Language, a simple XML dialect that uses tags as column aliases and
for bind variables. Its purpose is to generate XML using readable SQL. It can
not generate arbitrarily formatted XML or HTML.

%prep

%setup -q -n %{mod_name}
%patch0 -p0

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type d -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -c %{mod_name}.c %{_libdir}/librecode.la

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc SQIL.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


