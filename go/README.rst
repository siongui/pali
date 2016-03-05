=======================================
`Pāli Dictionary`_ and `Pāli Tipiṭaka`_
=======================================

Re-implementation of `Pāli Dictionary`_ and `Pāli Tipiṭaka`_ in Go_ programming
language.

Development Environment: `Ubuntu 15.10`_ and `Go 1.6`_.


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
     # enter directory of go implementation
     $ cd ~/dev/pali/go
     # git clone data repository
     $ make clone

3. Install GopherJS_, `go-libsass`_ (or pyScss_), `gettext-go`_, OpenCC_,
   `OpenCC Go binding`_, `go-succinct-trie`_, `go-online-pali-ime`_,
   `gopherjs-i18n`_ and common libraries for this project:

   .. code-block:: bash

     $ make install

4. Set up data of this project:

   .. code-block:: bash

     # optional: parse dictionary books
     $ make parsebooks

     $ make parsewords
     $ make twpo2cn

     # optional: convert po files to json
     $ make po2json

     # optional: build succinct trie
     $ make succinct_trie

     # optional: create blob
     $ make blobgo

     $ make po2mo
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
.. _Pāli Tipiṭaka: http://tipitaka.sutta.org/
.. _Go: https://golang.org/
.. _Ubuntu 15.10: http://releases.ubuntu.com/15.10/
.. _Go 1.6: https://golang.org/dl/
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
.. _go-succinct-trie: https://github.com/siongui/go-succinct-data-structure-trie
.. _go-online-pali-ime: https://github.com/siongui/go-online-input-method-pali
.. _gopherjs-i18n: https://github.com/siongui/gopherjs-i18n
