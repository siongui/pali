# Run Dictionary and Tipitaka Websites on Amazon Web Services

## Setup Amazon EC2

For AMI image, choose 'Ubuntu Server 12.04.1 LTS'. Attche one Elastic IP address to this instance, and remember to download key pair for SSH login. When the state of the instance is running:

## Install Packages

```bash
# login to the instance by SSH
ssh -i {{ key pair name }}.pem ubuntu@{{ Elastic IP Address }}

# upgrade system
sudo apt-get update

# install apache2 and mod_wsgi
sudo apt-get install libapache2-mod-wsgi

# install tool for installing and managing Python packages.
sudo apt-get install python-setuptools
sudo apt-get install python-pip

# install python server-side library to run website.
sudo pip install web.py
sudo pip install jinja2
sudo apt-get install python-lxml

# install git
sudo apt-get install git-all

# install tools for i18n
sudo apt-get install gettext

# install latest version of nodejs
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs

# install grunt
sudo npm install -g grunt-cli
```

References:

1. [How to setup Django + mod_wsgi on Apache & Ubuntu](http://www.theroadtosiliconvalley.com/technology/setup-django-modwsgi-apache-ubuntu/)
2. [Install guide (web.py)](http://webpy.org/install)
3. [Apache 2 Web Server on Ubuntu 12.04 LTS (Precise Pangolin)](http://library.linode.com/web-servers/apache/installation/ubuntu-12.04-precise-pangolin)

## Follow README to Setup Websites (to be updated)

## Config Apache2 & Domains & Sub-Domains

Associate naked domains and sundomains to one EC2 instance. See references for domain and sub-domains setup.

Then edit <em><strong>/etc/apache2/sites-available/default</strong></em>, the following is the sample config for dictionary website:
```xml
<VirtualHost *:80>
        ServerName      dictionary.online-dhamma.net
        ServerAdmin     {{ email }}
        DocumentRoot    {{ SOME_DIR }}/htdocs
        ErrorLog        {{ SOME_DIR }}/logs/error_log
        CustomLog       {{ SOME_DIR }}/logs/access_log combined

        Alias           /js/palidic.js {{ PALI_REPO_DIR }}/app/all_compiled.js
        Alias           /favicon.ico {{ PALI_REPO_DIR }}/common/app/img/favicon.ico
        Alias           /robots.txt {{ PALI_REPO_DIR }}/common/gae/robots.txt
        Alias           /wordJson/ {{ PALI_REPO_DIR }}/gaelibs/paliwords/

        WSGIScriptAlias / {{ PALI_REPO_DIR }}/mainweb.py

        AddType         text/html .py
</VirtualHost>
```

References:

1. [How to create subdomains ' apache2 '?](http://serverfault.com/questions/155624/how-to-create-subdomains-apache2)
2. [Apache and mod_wsgi on Ubuntu 12.04 (Precise Pangolin)](http://library.linode.com/web-servers/apache/mod-wsgi/ubuntu-12.04-precise-pangolin)
3. [Creating subdomains in Amazon EC2](http://stackoverflow.com/questions/4203580/creating-subdomains-in-amazon-ec2)

## Add Users in EC2

References:

1. [Setting up User Accounts, Password Authentication, and SSH Keys on a New EC2 Instance](http://thekeesh.com/2011/05/setting-up-user-accounts-password-authentication-and-ssh-keys-on-a-new-ec2-instance/)
2. [Manage multiple Linux Users on 1 Amazon EC2 Instance](http://utkarshsengar.com/2011/01/manage-multiple-accounts-on-1-amazon-ec2-instance/)

