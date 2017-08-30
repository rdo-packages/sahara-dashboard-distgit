%global pypi_name sahara-dashboard
%global mod_name sahara_dashboard

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-sahara-ui
Version:        7.0.0
Release:        1%{?dist}
Summary:        Sahara Management Dashboard

License:        ASL 2.0
URL:            https://github.com/openstack/sahara-dashboard
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
#

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
Requires: python-django-openstack-auth >= 3.5.0
Requires: python-designateclient >= 1.5.0
Requires: python-keystoneclient >= 1:3.8.0
Requires: python-manilaclient >= 1.12.0
Requires: python-neutronclient >= 6.3.0
Requires: python-novaclient >= 1:9.0.0
Requires: python-oslo-log >= 3.22.0
Requires: python-pbr >= 2.0.0
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
* Wed Aug 30 2017 rdo-trunk <javier.pena@redhat.com> 7.0.0-1
- Update to 7.0.0

* Fri Aug 25 2017 Alfredo Moralejo <amoralej@redhat.com> 7.0.0-0.2.0rc2
- Update to 7.0.0.0rc2

* Thu Aug 24 2017 Alfredo Moralejo <amoralej@redhat.com> 7.0.0-0.1.0rc1
- Update to 7.0.0.0rc1


