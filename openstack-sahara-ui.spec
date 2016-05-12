%global pypi_name sahara-dashboard
%global mod_name sahara_dashboard

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-sahara-ui
Version:        XXX
Release:        XXX
Summary:        Sahara Management Dashboard

License:        ASL 2.0
URL:            https://github.com/openstack/sahara-dashboard
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

Requires: python-babel
Requires: openstack-dashboard
Requires: python-iso8601
Requires: python-keystoneclient
Requires: python-manilaclient
Requires: python-neutronclient
Requires: python-novaclient
Requires: python-saharaclient

%description
Sahara Management Dashboard


%prep
%setup -q -n sahara-dashboard-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm test-requirements.txt

%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Move config to horizon
mkdir -p  %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
pushd .
cd %{mod_name}/enabled
for f in `ls _18*.py`
do
  mv $f %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/$f
  ln -s %{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/$f \
        %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/$f
done
popd

%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{mod_name}
%{python2_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1810_data_processing_panel_group.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1820_data_processing_clusters_panel.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1840_data_processing_jobs_panel.py*
%{_sysconfdir}/openstack-dashboard/enabled/_1810_data_processing_panel_group.py*
%{_sysconfdir}/openstack-dashboard/enabled/_1820_data_processing_clusters_panel.py*
%{_sysconfdir}/openstack-dashboard/enabled/_1840_data_processing_jobs_panel.py*


%changelog

