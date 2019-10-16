# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global pypi_name sahara-dashboard
%global mod_name sahara_dashboard

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-sahara-ui
Version:        11.0.0
Release:        1%{?dist}
Summary:        Sahara Management Dashboard

License:        ASL 2.0
URL:            https://git.openstack.org/cgit/openstack/sahara-dashboard
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
#

BuildArch:      noarch

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr >= 2.0.0
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-oslo-sphinx
# Required to compile translation files
BuildRequires:  python%{pyver}-django >= 1.11
BuildRequires:  gettext

Requires: python%{pyver}-babel
Requires: openstack-dashboard >= 1:14.0.0
Requires: python%{pyver}-django >= 1.11
Requires: python%{pyver}-django-compressor >= 2.0
Requires: python%{pyver}-designateclient >= 2.7.0
Requires: python%{pyver}-keystoneauth1 >= 3.4.0
Requires: python%{pyver}-keystoneclient >= 1:3.15.0
Requires: python%{pyver}-manilaclient >= 1.16.0
Requires: python%{pyver}-neutronclient >= 6.7.0
Requires: python%{pyver}-novaclient >= 1:9.1.0
Requires: python%{pyver}-oslo-log >= 3.36.0
Requires: python%{pyver}-pbr >= 2.0.0
Requires: python%{pyver}-saharaclient >= 2.2.0
Requires: python%{pyver}-oslo-serialization >= 2.18.0
Requires: python%{pyver}-pytz


%description
Sahara Management Dashboard


%prep
%setup -q -n sahara-dashboard-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm test-requirements.txt

%build
%{pyver_build}
# Generate i18n files
pushd build/lib/%{mod_name}
django-admin compilemessages
popd


%install
%{pyver_install}

# Move config to horizon
mkdir -p  %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled
mkdir -p  %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings.d
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d
# link enabled/* entries
pushd %{buildroot}%{pyver_sitelib}/%{mod_name}/enabled
for f in _18*.py*; do
    ln -s %{pyver_sitelib}/%{mod_name}/enabled/${f} \
        %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/${f}
    ln -s %{pyver_sitelib}/%{mod_name}/enabled/${f} \
        %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/${f}
done
popd
# link local_settings.d/* entries
pushd %{buildroot}%{pyver_sitelib}/%{mod_name}/local_settings.d
for f in _12*.py*; do
    ln -s %{pyver_sitelib}/%{mod_name}/local_settings.d/${f} \
        %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d/${f}
    ln -s %{pyver_sitelib}/%{mod_name}/local_settings.d/${f} \
        %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings.d/${f}
done
popd
# Remove .po and .pot (they are not required)
rm -f %{buildroot}%{pyver_sitelib}/%{mod_name}/locale/*/LC_*/django*.po
rm -f %{buildroot}%{pyver_sitelib}/%{mod_name}/locale/*pot
 
# Find language files
%find_lang django --all-name

%files -f django.lang
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{mod_name}
%{pyver_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_18*.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d/_12*.py*
%{_sysconfdir}/openstack-dashboard/enabled/_18*.py*
%{_sysconfdir}/openstack-dashboard/local_settings.d/_12*.py*


%changelog
* Wed Oct 16 2019 RDO <dev@lists.rdoproject.org> 11.0.0-1
- Update to 11.0.0

* Mon Sep 30 2019 RDO <dev@lists.rdoproject.org> 11.0.0-0.1.0rc1
- Update to 11.0.0.0rc1


