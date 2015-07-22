%define debug_package %{nil}

# Package namespaces
%global ns_name ea
%global ns_dir /opt/cpanel
%global _scl_prefix %ns_dir

%scl_package %scl

# This makes the ea-php<ver>-build macro stuff work
%scl_package_override

# OBS builds the 32-bit targets as arch 'i586', but 32-bit archive is
# named 'i386'.  Other archives are named as the actual architecture.
%if "%{_arch}" == "i586"
%global archive_arch i386
%else
%global archive_arch %{_arch}
%endif

Name:    %{?scl_prefix}php-sourceguardian
Vendor:  SourceGuardian Ltd.
Summary: Loader for SourceGuardian-encoded PHP files
Version: 10.1.5
Release: 1%{?dist}
License: Redistributable
Group:   Development/Languages
URL:     http://www.sourceguardian.com/loaders.php

# There is a different distribution archive per architecture.  The
# archive contains the license file, so no need to have it as a
# separate source file.
Source: https://www.sourceguardian.com/loaders/download/loaders.linux-%{archive_arch}.tar.gz

BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix}scldevel
BuildRequires: %{?scl_prefix}build
BuildRequires: %{?scl_prefix}php-devel
Requires:      %{?scl_prefix}php(api) = %{php_core_api}

# Don't provide extensions as shared library resources
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.lin$}
%{?filter_setup}

%description
The SourceGuardian Loader enables use of SourceGuardian-encoded PHP
files running under PHP %{php_version}.

%prep
%setup -q -c -n sourceguardian

%build
# For some reason, CentOS7 builds do not like spaces in filenames
mv 'SourceGuardian Loader License.pdf' SourceGuardian_Loader_License.pdf

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

# The module itself
install -d -m 755 $RPM_BUILD_ROOT%{php_extdir}
install -m 755 ixed.%{php_version}.lin $RPM_BUILD_ROOT%{php_extdir}

# The ini snippet
install -d -m 755 $RPM_BUILD_ROOT%{php_inidir}
cat > $RPM_BUILD_ROOT%{php_inidir}/sourceguardian.ini <<EOF
; Enable SourceGuardian Loader extension module
extension=ixed.%{php_version}.lin
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README SourceGuardian_Loader_License.pdf
%config(noreplace) %{php_inidir}/sourceguardian.ini
%{php_extdir}/ixed.%{php_version}.lin

%changelog
* Fri Jul 17 2015 Trinity Quirk <trinity.quirk@cpanel.net> - 10.1.5-1
- Initial creation
