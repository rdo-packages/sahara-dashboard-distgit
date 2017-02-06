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
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
# Required to compile translation files
BuildRequires:  python-django
BuildRequires:  gettext

Requires: python-babel
Requires: openstack-dashboard
Requires: python-django >= 1.8
Requires: python-django-compressor >= 2.0
Requires: python-django-openstack-auth >= 3.1.0
Requires: python-iso8601
Requires: python-designateclient >= 1.5.0
Requires: python-keystoneclient >= 1:3.8.0
Requires: python-manilaclient >= 1.12.0
Requires: python-neutronclient >= 5.1.0
Requires: python-novaclient >= 1:6.0.0
Requires: python-oslo-log >= 3.11.0
Requires: python-pbr >= 1.8
Requires: python-saharaclient >= 1.1.0
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
    mv ${f} %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/
done
popd

for f in %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_18*.py*; do
    filename=`basename $f`
    ln -s %{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/${filename} \
        %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/${filename}
done
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

# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/sahara-dashboard/commit/?id=b4e06bdba853c24488f77bd5f9d10decbfa99e85
