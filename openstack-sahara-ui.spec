%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global pypi_name sahara-dashboard
%global mod_name sahara_dashboard

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-sahara-ui
Version:        XXX
Release:        XXX
Summary:        Sahara Management Dashboard

License:        ASL 2.0
URL:            https://git.openstack.org/cgit/openstack/sahara-dashboard
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx
# Required to compile translation files
BuildRequires:  python3-django >= 1.11
BuildRequires:  gettext

Requires: python3-babel
Requires: openstack-dashboard >= 1:17.1.0
Requires: python3-designateclient >= 2.7.0
Requires: python3-keystoneauth1 >= 3.8.0
Requires: python3-keystoneclient >= 1:3.22.0
Requires: python3-manilaclient >= 1.16.0
Requires: python3-neutronclient >= 6.7.0
Requires: python3-novaclient >= 1:9.1.0
Requires: python3-oslo-log >= 3.36.0
Requires: python3-pbr >= 2.0.0
Requires: python3-saharaclient >= 2.2.0
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-pytz


%description
Sahara Management Dashboard


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%setup -q -n sahara-dashboard-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm test-requirements.txt

%build
%{py3_build}
# Generate i18n files
pushd build/lib/%{mod_name}
django-admin compilemessages
popd


%install
%{py3_install}

# Move config to horizon
mkdir -p  %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled
mkdir -p  %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings.d
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d
# link enabled/* entries
pushd %{buildroot}%{python3_sitelib}/%{mod_name}/enabled
for f in _18*.py*; do
    ln -s %{python3_sitelib}/%{mod_name}/enabled/${f} \
        %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/${f}
    ln -s %{python3_sitelib}/%{mod_name}/enabled/${f} \
        %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/${f}
done
popd
# link local_settings.d/* entries
pushd %{buildroot}%{python3_sitelib}/%{mod_name}/local_settings.d
for f in _12*.py*; do
    ln -s %{python3_sitelib}/%{mod_name}/local_settings.d/${f} \
        %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d/${f}
    ln -s %{python3_sitelib}/%{mod_name}/local_settings.d/${f} \
        %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings.d/${f}
done
popd
# Remove .po and .pot (they are not required)
rm -f %{buildroot}%{python3_sitelib}/%{mod_name}/locale/*/LC_*/django*.po
rm -f %{buildroot}%{python3_sitelib}/%{mod_name}/locale/*pot

# Find language files
%find_lang django --all-name

%files -f django.lang
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{mod_name}
%{python3_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_18*.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d/_12*.py*
%{_sysconfdir}/openstack-dashboard/enabled/_18*.py*
%{_sysconfdir}/openstack-dashboard/local_settings.d/_12*.py*


%changelog

