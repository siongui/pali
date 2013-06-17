# Pāḷi Tipiṭaka & Dictionary

* If you want to setup development environment and deploy applications on [Google App Engine Python](https://developers.google.com/appengine/docs/python/), please refer to this [README](docs/README_GAE.md).

My development environment is Ubuntu 13.04 with Python 2.7. If you are using Windows, <strong>i18nUtils.py</strong> cannot be run unless you install <em><a href="http://www.gnu.org/software/gettext/">GNU gettext tools</a></em>, which include <em>xgettext</em>, <em>msginit</em>, <em>msgmerge</em>, and <em>msgfmt</em>. However, I do not know how to install <em>GNU gettext tools</em> on Windows.

The data files, including Pāḷi texts, translations, and dictionaries, are located at [data](https://github.com/siongui/data) repository. Some Python and JavaScript libraries are also in [data](https://github.com/siongui/data) repository.

Please [install necessary tools for development](INSTALL.md) before setting up development environment.

## Set Up Development Environment

<i>PALI_DIR</i> below means the directory where you git clone <em>pali</em> repository.

1. git clone the [pali](https://github.com/siongui/pali) repository and [data](https://github.com/siongui/data) repository (put in the same directory).
```bash
    # create a directory to contain both pali and data repository.
    $ mkdir dev
    $ cd dev
    # git clone repositories
    $ git clone https://github.com/siongui/pali.git
    $ git clone https://github.com/siongui/data.git
```

2. Run <b>PALI_DIR/setup/setupdev.py</b> to create symbolic links and i18n files (pot, po, mo files under <strong>PALI_DIR/common/locale/</strong> directory) for use on dev and production server. (<em>pali</em> repository and <em>data</em> repository must be put under the same directory. Otherwise symlinks will not point to correct directories.)
```bash
    $ python PALI_DIR/setup/setupdev.py
```

3. Create index of words in dictionary books.
```bash
    $ cd PALI_DIR/dictionary/setup/
    $ python init1parseBooks.py
    $ python init2parseWords.py
    $ python init3prefixWordsHtml.py

    # build succinct trie of words
    $ cd PALI_DIR/dictionary/setup/nodejs
    $ nodejs buildSuccinctTrie.js
    $ cd PALI_DIR/dictionary/setup/
    $ python init4jsonToJS.py

    $ cd PALI_DIR/dictionary
    # Install grunt plugins
    $ npm install
    # combine and minify JavaScript/CSS.
    $ grunt
    # ctrl-C to abort watching, and then run dev server.
    $ python devNotGaeRun.py
```

4. See if dictionary website works: (Please keep above dev server running)
```bash
    # open browser to test local dev server:
    # http://localhost:8080/
```

5. Create Tipiṭaka-related translations for server and client.
```bash
    $ cd PALI_DIR/tipitaka/setup/
    $ python setTranslationData.py
```

6. Create data files used for Pāḷi Tipiṭaka and path of webpages of online Pāḷi Tipiṭaka website:
```bash
    $ cd PALI_DIR/tipitaka/setup/
    $ python init1getTocs.py
    $ python init2tocsToJson.py
    $ python init3addSubpathInJson.py

    $ cd PALI_DIR/tipitaka
    # Install grunt plugins
    $ npm install
    # combine and minify JavaScript/CSS.
    $ grunt
    # ctrl-C to abort watching, and then run dev server.
    $ python devNotGaeRun.py
```

7. See if tipiṭaka website works: (Please keep above dev server running)
```bash
    # open browser to test local dev server:
    # http://localhost:8080/
```

8. Deploy on [AWS EC2](http://aws.amazon.com/ec2/): See [AWS.md](docs/AWS.md)

## Development of Python/JavaScript/HTML/CSS code for the websites

Open and keep two terminals running, one for running dev server, the other for running grunt watch. The changes you make can be viewed from <em>http://localhost:8080/</em> in your browser window. (reload the page if the window is already open)

```bash
# open one termimal
$ cd PALI_DIR/dictionary    # if you are developing dictionary website
$ cd PALI_DIR/tipitaka      # if you are developing tipitaka website
# combine and minify JavaScript/CSS. Re-combine and re-minify if any changes made.
$ grunt

# open another terminal
$ cd PALI_DIR/dictionary    # if you are developing dictionary website
$ cd PALI_DIR/tipitaka      # if you are developing tipitaka website
# run dev server
$ python devNotGaeRun.py

# open browser window at the following URL
# http://localhost:8080/
```

## Development of i18n

Everytime strings in html files are marked to be translated, remember to re-generate i18n files and re-compile JavaScript files. A helper script named <b>i18nUtils.py</b> (located under <b>PALI_DIR/setup/</b>) to automate the i18n jobs.

```bash
$ cd PALI_DIR/setup/
# create POT from html files
$ python i18nUtils.py pot
# initialize PO files if not exist, or update POs files if exist.
$ python i18nUtils.py po
# after initialization, edit PO files and translate strings in PO files. Then
$ python i18nUtils.py cn
# the above command update zh_CN PO file from zh_TW PO file,
# so you do not have to manual translate (optional if you want to manually translate zh_CN PO file).
# then create MO files for server-side i18n
$ python i18nUtils.py mo
# create files for client-side i18n
$ python i18nUtils.py js

# run grunt to update files
$ cd PALI_DIR/dictionary
$ grunt
# ctrl-C to abort grunt watch
$ cd PALI_DIR/tipitaka
$ grunt
```

