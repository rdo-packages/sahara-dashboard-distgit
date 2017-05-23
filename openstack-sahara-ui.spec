%global pypi_name sahara-dashboard
%global mod_name sahara_dashboard

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-sahara-ui
Version:        4.1.2
Release:        1%{?dist}
Summary:        Sahara Management Dashboard

License:        ASL 2.0
URL:            https://github.com/openstack/sahara-dashboard
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
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
* Tue May 23 2017 Alfredo Moralejo <amoralej@redhat.com> 4.1.2-1
- Update to 4.1.2

* Thu May 26 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 4.0.0-3
- Fix symlinks

* Fri Apr 22 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 4.0.0-2
- Create symlinks for bytecode files

* Wed Apr 13 2016 haikel <haikel@zangetsu> - 4.0.0-1
- Initial package (based on Ethan Gafford work)

