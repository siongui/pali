# Specifications of Pāḷi Tipiṭaka & Dictionary Websites

## Multi-Language Support

Two different implementation is allowed. The <strong>locale</strong>s are listed [here](http://www.roseindia.net/tutorials/I18N/locales-list.shtml).

### Implementation #1 (Current Implementation)

When users visit <strong>/.*</strong>, the server should serve the content of the website in <strong>locale</strong> language according to http ACCEPT_LANGUAGES header. If locales in ACCEPT_LANGUAGES are all un-supported, then the sever should serve English by default.

when users visit <strong>/{{ locale }}/.*</strong>, the server should serve the content of the website in {{ locale }} language regardless of http ACCEPT_LANGUAGES header. For example, when users visit <strong>/zh_TW/.*</strong>, the server should serve the content of the websites in Traditional Chinese.

### Implementation #2 (sub-domain implementation)

When users visit <strong>example.org/.*</strong> or <strong>www.example.org/.*</strong>, the server should serve the content of the website in <strong>locale</strong> language according to http ACCEPT_LANGUAGES header. If locales in ACCEPT_LANGUAGES are all un-supported, then the sever should serve English by default.

when users visit <strong>{{ locale }}.example.org/.*</strong>, the server should serve the content of the website in {{ locale }} language regardless of http ACCEPT_LANGUAGES header. For example, when users visit <strong>zh_TW.example.org/.*</strong>, the server should serve the content of the websites in Traditional Chinese.

