=======================================
`Pāli Dictionary`_ and `Pāli Tipiṭaka`_
=======================================

Re-implementation of `Pāli Dictionary`_ and `Pāli Tipiṭaka`_ in Go_ programming
language.

Development Environment: `Ubuntu 16.04`_/`Ubuntu 16.10`_ and `Go 1.7`_.


Set Up Development Environment
++++++++++++++++++++++++++++++

1. `git clone`_ the `pali repository`_ and `data repository`_:

   .. code-block:: bash

     # create a workspace in your home directory
     $ mkdir ~/dev
     # enter workspace
     $ cd ~/dev
     # git clone pali repository
     $ git clone https://github.com/siongui/pali.git --depth=1
     # or clone with full depth
     #$ git clone https://github.com/siongui/pali.git
     # enter directory of Go implementation
     $ cd ~/dev/pali/go
     # git clone data repository
     $ make clone_pali_data

2. Update Ubuntu and install following packages:

   - Go_
   -  GopherJS_
   - `go-libsass`_ (or pyScss_)
   - `gettext-go`_
   - OpenCC_
   - `OpenCC Go binding`_
   - `go-succinct-trie`_
   - `go-online-pali-ime`_
   - `gopherjs-i18n`_
   - `gopherjs-utils`_
   - `gopherjs-input-suggest`_

   and common libraries for this project:

   .. code-block:: bash

     $ cd ~/dev/pali/go
     $ make update_ubuntu
     $ make download_go
     $ make install

     # you will get error message if you use Ubuntu 16.10, but it's ok.
     # waiting upstream to fix the libopencc-dev install issue
     $ make lib_opencc


3. Set up data of this project:

   .. code-block:: bash

     # optional: parse dictionary books
     $ make parsebooks

     $ make parsewords

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

     # If you use Ubuntu 16.10, uninstall libopencc-dev by the following command
     # waiting upstream to fix the libopencc-dev install issue
     $ make uninstall_libopencc-dev


4. Run development server at http://localhost:8000/

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
.. _Ubuntu 16.04: http://releases.ubuntu.com/16.04/
.. _Ubuntu 16.10: http://releases.ubuntu.com/16.10/
.. _Go 1.7: https://golang.org/dl/
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
.. _gopherjs-utils: https://github.com/siongui/gopherjs-utils
.. _gopherjs-input-suggest: https://github.com/siongui/gopherjs-input-suggest
