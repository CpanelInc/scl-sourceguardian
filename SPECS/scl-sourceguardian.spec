%define debug_package %{nil}

%global extension_type php
%global upstream_name sourceguardian

%{?scl:%global _scl_prefix /opt/cpanel}
%{?scl:%scl_package %{extension_type}-%{upstream_name}}
%{?scl:BuildRequires: scl-utils-build}
%{?scl:Requires: %scl_runtime}
%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package_override}

# must redefine this in the spec file because OBS doesn't know how
# to handle macros in BuildRequires statements
%{?scl:%global scl_prefix %{scl}-}

# OBS builds the 32-bit targets as arch 'i586', but 32-bit archive is
# named 'i386'.  Other archives are named as the actual architecture.
%if "%{_arch}" == "i586"
%global archive_arch i386
%else
%global archive_arch %{_arch}
%endif

Name:    %{?scl_prefix}%{extension_type}-%{upstream_name}
Vendor:  SourceGuardian Ltd.
Summary: Loader for SourceGuardian-encoded PHP files
Version: 11.0.6
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4592 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: Redistributable
Group:   Development/Languages
URL:     http://www.sourceguardian.com/loaders.php
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# There is a different distribution archive per architecture.  The
# archive contains the license file, so no need to have it as a
# separate source file.
Source: https://www.sourceguardian.com/loaders/download/loaders.linux-%{archive_arch}.tar.bz2

%{?scl:BuildRequires: %{?scl_prefix}scldevel}
%{?scl:BuildRequires: %{?scl_prefix}build}
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
* Fri Nov 18 2016 Edwin Buck <e.buck@cpanel.net> - 11.0.6-1
- EA-4383: Update Release value to OBS-proof versioning

* Mon Jun 20 2016 Dan Muey <dan@cpanel.net> - 10.1.5-5
- EA-4383: Update Release value to OBS-proof versioning

* Thu Mar 24 2016 Jacob Perkins <jacob.perkins@cpanel.net> 10.1.5-3
- Fixed upstream_name

* Wed Mar 09 2016 S. Kurt Newman <kurt.newman@cpanel.net> - 10.1.5-2
- Resolve internal SCL builds optimizations with Makefiles (EA-4269)

* Fri Jul 17 2015 Trinity Quirk <trinity.quirk@cpanel.net> - 10.1.5-1
- Initial creation
