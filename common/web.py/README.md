# Setup Amazon EC2

For AMI image, choose 'Ubuntu Server 12.04.1 LTS'. Attche one Elastic IP address to this instance, and remember to download key pair for SSH login. When the state of the instance is running:

```bash
# login to the instance by SSH
ssh -i {{ key pair name }}.pem ubuntu@{{ Elastic IP Address }}

sudo apt-get update
sudo apt-get install libapache2-mod-wsgi
sudo apt-get install python-setuptools
sudo apt-get install python-pip
sudo pip install web.py
sudo pip install jinja2
sudo apt-get install git-all
sudo apt-get install gettext
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs
sudo npm install -g grunt-cli
```

References:

1. <a href="http://www.theroadtosiliconvalley.com/technology/setup-django-modwsgi-apache-ubuntu/">How to setup Django + mod_wsgi on Apache & Ubuntu</a>

2. <a href="http://webpy.org/install">Install guide (web.py)</a>

3. <a href="http://library.linode.com/web-servers/apache/installation/ubuntu-12.04-precise-pangolin">Apache 2 Web Server on Ubuntu 12.04 LTS (Precise Pangolin)</a>

# Config Apache2 & Domains & Sub-Domains

Associate naked domains and sundomains to one EC2 instance. See references for domain and sub-domains setup.

Then edit <em><strong>/etc/apache2/sites-available/default</strong></em>, the following is sample config:
```xml
NameVirtualHost *:80

<VirtualHost *:80>
        ServerName      {{ domain_name }}
        ServerAlias     www.{{ domain_name }}
        ServerAdmin     {{ email }}
        DocumentRoot    /var/www/{{ domain_name }}/htdocs
        ErrorLog        /var/www/{{ domain_name }}/logs/error_log
        CustomLog       /var/www/{{ domain_name }}/logs/access_log combined
</VirtualHost>

<VirtualHost *:80>
        ServerName      {{ sub_domain }}.{{ domain_name }}
        ServerAdmin     {{ email }}
        DocumentRoot    /var/www/{{ sub_domain }}.{{ domain_name }}/htdocs
        ErrorLog        /var/www/{{ sub_domain }}.{{ domain_name }}/logs/error_log
        CustomLog       /var/www/{{ sub_domain }}.{{ domain_name }}/logs/access_log combined

        WSGIScriptAlias / /var/www/{{ sub_domain }}.{{ domain_name }}/htdocs/code.py
</VirtualHost>
```

References:

1. <a href="http://serverfault.com/questions/155624/how-to-create-subdomains-apache2">How to create subdomains ' apache2 '?</a>

2. <a href="http://library.linode.com/web-servers/apache/mod-wsgi/ubuntu-12.04-precise-pangolin">Apache and mod_wsgi on Ubuntu 12.04 (Precise Pangolin)</a>

3. <a href="http://stackoverflow.com/questions/4203580/creating-subdomains-in-amazon-ec2">Creating subdomains in Amazon EC2</a>

# Add Users in EC2

References:

1. <a href="http://thekeesh.com/2011/05/setting-up-user-accounts-password-authentication-and-ssh-keys-on-a-new-ec2-instance/">Setting up User Accounts, Password Authentication, and SSH Keys on a New EC2 Instance</a>

2. <a href="http://utkarshsengar.com/2011/01/manage-multiple-accounts-on-1-amazon-ec2-instance/">Manage multiple Linux Users on 1 Amazon EC2 Instance</a>

