# Pāḷi Tipiṭaka & Dictionary

My development environment is Ubuntu 13.04 with Python 2.7. If you are using Windows, <strong>i18nUtils.py</strong> cannot be run unless you install <em><a href="http://www.gnu.org/software/gettext/">GNU gettext tools</a></em>, which include <em>xgettext</em>, <em>msginit</em>, <em>msgmerge</em>, and <em>msgfmt</em>. However, I do not know how to install <em>GNU gettext tools</em> on Windows.

The data files, including Pāḷi texts, translations, and dictionaries, are located at [data repository](https://github.com/siongui/data). Some Python and JavaScript libraries are also in [data repository](https://github.com/siongui/data).

Please [install necessary tools for development](INSTALL_GAE.md) before setting up development environment.

## Set Up Development Environment

<i>PALI_DIR</i> below means the directory where you git clone [pali repository](https://github.com/siongui/pali).

1. git clone the [pali repository](https://github.com/siongui/pali) and [data repository](https://github.com/siongui/data) (put in the same directory). Then download [Google App Engine Python SDK](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python), unzip it, and also put in the same directory.
```bash
    # create a directory to contain both pali and data repository.
    $ mkdir dev
    $ cd dev
    # git clone repositories
    $ git clone https://github.com/siongui/pali.git
    $ git clone https://github.com/siongui/data.git

    # dowload App Engine SDK (remember to put in the same directory as pali and data repositories)
    $ wget http://googleappengine.googlecode.com/files/google_appengine_{{ version }}.zip
    $ unzip google_appengine_{{ version }}.zip
```

2. Run <b>PALI_DIR/setup/setupdev.py</b> to create symbolic links and i18n files (<em>pot</em>, <em>po</em>, <em>mo</em> files in [PALI_DIR/common/locale directory](https://github.com/siongui/pali/tree/master/common/locale)) for use on dev and production server. Note that [pali repository](https://github.com/siongui/pali) and [data repository](https://github.com/siongui/data) must be put in the same directory. Otherwise symbolic links will not point to correct directories.)
```bash
    $ python PALI_DIR/setup/setupdev.py
```

3. Uncomment (remove leading #) the following line in PALI_DIR/dictionary/app.yaml
```bash
    #builtins:
    #- remote_api: on
```

4. Uncomment (remove leading #) the following line in PALI_DIR/tipitaka/app.yaml
```bash
    #- url: /customRemoteBlobstoreAPI
    #  script: customRemoteBlobstoreAPI.app
    #  login: admin
 
    #builtins:
    #- remote_api: on
```

5. Create index of words in dictionary books.
   After data files created, upload them to Google App Engine dev server:
```bash
    $ cd PALI_DIR/dictionary/setup/
    $ python init1parseBooks.py
    $ python init2parseWords.py
    $ python init3prefixWordsHtml.py

    # copy succinct trie of words
    $ cd PALI_DIR/dictionary/pylib/json/
    $ cp ../../../../data/src/succinct_trie.json .
    # (optional) build succinct trie of words
    #$ cd PALI_DIR/dictionary/setup/nodejs
    #$ nodejs buildSuccinctTrie.js

    # create client-side JavaScript data files
    $ cd PALI_DIR/dictionary/setup/
    $ python init4jsonToJS.py

    $ cd PALI_DIR/dictionary
    # Install grunt plugins
    $ npm install
    # combine and minify JavaScript/CSS.
    $ grunt
    # ctrl-C to abort watching, and then run Google App Engine dev server.
    $ grunt run

    # keep above "grunt run" terminal running, and open another terminal
    # uploading words files to local GAE datastore of dev server.
    # Please answer 'y' when asked if upload to dev server
    $ cd PALI_DIR/dictionary/setup/
    $ python init5uploadToGAE.py

    # after uploading finished, open browser to test local dev server:
    # http://localhost:8080/
```

6. Create data files used for Pāḷi Tipiṭaka and path of webpages of online Pāḷi Tipiṭaka website.
   After data files created, upload them to Google App Engine dev server:
```bash
    $ cd PALI_DIR/tipitaka/setup/
    $ python init1getTocs.py
    $ python init2tocsToJson.py
    $ python init3addSubpathInJson.py

    # Create Tipiṭaka-related translations for server and client.
    $ python setTranslationData.py

    $ cd PALI_DIR/tipitaka
    # Install grunt plugins
    $ npm install
    # combine and minify JavaScript/CSS.
    $ grunt
    # ctrl-C to abort watching, and then run Google App Engine dev server.
    $ grunt run

    # keep above "grunt run" terminal running, and open another terminal
    # uploading data files to local GAE datastore of dev server.
    # Please answer 'y' when asked if upload to dev server
    $ cd PALI_DIR/tipitaka/setup/
    $ python init4uploadToGAE.py

    # after uploading finished, open browser to test local dev server:
    # http://localhost:8080/
```

7. Deploy on [Google App Engine (Python)](https://developers.google.com/appengine/docs/python/gettingstartedpython27/uploading): Before deployment, please modify the application name to your app name at the first line in [PALI_DIR/tipitaka/app.yaml](https://github.com/siongui/pali/blob/master/tipitaka/app.yaml) and [PALI_DIR/dictionary/app.yaml](https://github.com/siongui/pali/blob/master/dictionary/app.yaml).
```bash
    # deploy dictionary website
    $ cd PALI_DIR/dictionary
    # combine and minify JavaScript/CSS.
    $ grunt
    # ctrl-C to abort watching, then upload dictionary website to Google App Engine production server.
    $ grunt update

    # uploading words files to online GAE datastore of production server.
    # Please answer 'n' when asked if upload to dev server
    $ cd PALI_DIR/dictionary/setup/
    $ python init5uploadToGAE.py

    # deploy tipitaka website
    $ cd PALI_DIR/tipitaka
    $ grunt
    # ctrl-C to abort watching, then upload tipitaka website app to Google App Engine production server.
    $ grunt update

    # uploading data files to online GAE datastore of production server.
    # Please answer 'n' when asked if upload to dev server
    $ cd PALI_DIR/tipitaka/setup/
    $ python init4uploadToGAE.py
```

## Development of Python/JavaScript/HTML/CSS code for the websites

Open and keep two terminals running, one for running Google App Engine dev server, the other for running grunt watch. The changes you make can be viewed from <em>http://localhost:8080/</em> in your browser window. (reload the page if the window is already open)

```bash
# open one termimal
$ cd PALI_DIR/dictionary    # if you are developing dictionary website
$ cd PALI_DIR/tipitaka      # if you are developing tipitaka website
# combine and minify JavaScript/CSS. Re-combine and re-minify if any changes made.
$ grunt

# open another terminal
$ cd PALI_DIR/dictionary    # if you are developing dictionary website
$ cd PALI_DIR/tipitaka      # if you are developing tipitaka website
# run Google App Engine dev server
$ grunt run

# open browser window at the following URL
# http://localhost:8080/
```

## Development of i18n

Everytime strings in html files are marked to be translated, remember to re-create i18n files and re-compile JavaScript files. A helper script named <b>i18nUtils.py</b> (located under <b>PALI_DIR/setup/</b>) to automate the i18n jobs.

```bash
$ cd PALI_DIR/setup/
# re-create i18n files and re-compile JavaScript files
$ python i18nUtils.py all

$ cd PALI_DIR/dictionary
# run grunt to update combined js file of dictionary website
$ grunt
# ctrl-C to abort grunt watch
$ cd PALI_DIR/tipitaka
# run grunt to update combined js file of tipitaka website
$ grunt
```

