=======================================
`Pāli Dictionary`_ and `Pāli Tipiṭaka`_
=======================================

Development Environment:

  - `Ubuntu 15.10`_
  - `Python 2.7.10`_
  - `Go 1.6`_

Set Up Development Environment
++++++++++++++++++++++++++++++

1. Download Go_:

   .. code-block:: bash

     # create a workspace in your home directory
     $ mkdir ~/dev
     # enter workspace
     $ cd ~/dev
     # download Go 1.6 for Linux 64-bit
     $ wget https://storage.googleapis.com/golang/go1.6.linux-amd64.tar.gz
     # uncompress and untar
     $ tar xvzf go1.6.linux-amd64.tar.gz

   If you do not follow the above steps, please modify ``GOROOT`` and ``GOPATH``
   in `Makefile <Makefile>`_.

2. `git clone`_ the `pali repository`_ and `data repository`_:

   .. code-block:: bash

     # git clone pali repository
     $ cd ~/dev
     $ git clone https://github.com/siongui/pali.git
     # enter pali repository
     $ cd ~/dev/pali
     # git clone data repository
     $ make clone

3. Development environment setup:

   .. code-block:: bash

     $ cd ~/dev/pali
     $ make setup

4. Run Dictionary Dev Website:

   .. code-block:: bash

     $ cd ~/dev/pali
     $ make mindicjs
     $ make mindiccss
     $ make dicdevserver


UNLICENSE
+++++++++

Released in public domain. See UNLICENSE_.


References
++++++++++

.. [1] `GitHub - siongui/pali: Pāḷi Tipiṭaka and Pāḷi Dictionaries <https://github.com/siongui/pali>`_

.. [2] `siongui/data: Data files for Pāḷi Tipiṭaka, Pāḷi Dictionaries, and external libraries <https://github.com/siongui/data>`_

.. [3] `apt-get upgrade vs update <https://www.google.com/search?q=apt-get+upgrade+vs+update>`_

       `What is the difference between apt-get update and upgrade? - Ask Ubuntu <http://askubuntu.com/questions/94102/what-is-the-difference-between-apt-get-update-and-upgrade>`_

.. [4] `ubuntu check package version <https://www.google.com/search?q=ubuntu+check+package+version>`_

       `How can I check the available version of a package in the repositories? - Ask Ubuntu <http://askubuntu.com/questions/340530/how-can-i-check-the-available-version-of-a-package-in-the-repositories>`_

.. [5] `ubuntu check if packages are installed <https://www.google.com/search?q=ubuntu+check+if+packages+are+installed>`_

       `How do I check if a package is installed on my server? - Ask Ubuntu <http://askubuntu.com/questions/423355/how-do-i-check-if-a-package-is-installed-on-my-server>`_

.. [6] `python pip vs apt-get <https://www.google.com/search?q=python+pip+vs+apt-get>`_

.. [7] `How to extract files to another directory using 'tar' command? - Ask Ubuntu <http://askubuntu.com/questions/45349/how-to-extract-files-to-another-directory-using-tar-command>`_

.. [8] `Git Workflows and Tutorials | Atlassian Git Tutorial <https://www.atlassian.com/git/tutorials/comparing-workflows/>`_

.. [9] `makefile instead of grunt <https://www.google.com/search?q=makefile+instead+of+grunt>`_

       `What's in a Build Tool? (lihaoyi.com) <http://www.lihaoyi.com/post/WhatsinaBuildTool.html>`_
       (`HN discussions <https://news.ycombinator.com/item?id=11222967>`__)

       `ocaml-9p/Makefile at master · mirage/ocaml-9p · GitHub <https://github.com/mirage/ocaml-9p/blob/master/Makefile>`_

       `rappel/Makefile at master · yrp604/rappel · GitHub <https://github.com/yrp604/rappel/blob/master/Makefile>`_

       `In defense of Unix (leancrew.com) <http://leancrew.com/all-this/2016/03/in-defense-of-unix/>`_
       (`HN discussions <https://news.ycombinator.com/item?id=11229025>`__)

.. [10] `makefile check if symlink exists <https://www.google.com/search?q=makefile+check+if+symlink+exists>`_

.. [11] `makefile concatenate files <https://www.google.com/search?q=makefile+concatenate+files>`_

        `javascript - Makefile to combine js files and make a compressed version - Stack Overflow <http://stackoverflow.com/questions/4413903/makefile-to-combine-js-files-and-make-a-compressed-version>`_

        `build - Is there a way to exclude certain source files or folders from a makefile? - Stack Overflow <http://stackoverflow.com/questions/1531318/is-there-a-way-to-exclude-certain-source-files-or-folders-from-a-makefile>`_

.. _Pāli Dictionary: http://dictionary.sutta.org/
.. _Pāli Tipiṭaka: http://tipitaka.sutta.org/
.. _Ubuntu 15.10: http://releases.ubuntu.com/15.10/
.. _Python 2.7.10: https://www.python.org/downloads/release/python-2710/
.. _Go 1.6: https://golang.org/dl/
.. _Go: https://golang.org/
.. _git clone: https://www.google.com/search?q=git+clone
.. _pali repository: https://github.com/siongui/pali
.. _data repository: https://github.com/siongui/data
.. _UNLICENSE: http://unlicense.org/
