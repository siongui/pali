# Pāḷi Tipiṭaka & Dictionary

My development environment is Ubuntu 13.04 with Python 2.7. If you are using Windows, <strong>i18nUtils.py</strong> cannot be run unless you install <em><a href="http://www.gnu.org/software/gettext/">GNU gettext tools</a></em>, which include <em>xgettext</em>, <em>msginit</em>, <em>msgmerge</em>, and <em>msgfmt</em>. However, I do not know how to install <em>GNU gettext tools</em> on Windows.

The data files, including Pāḷi texts, translations, and dictionaries, are located at [data](https://github.com/siongui/data) repository. Some Python and JavaScript libraries are also in [data](https://github.com/siongui/data) repo.

Please [install necessary tools for development](https://github.com/siongui/pali/blob/master/INSTALL.md) before setting up development environment.

## Set Up Development Environment (TO BE UPDATED)

<i>PALI_DIR</i> below means the directory where you git clone <em>pali</em> repository. <i>GAE_PYSDK_DIR</i> means the directory of [Google App Engine Python SDK](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python).

1. git clone the <em>pali</em> repository and <em>data</em> repository (put in the same dir). Then download [Google App Engine Python SDK](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python), unzip it, and also put in the same dir.
```bash
    # create a directory to contain both pali and data repository.
    mkdir dev
    cd dev
    # git clone repositories
    git clone https://github.com/siongui/pali.git
    git clone https://github.com/siongui/data.git

    # dowload App Engine SDK (remember to put in the same dir as git repositories)
    wget {{SDK_URL}}
    unzip {{APP_ENGINE_SDK_ZIP_FILE}}
```

2. Run <b>PALI_DIR/common/pytools/setupdev.py</b> to create symbolic links. (<em>pali</em> repository and <em>data</em> repository must be put under the same directory. Otherwise symlinks will not point to correct directories.)
```bash
    python PALI_DIR/common/pytools/setupdev.py
```

3. Create index of words in dictionary books.
```bash
    cd PALI_DIR/common/pytools/
    python dic1parseBooks.py
    python dic2parseWords.py
    python dic3uploadToGAE.py

    # build succinct trie of words
    cd PALI_DIR/common/pytools/nodejs
    nodejs buildSuccinctTrie.js
```

4. Create data files (<strong>PALI_DIR/tipitaka/app/js/treeviewAllJson-service.js</strong> and <strong>REPO_DIR/tipitaka/gaelibs/json/treeviewAll.json</strong>) used for Pāḷi Tipiṭaka and path of webpages of online Pāḷi Tipiṭaka website. After data files created, upload them to Google App Engine:
```bash
    cd PALI_DIR/common/pytools/
    python tpk1getTocs.py
    python tpk2tocsToJson.py
    python tpk3addSubpathInJson.py
    python tpk4uploadToGAE.py
```

5. Create Tipiṭaka-related translations for server and client.
```bash
    cd PALI_DIR/tipitaka/gaelibs/
    python translationData.py
```

6. Create i18n files (pot, po, mo files under <strong>PALI_DIR/common/locale/</strong> directory) for production use on server side:
```bash
    cd PALI_DIR/common/pytools/
    # create i18n files
    python i18nUtils.py pot
    python i18nUtils.py po
    python i18nUtils.py cn
    python i18nUtils.py mo

    # create JavaScript file ( <strong>PALI_DIR/common/app/js/services-i18nStrings.js</strong> ) of translated strings for client side
    python i18nUtils.py js
```

7. Create compiled JavaScript files:
```bash
    # create compiled JavaScript files ( <strong>PALI_DIR/dictionary/app/all_compiled.js</strong> and <strong>REPO_DIR/tipitaka/app/all_compiled.js</strong> ) by Google Closure Compiler Service API
    python compile.py
```

8. Deploy on [Google App Engine (Python)](https://developers.google.com/appengine/docs/python/gettingstartedpython27/uploading): Before deployment, please modify the application name at the first line in <i><b>PALI_DIR/tipitaka/app.yaml</b></i> and <i><b>REPO_DIR/dictionary/app.yaml</b></i>. 
```bash
    cd GAE_PYSDK_DIR/
    # deploy dictionary
    ./appcfg.py update PALI_DIR/dictionary
    # deploy tipitaka
    ./appcfg.py update PALI_DIR/tipitaka
```

## Writing JavaScript Code ...

Remember to re-compile all JavaScript files before deployment or before testing the compiled file:

```bash
cd PALI_DIR/common/pytools/
python compile.py
```

## Development of i18n

Everytime strings in html files are marked to be translated, remember to re-generate i18n files and re-compile JavaScript files. A helper script named <b>i18nUtils.py</b> (located under <b>PALI_DIR/common/pytools/</b>) to automate the i18n jobs.

```bash
cd PALI_DIR/common/pytools/
# create POT from html files
python i18nUtils.py pot
# initialize PO files if not exist, or update POs files if exist.
python i18nUtils.py po
# after initialization, edit PO files and translate strings in PO files. Then
python i18nUtils.py cn
# the above command update zh_CN PO file from zh_TW PO file,
# so you do not have to manual translate (optional if you want to manually translate zh_CN PO file).
# then create MO files for server-side i18n
python i18nUtils.py mo
# create files for client-side i18n
python i18nUtils.py js
# re-compile all JavaScript files
python compile.py
```

# References

## i18n (to be updated)

Related links to enable i18n:
* [Internationalization and localization with webapp2](http://webapp-improved.appspot.com/tutorials/i18n.html)
* [How to enable {% trans %} tag for jinja templates?](http://stackoverflow.com/questions/8471455/how-to-enable-trans-tag-for-jinja-templates)
* [Extensions - Jinja2 2.7-dev documentation](http://jinja.pocoo.org/docs/extensions/)

### Enable i18n Using webapp2, jinja2, babel, and gaepytz

To enable i18n using webapp2, jinja2, babel, gaepytz. The following lines in [main.py](https://github.com/siongui/palidictionary/blob/master/main.py) is crucial:
```bash
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gaepalilibs/babel.zip'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gaepalilibs/pytz.zip'))

from webapp2_extras import i18n

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader([os.path.join(os.path.dirname(__file__), 'app'),
                                    os.path.join(os.path.dirname(__file__), 'app/sympartials')]),
    extensions=['jinja2.ext.i18n'],
    variable_start_string='{$',
    variable_end_string='$}')

jinja_environment.install_gettext_translations(i18n)
```
The point is that [zipimport](https://developers.google.com/appengine/articles/django10_zipimport) babel and gaepytz which we install in advance. Then import i18n in webapp2_extras, enable i18n extension of jinja2, and install webapp2 i18n in jinja2.

To tell jinja2 to serve translalted strings, the strings in HTML files need to be marked like the following:
```bash
# If default variable start_string and end_stirng are used
{{_("string_to_be_translated")}}

# In our case, we use {$ and $} as start_string and end_string respectively
# to prevent collision with the notation of AngularJS interpolation
# so we need to wrap the string like the following
{$_("string_to_be_translated")$}
```

And in the http request handler, call <em>[i18n.get_i18n().set_locale()](http://webapp-improved.appspot.com/api/webapp2_extras/i18n.html#webapp2_extras.i18n.I18n.set_locale)</em> to specify the locale we want to serve. The following sample code demonstrates how:
```python
class MainPage(webapp2.RequestHandler):
  def get(self):
    template_values = {...}
    i18n.get_i18n().set_locale('zh_TW')

    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))
```
### Extract from HTML and Create POT

Related links to generate translation files (POT, PO, and MO files):
* [Internationalize A Python Application](http://wiki.maemo.org/Internationalize_a_Python_application)
* [Python localization made easy](http://www.supernifty.org/blog/2011/09/16/python-localization-made-easy/)

The default locale directory of webapp2_extras i18n is <b>PALI_DIR/locale/</b> and default domain is <b><i>messages</i></b> (see [webapp2_extras.i18n.default_config](http://webapp-improved.appspot.com/api/webapp2_extras/i18n.html#webapp2_extras.i18n.default_config) for details). In our repository, the html files to be localized are located under <b>REPO_DIR/app/</b>, texts to be translated are wrapped in <b><i> _("TEXT_TO_BE_TRANSLATED") </i></b>. Note that cannot use <b><i> _(' ') </i></b> to wrap texts, must use <b><i> _(" ") </i></b>. Otherwise <i>[xgettext](http://www.gnu.org/software/gettext/manual/html_node/xgettext-Invocation.html)</i> utility cannot recognize the texts and will not put them in POT file. After finishing wraping texts to be translated, we can use the following Python code to generate POT file:
```python
locale_dir = os.path.join(os.path.dirname(__file__), '../locale')
html_dir = os.path.join(os.path.dirname(__file__), '../app')

if not os.path.exists(locale_dir):
  os.makedirs(locale_dir)

cmd_xgettext = 'xgettext --no-wrap --from-code=UTF-8 --keyword=_ --output=%s/messages.pot `find %s -name *.html`' % (locale_dir, html_dir)
cmd_sed = 'sed -i "s/charset=CHARSET/charset=utf-8/g" %s/messages.pot' % locale_dir

os.system(cmd_xgettext)
os.system(cmd_sed)
```
<i>[xgettext](http://www.gnu.org/software/gettext/manual/html_node/xgettext-Invocation.html)</i> is the utility to generate POT file. HTML format is not supported format so <i>xgettext</i> will give warnings but still can generate POT file. See this Stack Overflow [question](http://stackoverflow.com/questions/1656174/gettext-for-html-or-latex) for reference.

### Initialize PO from POT

The next step is to initialize the PO files for each locale. <b><i>[msginit](http://www.gnu.org/software/gettext/manual/html_node/msginit-Invocation.html)</i></b> is responsible for creating a new PO file for a given locale. The PO file of a given <i>locale</i> in our application will be located under <b>PALI_DIR/locale/{{locale}}/LC_MESSAGES/messages.po</b>, where {{locale}} is the name of the locale. The following Python code can be used to call <i>msginit</i> to create a PO file for a given locale.
```python
def initLocalePO(locale):
  locale_dir = os.path.join(os.path.dirname(__file__), '../locale')
  potpath = os.path.join(locale_dir, 'messages.pot')
  popath = os.path.join(locale_dir, '%s/LC_MESSAGES/messages.po' % locale)

  if not os.path.exists(os.path.dirname(popath)):
    os.makedirs(os.path.dirname(popath))
  cmd_msginit = 'msginit --no-translator --input=%s --locale=%s -o %s' % (potpath, locale, popath)
  os.system(cmd_msginit)
```
Currently three locales are supported (en_US, zh_TW, zh_CN). After PO files are created, edit the PO files to translate texts.

### Create MO from PO

Final step is to create MO files to be used in production. One PO file has a corresponding MO file. The following Python code shows how to use <b><i>[msgfmt](http://www.gnu.org/software/gettext/manual/html_node/msgfmt-Invocation.html)</i></b> to create MO file from a give po file. The MO file in our application will be located in the same directory as the source PO file ( in <b>PALI_DIR/locale/{{locale}}/LC_MESSAGES/messages.po</b> ).
```python
def formatMO(locale):
  locale_dir = os.path.join(os.path.dirname(__file__), '../locale')
  popath = os.path.join(locale_dir, '%s/LC_MESSAGES/messages.po' % locale)
  mopath = popath[:-2] + 'mo'

  cmd_msgfmt = 'msgfmt %s -o %s' % (popath, mopath)
  os.system(cmd_msgfmt)
```

### Merge PO files

Everytime strings are marked in html files, [msgmerge](http://www.gnu.org/software/gettext/manual/html_node/msgmerge-Invocation.html) ([reference](http://wiki.xfce.org/translations/msgmerge)) can be used to merge translated strings from two PO (or POT) files into one, so translated strings can be re-used without manual typing once again.
```python
def updateLocalePO(locale):
  locale_dir = os.path.join(os.path.dirname(__file__), '../locale')
  potpath = os.path.join(locale_dir, 'messages.pot')
  popath = os.path.join(locale_dir, '%s/LC_MESSAGES/messages.po' % locale)

  if not os.path.exists(os.path.dirname(popath)):
    os.makedirs(os.path.dirname(popath))
  cmd_msginit = 'msgmerge --no-wrap --backup=none --update %s %s' % (popath, potpath)
  print(cmd_msginit)
  os.system(cmd_msginit)
```

### TODO: write something about fusion of i18n on both server side and client side, and json/js parameters in i18nUtils.py

