%global pypi_name sahara-dashboard
%global mod_name sahara_dashboard

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-sahara-ui
Version:        9.0.2
Release:        1%{?dist}
Summary:        Sahara Management Dashboard

License:        ASL 2.0
URL:            https://git.openstack.org/cgit/openstack/sahara-dashboard
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
#

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-pbr >= 2.0.0
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx
BuildRequires:  python2-oslo-sphinx
# Required to compile translation files
BuildRequires:  python2-django >= 1.11
BuildRequires:  gettext

Requires: python2-babel
Requires: openstack-dashboard >= 1:14.0.0
Requires: python2-django >= 1.11
Requires: python2-django-compressor >= 2.0
Requires: python2-designateclient >= 2.7.0
Requires: python2-keystoneauth1 >= 3.4.0
Requires: python2-keystoneclient >= 1:3.15.0
Requires: python2-manilaclient >= 1.16.0
Requires: python2-neutronclient >= 6.7.0
Requires: python2-novaclient >= 1:9.1.0
Requires: python2-oslo-log >= 3.36.0
Requires: python2-pbr >= 2.0.0
Requires: python2-saharaclient >= 2.0.0
Requires: python2-oslo-serialization >= 2.18.0
Requires: pytz


%description
Sahara Management Dashboard


%prep
%setup -q -n sahara-dashboard-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm test-requirements.txt

%build
%{__python2} setup.py build
# Generate i18n files
pushd build/lib/%{mod_name}
django-admin compilemessages
popd


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Move config to horizon
mkdir -p  %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled
mkdir -p  %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings.d
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d
# link enabled/* entries
pushd %{buildroot}%{python2_sitelib}/%{mod_name}/enabled
for f in _18*.py*; do
    ln -s %{python2_sitelib}/%{mod_name}/enabled/${f} \
        %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/${f}
    ln -s %{python2_sitelib}/%{mod_name}/enabled/${f} \
        %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/${f}
done
popd
# link local_settings.d/* entries
pushd %{buildroot}%{python2_sitelib}/%{mod_name}/local_settings.d
for f in _12*.py*; do
    ln -s %{python2_sitelib}/%{mod_name}/local_settings.d/${f} \
        %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d/${f}
    ln -s %{python2_sitelib}/%{mod_name}/local_settings.d/${f} \
        %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings.d/${f}
done
popd
# Remove .po and .pot (they are not required)
rm -f %{buildroot}%{python2_sitelib}/%{mod_name}/locale/*/LC_*/django*.po
rm -f %{buildroot}%{python2_sitelib}/%{mod_name}/locale/*pot
 
# Find language files
%find_lang django --all-name

%files -f django.lang
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{mod_name}
%{python2_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_18*.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d/_12*.py*
%{_sysconfdir}/openstack-dashboard/enabled/_18*.py*
%{_sysconfdir}/openstack-dashboard/local_settings.d/_12*.py*


%changelog
* Wed Jan 29 2020 RDO <dev@lists.rdoproject.org> 9.0.2-1
- Update to 9.0.2

* Tue Jan 15 2019 RDO <dev@lists.rdoproject.org> 9.0.1-1
- Update to 9.0.1

* Thu Aug 30 2018 RDO <dev@lists.rdoproject.org> 9.0.0-1
- Update to 9.0.0

* Thu Aug 23 2018 RDO <dev@lists.rdoproject.org> 9.0.0-0.2.0rc1
- Update to 9.0.0.0rc2

* Tue Aug 21 2018 RDO <dev@lists.rdoproject.org> 9.0.0-0.1.0rc1
- Update to 9.0.0.0rc1


