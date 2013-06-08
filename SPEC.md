# Specifications of Pāḷi Tipiṭaka & Dictionary Websites

## Multilingual Support of the Website

Two different implementations are allowed. The <strong>locale</strong>s are listed [here](http://www.roseindia.net/tutorials/I18N/locales-list.shtml).

### Implementation #1 (Current Implementation)

When users visit <strong>/.*</strong>, the server should serve the content of the website in <strong>locale</strong> language according to http ACCEPT_LANGUAGES header. If locales in ACCEPT_LANGUAGES are all un-supported, then the sever should serve English (en_US) content by default.

when users visit <strong>/{{ locale }}/.*</strong>, the server should serve the content of the website in {{ locale }} language regardless of http ACCEPT_LANGUAGES header. For example, when users visit <strong>/zh_TW/.*</strong>, the server should serve the content of the websites in Traditional Chinese.

### Implementation #2 (sub-domain implementation)

When users visit <strong>example.org/.*</strong> or <strong>www.example.org/.*</strong>, the server should serve the content of the website in <strong>locale</strong> language according to http ACCEPT_LANGUAGES header. If locales in ACCEPT_LANGUAGES are all un-supported, then the sever should serve English (en_US) content by default.

when users visit <strong>{{ locale }}.example.org/.*</strong>, the server should serve the content of the website in {{ locale }} language regardless of http ACCEPT_LANGUAGES header. For example, when users visit <strong>zh_TW.example.org/.*</strong>, the server should serve the content of the websites in Traditional Chinese.

## Order of Dictionaries When Users Lookup the Word

currently 5 different languages of dictionaries are supported: Pali-English, Pali-Chinese, Pali-Japanese, Pali-Vietnamese, Pali-Burmese.

When users look up the definition of the word, no matter in tooltip or preview, the order of the languages of dictionaries should be determined according to http ACCEPT_LANGUAGES header by default. If not in ACCEPT_LANGUAGES, the order can be determined by programmers.

Besides, in the settings of the website, options should be provided to users to choose the order of the languages of dictionaries.


