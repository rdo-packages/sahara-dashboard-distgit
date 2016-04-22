# Turn off the brp-python-bytecompile script
#%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%global pypi_name sahara-dashboard
%global mod_name sahara_dashboard

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-sahara-ui
Version:        4.0.0
Release:        2%{?dist}
Summary:        Sahara Management Dashboard

License:        ASL 2.0
URL:            https://github.com/openstack/sahara-dashboard
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
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
for f in sahara_dashboard/enabled/_18*.py;do
cp -a $f  %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/
done


for f in %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/*.py*; do
filename=`basename $f`
ln -s %{_sysconfdir}/openstack-dashboard/enabled/$filename %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/$filename
ln -s %{_sysconfdir}/openstack-dashboard/enabled/${filename}o %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/${filename}o
ln -s %{_sysconfdir}/openstack-dashboard/enabled/${filename}c %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/${filename}c
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
* Fri Apr 22 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 4.0.0-2
- Create symlinks for bytecode files

* Wed Apr 13 2016 haikel <haikel@zangetsu> - 4.0.0-1
- Initial package (based on Ethan Gafford work)

