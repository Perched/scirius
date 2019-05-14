# Commit Info
%global commit f65c77aa217ce058c3fec1feca90fadf7dd94888
%global commit_count 2002
%global shortcommit %(c=%{commit}; echo ${c:0:7}) 

# Use our virtualenv python for precompiling
%global __python /opt/venvs/%{name}/bin/python

# Disable debug symbol package
%global debug_package %{nil}

%if 0%{?epel}
%define scl rh-nodejs8
%define scl_prefix rh-nodejs8-
%endif

Name:           scirius
Version:        3.2.0
Release:        0.git.%{commit_count}.%{shortcommit}%{?dist}
Summary:        Web application for Suricata ruleset management

License:        GPL3
URL:            https://scirius.readthedocs.io/en/latest/index.html
Source0:        https://github.com/StamusNetworks/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz 
Patch0:         https://github.com/StamusNetworks/scirius/compare/%{commit}...Perched:dcode/packaging.patch#/001-packaging-cleanup.patch

BuildRequires:  %{?scl_prefix}npm
BuildRequires:  python-virtualenv
BuildRequires:  python-devel
BuildRequires:  python
BuildRequires:  git

Requires:       git
Requires:       python

%systemd_requires

%description
Scirius Community Edition is a web interface dedicated to Suricata ruleset management. It handles the rules file and update associated files.

######### Define some macros #############
# Borrowed logic from https://github.com/kushaldas/rpm-macros-virtualenv
%define __pyenv %{buildroot}/opt/venvs/%{name}/bin/python2
%define __pyenvpip2 %{buildroot}/opt/venvs/%{name}/bin/pip2
%define __pyenv_root %{buildroot}/opt/venvs/%{name}

%define pyenv_create() %{expand:\\\
  mkdir -p %{buildroot}/opt/venvs/
  CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" \\\
    virtualenv %{__pyenv_root} %{?*}

  %{__pyenvpip2} install wheel $PYVENV_WHEEL_ARGS
  %{__pyenvpip2} install --upgrade pip
  %{__pyenvpip2} install --requirement requirements.txt

  sleep 1
}

%define pyenv_build() %{expand:\\\
  CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}"\\\
  %{__pyenv} %{py_setup} %{?py_setup_args} build %{?*}
  sleep 1
}

%define pyenv_install() %{expand:\\\
  %{__pyenv} %{py_setup} %{?py_setup_args} install %{?*}
  find  %{__pyenv_root} -type f -a -name '*.pyc' -delete 
  find  %{__pyenv_root} -type f -print0 | xargs -0 sed -i 's~%{buildroot}~~'
}

%prep
%autosetup -S git -n %{name}-%{commit}

## Insert packaging values for state and sysconf files
sed -i'' 's|SHAREDSTATE_DIR = .*$|SHAREDSTATE_DIR = "%{_sharedstatedir}/%{name}"|' scirius/sysconf_settings.py
sed -i'' 's|GLOBAL_CONFIG_OVERRIDE = .*$|GLOBAL_CONFIG_OVERRIDE = "%{_sysconfdir}/%{name}/settings.py"|' scirius/settings.py


%build
%pyenv_create
%pyenv_build

pwd
%{?scl:scl enable %{scl} "}
npm install
cd hunt

npm install
npm run build
pwd

cd ..
npx webpack -p --progress --env.prod

%{?scl: "}

# Build documentation
%{__pyenvpip2} install sphinx
cd doc; make html SPHINXBUILD=%{__pyenv_root}/bin/sphinx-build

%install

%pyenv_create

install -d %{buildroot}%{_sharedstatedir}/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}
install scirius/sysconf_settings.py %{buildroot}%{_sysconfdir}/%{name}/settings.py

# Install static files to static root
install -d %{buildroot}%{_localstatedir}/www/%{name}
tee -a scirius/settings.py <<EOF

STATIC_ROOT = '%{buildroot}%{_localstatedir}/www/%{name}'
EOF

%{__pyenv} manage.py collectstatic --noinput

# Copy over docs
cp -a doc/_build/html %{buildroot}%{_localstatedir}/www/%{name}/doc

# Remove local settings before installing files
rm scirius/sysconf_settings.py
sed -i'' '/^STATIC_ROOT/d' scirius/settings.py

%pyenv_install

# Create log dir 
install -d %{buildroot}%{_localstatedir}/log/%{name}
touch %{buildroot}%{_localstatedir}/log/%{name}/{access,error}.log

# Install systemd service files
install -d %{buildroot}%{_tmpfilesdir}
install -d %{buildroot}%{_unitdir}
install -d -m 0755 %{buildroot}/run/%{name}
install -m 0644 systemd/%{name}-tmpfiles.conf %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -m 0644 systemd/%{name}.service %{buildroot}%{_unitdir}/
install -m 0644 systemd/%{name}.socket  %{buildroot}%{_unitdir}/

%files
%license LICENSE
%doc README.rst

# Site specific config
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/settings.py

# Sqlite database for auth and such
%attr(0750, scirius, scirius) %{_sharedstatedir}/%{name}
%ghost %{_sharedstatedir}/%{name}/db.sqlite3

# Virtualenv
/opt/venvs/%{name}

# Static files for webserver to server
%{_localstatedir}/www/%{name}

# Log files
%dir %{_localstatedir}/log/%{name}
%attr(0750, scirius, scirius) %{_localstatedir}/log/%{name}
%ghost %{_localstatedir}/log/%{name}/*.log

# systemd files
%dir /run/%{name}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
 
%pre
getent group %{name} >/dev/null  || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin -c "%{name} service account" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog

* Mon May 13 2019 Derek Ditch <derek@perched.io> 3.1.0-1
- Initial RPM packaging
- Created split system config to allow site config from /etc/scirius/settings.py
- Moved database to /var/lib/scirius
