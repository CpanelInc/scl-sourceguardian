%global extension_type php
%global upstream_name sourceguardian
%define debug_package %{nil}
%define _enable_debug_packages %{nil}

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
%global archive_arch %{_arch}

Name:    %{?scl_prefix}%{extension_type}-%{upstream_name}
Vendor:  cPanel, Inc.
Summary: Loader for SourceGuardian-encoded PHP files
Version: 15.0.2
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4592 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: Redistributable
Group:   Development/Languages
URL:     http://www.sourceguardian.com/loaders.html
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# There is a different distribution archive per architecture.  The
# archive contains the license file, so no need to have it as a
# separate source file.
Source: https://www.sourceguardian.com/loaders/download/loaders.linux-%{archive_arch}.tar.bz2

%{?scl:BuildRequires: %{?scl_prefix}scldevel}
%{?scl:BuildRequires: %{?scl_prefix}build}
BuildRequires: %{?scl_prefix}php-devel
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires:      %{?scl_prefix}php-cli

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
* Thu Aug 01 2024 Cory McIntire <cory@cpanel.net> - 15.0.2-1
- EA-12312: Update scl-sourceguardian from v14.0.3 to v15.0.2

* Mon May 22 2023 Cory McIntire <cory@cpanel.net> - 14.0.3-1
- EA-11429: Update scl-sourceguardian from v14.0.2 to v14.0.3

* Tue Apr 04 2023 Julian Brown <julian.brown@cpanel.net> - 14.0.2-2
- ZC-10047: Do not build on Ubuntu 22

* Sun Mar 26 2023 Cory McIntire <cory@cpanel.net> - 14.0.2-1
- EA-11314: Update scl-sourceguardian from v14.0.1 to v14.0.2

* Mon Feb 20 2023 Cory McIntire <cory@cpanel.net> - 14.0.1-1
- EA-11257: Update scl-sourceguardian from v14.0.0 to v14.0.1

* Thu Jan 19 2023 Cory McIntire <cory@cpanel.net> - 14.0.0-1
- EA-11168: Update scl-sourceguardian from v13.0.3 to v14.0.0

* Thu Apr 28 2022 Cory McIntire <cory@cpanel.net> - 13.0.3-2
- EA-10672: Update Sourceguardian to support PHP 8.1

* Fri Apr 15 2022 Cory McIntire <cory@cpanel.net> - 13.0.3-1
- EA-10641: Update scl-sourceguardian from v12.1.2 to v13.0.3

* Tue Dec 28 2021 Dan Muey <dan@cpanel.net> - 12.1.2-2
- ZC-9589: Update DISABLE_BUILD to match OBS

* Mon Oct 04 2021 Cory McIntire <cory@cpanel.net> - 12.1.2-1
- EA-10163: Update scl-sourceguardian from v12.1 to v12.1.2

* Mon Jun 14 2021 Cory McIntire <cory@cpanel.net> - 12.1.0-1
- EA-9862: Update scl-sourceguardian from v12.0.0 to v12.1

* Fri Mar 12 2021 Cory McIntire <cory@cpanel.net> - 12.0.0-2
- EA-9650: Update SourceGuardian to include PHP 8.0

* Mon Mar 01 2021 Cory McIntire <cory@cpanel.net> - 12.0.0-1
- EA-9610: Update scl-sourceguardian from v11.4.1 to v12.0.0

* Thu Apr 30 2020 Daniel Muey <dan@cpanel.net> - 11.4.1-1
- EA-9048: Update scl-sourceguardian from v11.3.4 to v11.4.1

* Tue Feb 18 2020 Tim Mullin <tim@cpanel.net> - 11.3.4-2
- EA-8865: Add php-cli as a dependency

* Mon Dec 16 2019 Tim Mullin <tim@cpanel.net) - 11.3.4-1
- EA-8785: Update to v11.3.4

* Fri May 17 2019 Cory McIntire <cory@cpanel.net> - 11.3.1-1
- EA-8465: Update to v11.3, drop v11.2
  Add PHP 7.3 support
  Remove 32 bit loader

* Mon May 21 2018 Daniel Muey <dan@cpanel.net> - 11.2-1
- EA-7324: Update to v11.2, drop v11.0.6 (Add 7.1 and 7.2 support)

* Fri Dec 16 2016 Cory McIntire <cory@cpanel.net> - 11.0.6-2
- Updated Vendor field in SPEC file

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
