===================
Deploy on AWS_ EC2_
===================

Deployment Environment
++++++++++++++++++++++

  - AWS_ EC2_ t2.nano_
  - `Ubuntu 14.04 LTS`_
  - `Apache-2.4`_

Setup
+++++

1. Login to t2.nano_ running `Ubuntu 14.04 LTS`_:

   .. code-block:: sh

      # login to the instance by SSH
      $ ssh -i {{ key pair name }}.pem ubuntu@{{ Elastic IP Address }}

2. Install necessary packages:

   .. code-block:: sh

      # upgrade system
      $ sudo apt-get update
      $ sudo apt-get upgrade

      # install apache2 and mod_wsgi
      $ sudo apt-get install apache2 libapache2-mod-wsgi

      # install python server-side library to run website
      $ sudo apt-get install python-webpy
      $ sudo apt-get install python-jinja2
      $ sudo apt-get install python-lxml

      # install offline tools
      $ sudo apt-get install vim
      $ sudo apt-get install git
      $ sudo apt-get install gettext
      $ sudo apt-get install make
      $ sudo apt-get install opencc

3. Download_ Go_:

   .. code-block:: sh

     # run as user *ubuntu*
     # create a workspace in your home directory
     $ mkdir ~/dev
     # enter workspace
     $ cd ~/dev
     # download Go 1.6.2 for Linux 64-bit
     $ wget https://storage.googleapis.com/golang/go1.6.2.linux-amd64.tar.gz
     # uncompress and untar
     $ tar xvzf go1.6.2.linux-amd64.tar.gz

   If you do not follow the above steps, please modify ``GOROOT`` and ``GOPATH``
   in `Makefile <Makefile>`_.

4. `git clone`_ the `pali repository`_ and `data repository`_:

   .. code-block:: sh

     # git clone pali repository
     $ cd ~/dev
     $ git clone https://github.com/siongui/pali.git
     # enter pali repository
     $ cd ~/dev/pali
     # git clone data repository
     $ make clone

5. Development environment setup:

   .. code-block:: sh

     $ cd ~/dev/pali
     $ make ec2setup

6. Build Dictionary Website:

   .. code-block:: sh

     $ cd ~/dev/pali
     $ make mindicjs
     $ make mindiccss

     # edit dictionary/mainweb.py
     # change serverEnv, tpkWebAppUrl, dicWebAppUrl

7. Build Tipiṭaka Website:

   .. code-block:: sh

     $ cd ~/dev/pali
     $ make mintpkjs
     $ make mintpkcss

     # edit tipitaka/mainweb.py
     # change serverEnv, tpkWebAppUrl, dicWebAppUrl

8. Edit apache2 config file (`/etc/apache2/sites-available/000-default.conf`):

   .. code-block:: sh

      WSGIPythonPath	/home/ubuntu/dev/pali/tipitaka
      <VirtualHost *:80>
	ServerName	tipitaka.sutta.org
	ServerAdmin	siongui@gmail.com
	ErrorLog	/home/ubuntu/logs/error_log
	CustomLog	/home/ubuntu/logs/access_log combined

	Alias		/js/tipitaka.js /home/ubuntu/dev/pali/tipitaka/app/all_compiled.js
	Alias		/favicon.ico /home/ubuntu/dev/pali/tipitaka/app/favicon.ico
	Alias		/robots.txt /home/ubuntu/dev/pali/common/robots.txt
	Alias		/wordJson/ /home/ubuntu/dev/pali/dictionary/pylib/paliwords/

	WSGIScriptAlias	/ /home/ubuntu/dev/pali/tipitaka/devNotGaeRun.py

	AddType		text/html .py

	<Directory />
		Require all granted
	</Directory>
      </VirtualHost>
      <VirtualHost *:80>
	ServerName	dictionary.sutta.org
	ServerAdmin	siongui@gmail.com
	ErrorLog	/home/ubuntu/logs/dic_error_log
	CustomLog	/home/ubuntu/logs/dic_access_log combined

	Alias		/js/palidic.js /home/ubuntu/dev/pali/dictionary/app/all_compiled.js
	Alias		/favicon.ico /home/ubuntu/dev/pali/dictionary/app/favicon.ico
	Alias		/robots.txt /home/ubuntu/dev/pali/common/robots.txt
	Alias		/wordJson/ /home/ubuntu/dev/pali/dictionary/pylib/paliwords/

	WSGIScriptAlias	/ /home/ubuntu/dev/pali/dictionary/mainweb.py

	AddType		text/html .py

	<Directory />
		Require all granted
	</Directory>
      </VirtualHost>

   Create *logs* directory:

   .. code-block:: sh

      $ mkdir ~/logs

   Restart apache2:

   .. code-block:: sh

      $ sudo service apache2 restart
      # or
      $ sudo /etc/init.d/apache2 restart


References
++++++++++

.. [1] `[AWS] Create/Migrate Linux Users on Amazon EC2 <https://siongui.github.io/2016/04/30/aws-create-or-migrate-linux-users-on-ec2/>`_

.. [2] `Apache Web Server on Ubuntu 14.04 LTS <https://www.linode.com/docs/websites/apache/apache-web-server-on-ubuntu-14-04>`_

.. [3] `Apache and mod_wsgi on Ubuntu 14.04 (Trusty Tahr) <https://www.linode.com/docs/websites/apache/apache-and-modwsgi-on-ubuntu-14-04-precise-pangolin>`_


.. _AWS: https://aws.amazon.com/
.. _EC2: https://aws.amazon.com/ec2/
.. _t2.nano: https://aws.amazon.com/blogs/aws/ec2-update-t2-nano-instances-now-available/
.. _Ubuntu 14.04 LTS: https://aws.amazon.com/marketplace/pp/B00JV9TBA6/
.. _Apache-2.4: https://httpd.apache.org/docs/2.4/
.. _Download: https://golang.org/dl/
.. _Go: https://golang.org/
.. _git clone: https://www.google.com/search?q=git+clone
.. _pali repository: https://github.com/siongui/pali
.. _data repository: https://github.com/siongui/data
