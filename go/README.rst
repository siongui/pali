=======================================
`Pāli Dictionary`_ and `Pāli Tipiṭaka`_
=======================================

Re-implementation of `Pāli Dictionary`_ and `Pāli Tipiṭaka`_ in Go_ programming
language.

Development Environment: `Ubuntu 15.10`_ and `Go 1.5.3`_.


Set Up Development Environment
++++++++++++++++++++++++++++++

1. Download Go_:

   .. code-block:: bash

     # create a workspace in your home directory
     $ mkdir ~/dev
     # enter workspace
     $ cd ~/dev
     # download Go 1.5.3 for Linux 64-bit
     $ wget https://storage.googleapis.com/golang/go1.5.3.linux-amd64.tar.gz
     # uncompress and untar
     $ tar xvzf go1.5.3.linux-amd64.tar.gz

2. `git clone`_ the `pali repository`_ and `data repository`_:

   .. code-block:: bash

     # git clone pali repository
     $ cd ~/dev
     $ git clone https://github.com/siongui/pali.git
     # enter directory of go implementation
     $ cd ~/dev/pali/go
     # git clone data repository
     $ make clone

3. Install GopherJS_, pyScss_ (or `go-libsass`_), `gettext-go`_, OpenCC_,
   `OpenCC Go binding`_, and common libraries for this project:

   .. code-block:: bash

     $ make install

4. Set up data of this project:

   .. code-block:: bash

     $ make parsebooks
     $ make parsewords
     $ make html
     $ make scss
     $ make js

5. Run development server at http://localhost:8000/

   .. code-block:: bash

     $ make devserver


UNLICENSE
+++++++++

Released in public domain. See UNLICENSE_.


References
++++++++++

.. [1] `GitHub - siongui/pali: Pāḷi Tipiṭaka and Pāḷi Dictionaries <https://github.com/siongui/pali>`_

.. [2] `siongui/data: Data files for Pāḷi Tipiṭaka, Pāḷi Dictionaries, and external libraries <https://github.com/siongui/data>`_


.. _Pāli Dictionary: https://siongui.github.io/pali-dictionary/
.. _Pāli Tipiṭaka: https://epalitipitaka.appspot.com/
.. _Go: https://golang.org/
.. _Ubuntu 15.10: http://releases.ubuntu.com/15.10/
.. _Go 1.5.3: https://golang.org/dl/
.. _git clone: https://www.google.com/search?q=git+clone
.. _pali repository: https://github.com/siongui/pali
.. _data repository: https://github.com/siongui/data
.. _UNLICENSE: http://unlicense.org/
.. _GopherJS: http://www.gopherjs.org/
.. _go-libsass: https://github.com/wellington/go-libsass
.. _pyScss: https://github.com/Kronuz/pyScss
.. _gettext-go: https://github.com/chai2010/gettext-go
.. _OpenCC: https://github.com/BYVoid/OpenCC
.. _OpenCC Go binding: https://github.com/siongui/go-opencc
