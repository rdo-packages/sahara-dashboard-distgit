%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815AFEC729392386480E076DCC0DFE2D21C023C9
%global pypi_name sahara-dashboard
%global mod_name sahara_dashboard

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate sphinx openstackdocstheme xvfbwrapper

Name:           openstack-sahara-ui
Version:        19.0.0
Release:        1%{?dist}
Summary:        Sahara Management Dashboard

License:        Apache-2.0
URL:            https://git.openstack.org/cgit/openstack/sahara-dashboard
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
#

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
BuildRequires:  pyproject-rpm-macros
BuildRequires:  gettext
BuildRequires:  openstack-dashboard >= 1:17.1.0

Requires: openstack-dashboard >= 1:17.1.0

%description
Sahara Management Dashboard


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n sahara-dashboard-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel


%install
%pyproject_install

# Generate i18n files
pushd %{buildroot}/%{python3_sitelib}/%{mod_name}
django-admin compilemessages
popd

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

# Missing xvfbwrapper which is needed to run unit tests
#%check
#export PYTHONPATH=.:%{buildroot}%{python3_sitearch}:%{buildroot}%{python3_sitelib}:/usr/share/openstack-dashboard/
#%%tox -e %{default_toxenv}

%files -f django.lang
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{mod_name}
%{python3_sitelib}/*.dist-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_18*.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d/_12*.py*
%{_sysconfdir}/openstack-dashboard/enabled/_18*.py*
%{_sysconfdir}/openstack-dashboard/local_settings.d/_12*.py*


%changelog
* Wed Oct 04 2023 RDO <dev@lists.rdoproject.org> 19.0.0-1
- Update to 19.0.0

* Fri Sep 15 2023 RDO <dev@lists.rdoproject.org> 19.0.0-0.1.0rc1
- Update to 19.0.0.0rc1


