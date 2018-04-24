
%define name ADEO_beapi
%define version %(git describe HEAD --tags --match "v*.*" | awk -F "-" '{if ($1 == ""){print "0.0"}else{print substr($1,2)}}')
%define serial %(git rev-parse --short HEAD)
%define release %(git describe HEAD --tags --match "v*.*" | awk -F "-" '{if ($2 == ""){print "0"}else{print $2}}').%{serial}

%define api beapi
%define dir_api "/usr/local/beapi"
%define desc "beapi"

%define __os_install_post %{nil}


%define packager               Laurent Licour
%define vendor                 ADEO
%define distribution           ADEO Services
%define debug_package          %{nil}


Summary: %{desc}
Name: %{name}
Version: %{version}
Release: %{release}
Source0: app.zip

License: ADEO - GIT
Group: -
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildArch: noarch
Conflicts: %{name} < %{version}-%{release}
Requires: httpd, mod_ssl, mod_wsgi, python, python-virtualenv, gcc
Requires: tmpwatch, logrotate

AutoReqProv: no


%package conf-default
Summary: %{desc} configuration for default environment
Requires: %{name} = %{version}-%{release}
Conflicts: %{name}-conf-recette, %{name}-conf-preprod, %{name}-conf-prod

#%package conf-recette
#Summary: %{desc} configuration for recette environment
#Requires: %{name} = %{version}-%{release}
#Conflicts: %{name}-conf-preprod, %{name}-conf-prod

#%package conf-preprod
#Summary: %{desc} configuration for preproduction environment
#Requires: %{name} = %{version}-%{release}
#Conflicts: %{name}-conf-recette, %{name}-conf-prod

#%package conf-prod
#Summary: %{desc} configuration for production environment
#Requires: %{name} = %{version}-%{release}
#Conflicts: %{name}-conf-recette, %{name}-conf-preprod

%description
%{desc} Core engine

%description conf-default
%{desc} configuration for default environment

#%description conf-recette
#%{desc} configuration for recette environment

#%description conf-preprod
#%{desc} configuration for preproduction environment

#%description conf-prod
#%{desc} configuration for production environment


%prep
if [ -d $RPM_BUILD_ROOT ]; then
   rm -rf $RPM_BUILD_ROOT
fi
mkdir -p $RPM_BUILD_ROOT


%build


%install
mkdir -p $RPM_BUILD_ROOT/
mkdir -p $RPM_BUILD_ROOT/etc/cron.d
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
mkdir -p $RPM_BUILD_ROOT/%{dir_api}
unzip %{SOURCE0} -d $RPM_BUILD_ROOT/%{dir_api}

# generic flaskit MCO files
mv $RPM_BUILD_ROOT/%{dir_api}/contrib/%{api}_purge $RPM_BUILD_ROOT/etc/cron.d/
mv $RPM_BUILD_ROOT/%{dir_api}/contrib/%{api}.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/%{api}

# ghost file
touch ${RPM_BUILD_ROOT}/etc/httpd/conf.d/%{api}.conf

# remove unused content
rm -f $RPM_BUILD_ROOT/%{dir_api}/env/%{api}.default/config.cfg.sample
rm -f $RPM_BUILD_ROOT/%{dir_api}/install/Dockerfile
rm -f $RPM_BUILD_ROOT/%{dir_api}/install/docker_build
rm -f $RPM_BUILD_ROOT/%{dir_api}/install/%{api}.spec

# remove generated doc
rm -rf $RPM_BUILD_ROOT/%{dir_api}/doc/classes
rm -rf $RPM_BUILD_ROOT/%{dir_api}/doc/schemas

%clean
rm -rf $RPM_BUILD_ROOT


#			install		upgrade		uninstall
#%pretrans	$1 == 0		$1 == 0		(N/A)
#%pre		$1 == 1		$1 == 2		(N/A)
#%post		$1 == 1		$1 == 2		(N/A)
#%preun		(N/A)		$1 == 1		$1 == 0
#%postun	(N/A)		$1 == 1		$1 == 0
#%posttrans	$1 == 0		$1 == 0		(N/A)

#use :
#if [ $1 = 2 ]
#then
#echo 
#fi


%pre
# refuse to install on a dev host
if [ -d %{dir_api}/.git ]; then
  echo "Error : Seems to be a developpement environment (git initialized on %{dir_api})"
  exit 1
fi

%pre conf-default
if [ -d %{dir_api}/.git ]; then
  echo "Error : Seems to be a developpement environment (git initialized on %{dir_api})"
  exit 1
fi

#%pre conf-recette
#if [ -d %{dir_api}/.git ]; then
#  echo "Error : Seems to be a developpement environment (git initialized on %{dir_api})"
#  exit 1
#fi

#%pre conf-preprod
#if [ -d %{dir_api}/.git ]; then
#  echo "Error : Seems to be a developpement environment (git initialized on %{dir_api})"
#  exit 1
#fi

#%pre conf-prod
#if [ -d %{dir_api}/.git ]; then
#  echo "Error : Seems to be a developpement environment (git initialized on %{dir_api})"
#  exit 1
#fi


%post
DIRLOG=/home3/%{api}
mkdir -p ${DIRLOG}/log
chown -R apache ${DIRLOG}

# install/update virtualenv
cd %{dir_api}
install/flaskit_mkvenv > /dev/null

# last command should return 0 (not the case with an if in last command)
true

%post conf-default
if [ $1 = 1 ]; then # install
  ln -sf %{dir_api}/env/%{api}.default/httpd.conf /etc/httpd/conf.d/%{api}.conf
  /bin/systemctl restart httpd.service
  /bin/systemctl enable httpd
else  # soft reload
  touch %{dir_api}/venv/bin/flaskit_launcher.py
fi

#%post conf-recette
#if [ $1 = 1 ]; then # install
#  ln -sf %{dir_api}/env/%{api}.recette/httpd.conf /etc/httpd/conf.d/%{api}.conf
#  /bin/systemctl restart httpd.service
#  /bin/systemctl enable httpd
#else  # soft reload
#  touch %{dir_api}/venv/bin/flaskit_launcher.py
#fi

#%post conf-preprod
#if [ $1 = 1 ]; then # install
#  ln -sf %{dir_api}/env/%{api}.preprod/httpd.conf /etc/httpd/conf.d/%{api}.conf
#  /bin/systemctl restart httpd.service
#  /bin/systemctl enable httpd
#else  # soft reload
#  touch %{dir_api}/venv/bin/flaskit_launcher.py
#fi

#%post conf-prod
#if [ $1 = 1 ]; then # install
#  ln -sf %{dir_api}/env/%{api}.prod/httpd.conf /etc/httpd/conf.d/%{api}.conf
#  /bin/systemctl restart httpd.service
#  /bin/systemctl enable httpd
#else  # soft reload
#  touch %{dir_api}/venv/bin/flaskit_launcher.py
#fi

%preun


%postun
# uninstall
if [ $1 = 0 ]; then
  # remove virtualenv
  rm -rf %{dir_api}/venv
fi

%postun conf-default
# uninstall
if [ $1 = 0 ]; then
  rm -f /etc/httpd/conf.d/%{api}.conf
  /bin/systemctl restart httpd.service
fi

#%postun conf-recette
## uninstall
#if [ $1 = 0 ]; then
#  rm -f /etc/httpd/conf.d/%{api}.conf
#  /bin/systemctl restart httpd.service
#fi

#%postun conf-preprod
## uninstall
#if [ $1 = 0 ]; then
#  rm -f /etc/httpd/conf.d/%{api}.conf
#  /bin/systemctl restart httpd.service
#fi

#%postun conf-prod
## uninstall
#if [ $1 = 0 ]; then
#  rm -f /etc/httpd/conf.d/%{api}.conf
#  /bin/systemctl restart httpd.service
#fi

%files
%defattr(0644,root,root,0755)
%dir /usr/local/beapi
%dir /usr/local/beapi/env
%dir /usr/local/beapi/resources
%dir /usr/local/beapi/conf
%dir /usr/local/beapi/conf/auth.d
%dir /usr/local/beapi/conf/dynrules.d
%dir /usr/local/beapi/def
%dir /usr/local/beapi/def/apis
%dir /usr/local/beapi/def/routes
%dir /usr/local/beapi/def/schemas
%dir /usr/local/beapi/def/schemas/include
%dir /usr/local/beapi/install
/usr/local/beapi/conf/auth.d/health.xml
/usr/local/beapi/conf/dynrules.d/readme.txt
/usr/local/beapi/def/apis/HealthGet.json
/usr/local/beapi/def/routes/health.json
/usr/local/beapi/def/schemas/HealthGet.schema.json
%attr(0755,root,root) /usr/local/beapi/install/flaskit_mkvenv
/usr/local/beapi/install/requirement.txt
/usr/local/beapi/resources/__init__.py
/usr/local/beapi/resources/health.py
/etc/logrotate.d/%{api}
/etc/cron.d/%{api}_purge

%files conf-default
%defattr(0644,root,root,0755)
%dir /usr/local/beapi/env/%{api}.default
%config(noreplace) /usr/local/beapi/env/%{api}.default/config.cfg
%config(noreplace) /usr/local/beapi/env/%{api}.default/httpd.conf
%ghost /etc/httpd/conf.d/%{api}.conf

#%files conf-recette
#%defattr(0644,root,root,0755)
#%dir /usr/local/beapi/env/%{api}.recette
#%config(noreplace) /usr/local/beapi/env/%{api}.recette/config.cfg
#%config(noreplace) /usr/local/beapi/env/%{api}.recette/httpd.conf
#%ghost /etc/httpd/conf.d/%{api}.conf

#%files conf-preprod
#%defattr(0644,root,root,0755)
#%dir /usr/local/beapi/env/%{api}.preprod
#%config(noreplace) /usr/local/beapi/env/%{api}.preprod/config.cfg
#%config(noreplace) /usr/local/beapi/env/%{api}.preprod/httpd.conf
#%ghost /etc/httpd/conf.d/%{api}.conf

#%files conf-prod
#%defattr(0644,root,root,0755)
#%dir /usr/local/beapi/env/%{api}.prod
#%config(noreplace) /usr/local/beapi/env/%{api}.prod/config.cfg
#%config(noreplace) /usr/local/beapi/env/%{api}.prod/httpd.conf
#%ghost /etc/httpd/conf.d/%{api}.conf


%changelog
* Thu Jun 09 2016 Laurent Licour <laurent.licour@ext.adeo.com> 1.0-0
- initial packaging