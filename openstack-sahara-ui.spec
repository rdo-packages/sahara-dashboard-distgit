%global pypi_name sahara-dashboard
%global mod_name sahara_dashboard

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-sahara-ui
Version:        XXX
Release:        XXX
Summary:        Sahara Management Dashboard

License:        ASL 2.0
URL:            https://github.com/openstack/sahara-dashboard
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx
BuildRequires:  python2-oslo-sphinx
# Required to compile translation files
BuildRequires:  python2-django
BuildRequires:  gettext

Requires: python2-babel
Requires: openstack-dashboard >= 1:13.0.0
Requires: python2-django >= 1.8
Requires: python2-django-compressor >= 2.0
Requires: python2-designateclient >= 2.7.0
Requires: python2-keystoneclient >= 1:3.8.0
Requires: python2-manilaclient >= 1.16.0
Requires: python2-neutronclient >= 6.3.0
Requires: python2-novaclient >= 1:9.1.0
Requires: python2-oslo-log >= 3.36.0
Requires: python2-pbr >= 2.0.0
Requires: python2-saharaclient >= 1.4.0
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
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
pushd .
cd %{buildroot}%{python2_sitelib}/%{mod_name}/enabled
for f in _18*.py*; do
    ln -s %{buildroot}%{python2_sitelib}/%{mod_name}/enabled/${f} \
        %{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/${f}
    ln -s %{buildroot}%{python2_sitelib}/%{mod_name}/enabled/${f} \
        %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/${f}
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
%{_sysconfdir}/openstack-dashboard/enabled/_18*.py*


%changelog

