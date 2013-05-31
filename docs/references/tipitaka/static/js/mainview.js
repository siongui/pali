/**
 * @fileoverview Show pali on the mainview Div
 */

pali.require('base');

var MainView = MainView || {};

MainView.mainview = document.getElementById('mainview');

MainView.cache = {}; // key:value -> url: xmlDoc

MainView.getPaliUrl = function(xmlFilename) {
  return '/romn/cscd/' + xmlFilename;
};

MainView.getTranslationUrl = function(xmlFilename, locale, source) {
  return '/translation/' + locale + '/' + source + '/' + xmlFilename;
};

MainView.showOnMainView = function(element) {
  pali.removeAllChildren(MainView.mainview);
  MainView.mainview.appendChild(element);
  i18n.translateMainView();
};

MainView.showLoading = function(canonName) {
  pali.removeAllChildren(MainView.mainview);
  var info = document.createElement('span');
  info.style.padding = '1em';
  // FIXME: use innerHTML?
  info.appendChild(document.createTextNode(
    i18n.gettext('Loading') + ' ' +
    i18n.translateCanonText(canonName) + ' ...'));
  MainView.mainview.appendChild(info);
};

MainView.loadPaliXmlDoc = function(xmlFilename, canonName, opt_translation, opt_locale, opt_source) {
  MainView.showLoading(canonName);

  if (opt_translation)
    var url = MainView.getTranslationUrl(xmlFilename, opt_locale, opt_source);
  else
    var url = MainView.getPaliUrl(xmlFilename);

  if (MainView.cache.hasOwnProperty(url))
    MainView.parsePaliXmlDoc(MainView.cache[url], url);
  else {
    if (opt_translation && opt_locale == 'zh_CN')
      url = url.replace('zh_CN', 'zh_TW');
    pali.httpGetXml(url, function(xmlDoc, urlDoc) {
      if (opt_translation && opt_locale == 'zh_CN') {
        urlDoc = urlDoc.replace('zh_TW', 'zh_CN');
        i18n.xmlDoc2CN(xmlDoc);
      }
      MainView.cache[urlDoc] = xmlDoc;
      MainView.parsePaliXmlDoc(xmlDoc, urlDoc);
    });
  }
};


function onWordDbclick(e) {
  var word = Lookup.getProcessedUserInput(this.innerHTML.toLowerCase());
  if (word == null) return;

  var url = 'http://palidictionary.appspot.com/browse/' + word[0] + '/' + word;
  if (window.location.host == 'localhost:8080') url += '?track=no';
  window.open(url);
}

function onWordMouseOver(e) {
  this.style.color = 'red';
  if (!document.getElementById('showTooltip').checked) return;

  setTimeout(Lookup.getLookupResult.bind(this),
             Lookup.DELAY_INTERVAL);
}

function onWordMouseOut(e) {
  this.style.color = '';
  if (!document.getElementById('showTooltip').checked) return;

  setTimeout(Lookup.delayedCloseTooltip,
             Lookup.DELAY_INTERVAL);
}

/**
 * wrap words in the string by html span tag
 * @param {string}
 * @return {HTML DOM element}
 */
MainView.wrapWordsBySpan = function(string) {
  if (string.length == 0) {
    console.log('in wrapWordsInSpan: string length == 0');
    return document.createTextNode('');
  }
  var nonWordChars = '.,;()‘’–-? 1234567890…';
  var startPos = 0;

  var isWordChar = false;
  if (nonWordChars.indexOf(string.charAt(0)) < 0 )
    isWordChar = true;

  var container = document.createElement('span');
  for (var i=1; i<string.length; i++) {
    if (nonWordChars.indexOf(string.charAt(i)) < 0 ) {
      // this is a word char
      if (isWordChar == false) {
        var substr = string.slice(startPos, i);
        container.appendChild(document.createTextNode(substr));
        startPos = i;
        isWordChar = true;
      }
    } else {
      // this is not a word char
      if (isWordChar == true) {
        var spanElem = document.createElement('span');
        spanElem.innerHTML = string.slice(startPos, i);
        spanElem.onmouseover = onWordMouseOver;
        spanElem.onmouseout = onWordMouseOut;
        spanElem.ondblclick = onWordDbclick;
        container.appendChild(spanElem);
        startPos = i;
        isWordChar = false;
      }
    }
  }

  if (isWordChar == true) {
    var spanElem = document.createElement('span');
    spanElem.innerHTML = string.slice(startPos);
    spanElem.onmouseover = onWordMouseOver;
    spanElem.onmouseout = onWordMouseOut;
    spanElem.ondblclick = onWordDbclick;
    container.appendChild(spanElem);
  } else {
    var substr = string.slice(startPos);
    container.appendChild(document.createTextNode(substr));
  }

  return container;
};

/**
 * wrap all words in the element
 * @param {DOM element} FIXME: is this HTML or XML dom element?
 */
MainView.wrapWordsInElement = function(xmlElement) {
  // 1: element node
  if (xmlElement.nodeType == 1) {
    for (var i=0; i<xmlElement.childNodes.length; i++)
      MainView.wrapWordsInElement(xmlElement.childNodes[i]);
    return;
  }

  // 3: text node
  if (xmlElement.nodeType == 3) {
    // wrap all words in span here
    var wrapedWords = MainView.wrapWordsBySpan(xmlElement.nodeValue);
    if (xmlElement.parentNode)
      xmlElement.parentNode.replaceChild(wrapedWords, xmlElement);
    else
      xmlElement = wrapedWords;
    return;
  }

  console.log('at the end of MainView.wrapWordsInElement');
  console.log(xmlElement);
};

/**
 * transform xml dom element to html dom element (not by xslt)
 * @param {XML DOM element}
 * @return {HTML DOM element}
 */
MainView.transformXmlElement = function(xmlElement) {
  // 1: element node
  if (xmlElement.nodeType == 1) {
    // element node AND tag == p
    if (xmlElement.tagName.toLowerCase() == 'p') {
      var pElem = document.createElement('p');

      if (xmlElement.getAttribute('rend') == 'centre')
        pElem.className = "centered";
      else
        pElem.className = xmlElement.getAttribute('rend');

      if (xmlElement.getAttribute('n')) {
        var aElem = document.createElement('a');
        aElem.name = 'para' + xmlElement.getAttribute('n');
        pElem.appendChild(aElem);
      }

      // recursively process childs
      for (var i=0; i<xmlElement.childNodes.length; i++)
        pElem.appendChild(MainView.transformXmlElement(xmlElement.childNodes[i]));

      return pElem;
    }

    // element node AND tag == hi
    if (xmlElement.tagName.toLowerCase() == 'hi') {
      var spanElem = document.createElement('span');

      if (xmlElement.getAttribute('rend') == 'dot') {}
      else if (xmlElement.getAttribute('rend') == 'bold')
        spanElem.className = 'bld';
      else
        spanElem.className = xmlElement.getAttribute('rend');

      // recursively process childs
      for (var i=0; i<xmlElement.childNodes.length; i++)
        spanElem.appendChild(MainView.transformXmlElement(xmlElement.childNodes[i]));

      return spanElem;
    }

    // element node AND tag == pb
    if (xmlElement.tagName.toLowerCase() == 'pb') {
      if (xmlElement.childNodes.length != 0)
        console.log('tag pb child # != 0');

      var aElem = document.createElement('a');
      aElem.name = xmlElement.getAttribute('ed') + xmlElement.getAttribute('n');
      return aElem;
    }

    // element node AND tag == note
    if (xmlElement.tagName.toLowerCase() == 'note') {
      var spanElem = document.createElement('span');
      spanElem.className = 'note';

      spanElem.appendChild(document.createTextNode('['));

      // recursively process childs
      for (var i=0; i<xmlElement.childNodes.length; i++)
        spanElem.appendChild(MainView.transformXmlElement(xmlElement.childNodes[i]));

      spanElem.appendChild(document.createTextNode(']'));

      return spanElem;
    }

    console.log('In MainView.transformXmlElement: at the end of element node processing');
    console.log(xmlElement);
    return document.createTextNode('');
  }

  // 3: text node
  if (xmlElement.nodeType == 3)
    return document.createTextNode(xmlElement.nodeValue);

  console.log('at the end of MainView.transformXmlElement');
  console.log(xmlElement);
  return document.createTextNode('');
};

MainView.showXmlDoc = function(xmlDoc, url) {
  var container = document.createElement('div');
  container.style.padding = '1em';
  container.style.backgroundColor = '#F0F8FF';
  container.style.minHeight = '100%';

  container.appendChild(MainView.getXmlDocTranslationLink(url));

  var body = xmlDoc.getElementsByTagName('body')[0];
  for (var i=0; i<body.childNodes.length; i++) {
    if (MainView.isMSIE())
      var tmp = MainView.transformXmlElement(body.childNodes[i]);
    else
      var tmp = body.childNodes[i].cloneNode(true);

    if (pali.startswith(url, '/romn/cscd/'))
      // This is a pali document => wrap words
      MainView.wrapWordsInElement(tmp);

    container.appendChild(tmp);
  }

  MainView.showOnMainView(container);
};

MainView.transformXmlWithXslt = function(xmlDoc, xsltDoc) {
  // transform xml using xslt.
  // @see http://www.w3schools.com/xsl/xsl_client.asp
  // @see http://stackoverflow.com/questions/5722410/how-can-i-use-javascript-to-transform-xml-xslt
  var transformedXML;

  if (window.XSLTProcessor) {
    transformedXML = new XSLTProcessor();
    transformedXML.importStylesheet(xsltDoc);
    transformedXML = transformedXML.transformToDocument(xmlDoc);
  } else {
    // for IE
    transformedXML = new ActiveXObject("MSXML2.DOMDocument");
    xmlDoc.transformNodeToObject(xsltDoc, transformedXML);
  }

  return transformedXML;
};

MainView.parsePaliXmlDoc = function(xmlDoc, url) {
  if (!MainView.cache.hasOwnProperty(url))
    MainView.cache[url] = xmlDoc;

  if (MainView.isMSIE()) {
    MainView.showXmlDoc(xmlDoc, url);
  } else {
    var urlXslt = '/romn/cscd/tipitaka-latn.xsl';

    // if no xslt in cache
    if (!MainView.cache.hasOwnProperty(urlXslt)) {
      // get xslt and re-run this function again
      pali.httpGetXml(urlXslt, function(xsltDoc, xsltUrl) {
        MainView.cache[xsltUrl] = xsltDoc;
        MainView.parsePaliXmlDoc(xmlDoc, url);
      });

      return;
    }

    var xsltDoc = MainView.cache[urlXslt];
    MainView.showXmlDoc(MainView.transformXmlWithXslt(xmlDoc, xsltDoc), url);
  }
};


// this variable should be the same as the 'translationInfo' variable in canonUrl.py
MainView.translationInfo = {
'zh_TW': {
  'canon': {
    's0502m.mul0.xml': ['2'],
    's0502m.mul1.xml': ['2'],
    's0502m.mul2.xml': ['2'],
    's0502m.mul3.xml': ['2'],
    's0502m.mul4.xml': ['2'],
    's0505m.mul0.xml': ['1']
  },
  'source': {
    '1': ['郭良鋆', 'http://blog.yam.com/benji/article/34665984'],
    '2': ['了參法師(葉均)', 'http://nt.med.ncku.edu.tw/biochem/lsn/Tipitaka/Sutta/Khuddaka/Dhammapada/Dhammapada.htm'],
    '3': ['蕭式球', 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5']
  }
},
'en_US': {
  'canon': {
    's0502m.mul0.xml': ['1'],
    's0502m.mul1.xml': ['1'],
    's0502m.mul2.xml': ['1'],
    's0502m.mul3.xml': ['1'],
    's0502m.mul4.xml': ['1']
  },
  'source': {
    // FIXME: use 3 instead of 1?
    '1': ['Ṭhānissaro Bhikkhu', 'http://www.accesstoinsight.org/tipitaka/translators.html#than', 'http://www.accesstoinsight.org/lib/authors/thanissaro/dhammapada.pdf']
  }
}
};
MainView.translationInfo['zh_CN'] = MainView.translationInfo['zh_TW'];

MainView.getOriginalPaliLink = function(xmlFilename) {
  var container = document.createElement('div');
  container.appendChild(document.createTextNode('<< '));

  var aOri = document.createElement('a');
  aOri.id = 'oriPali';
  aOri.name = xmlFilename;
  aOri.href = 'javascript:void(0);';
  aOri.innerHTML = 'Original Pāḷi Text';
  aOri.onclick = function() {
    MainView.loadPaliXmlDoc(this.name, '');
  };
  container.appendChild(aOri);

  return container;
};

MainView.getTranslationItem = function(xmlFilename, locale , source) {
  var container = document.createElement('div');
  container.style.paddingLeft = '1em';
  var translator = MainView.translationInfo[locale]['source'][source][0];

  var aTr = document.createElement('a');
  aTr.href = 'javascript:void(0);';
  aTr.name = xmlFilename + '%' + locale + '%' + source;
  aTr.onclick = function() {
    var localeAndSource = this.name.split('%');
    MainView.loadPaliXmlDoc(localeAndSource[0], '', true, localeAndSource[1], localeAndSource[2]);
  };
  aTr.appendChild(document.createTextNode(translator));

  var aCr = document.createElement('a');
  aCr.href = 'javascript:void(0);';
  aCr.onclick = function() {
    MainView.contrastReading(xmlFilename, locale, source, '');
  };
  aCr.appendChild(document.createTextNode('Contrast Reading'));

  container.appendChild(aTr);
  container.appendChild(document.createTextNode(' ('));
  container.appendChild(aCr);
  container.appendChild(document.createTextNode(')'));

  return container;
};

MainView.getAllLocaleTranslation = function(locale) {
  var container = document.createElement('div');
  container.style.paddingLeft = '1em';
  container.style.paddingBottom = '1em';

  for (var xmlFilename in MainView.translationInfo[locale]['canon']) {
    var aName = document.createElement('a');
    aName.href = 'javascript:void(0);';
    aName.name = xmlFilename;
    aName.onclick = function() {
      MainView.loadPaliXmlDoc(this.name, '');
    };
    // FIXME: translate xmlFilename to canon name
    aName.appendChild(document.createTextNode(
             MainView.xmlFilename2CanonName(xmlFilename)));

    var itemContainer = document.createElement('div');
    itemContainer.style.paddingLeft = '1em';
    itemContainer.style.marginTop = '.25em';
    itemContainer.style.border = '1px dotted #E0E0E0';
    itemContainer.appendChild(aName);
    itemContainer.appendChild(document.createTextNode(':'));

    var sources = MainView.translationInfo[locale]['canon'][xmlFilename];

    for (var i=0; i<sources.length; i++)
      itemContainer.appendChild(MainView.getTranslationItem(xmlFilename, locale , sources[i]));

    container.appendChild(itemContainer);
  }

  if (container.childNodes.length == 0)
    return document.createTextNode('');
  else {
    var aLocale = document.createElement('a');
    aLocale.href = 'javascript:void(0);';
    aLocale.name = locale;
    aLocale.onclick = function() {
      MainView.showAllLocaleTranslation(this.name);
    };
    aLocale.appendChild(document.createTextNode(locale));

    container.insertBefore(document.createTextNode(':'), container.firstChild);
    container.insertBefore(aLocale, container.firstChild);
  }

  return container;
};

MainView.showAllLocaleTranslation = function(locale) {
  var container = document.createElement('div');
  container.id = 'localeTranslationDiv';

  container.appendChild(document.createTextNode('<< '));
  var aAllTr = document.createElement('a');
  aAllTr.href = 'javascript:void(0);';
  aAllTr.innerHTML = 'See All Translation';
  aAllTr.onclick = function() {
    var container = document.createElement('div');
    container.style.minHeight = '100%';
    container.style.padding = '1em';
    container.style.backgroundColor = '#F0F8FF'
    container.appendChild(MainView.getAllTranslation());
    MainView.showOnMainView(container);
  };

  container.appendChild(aAllTr);
  container.appendChild(document.createElement('br'));
  container.appendChild(document.createElement('br'));

  var localeDiv = MainView.getAllLocaleTranslation(locale);
  if (localeDiv.nodeType == 3)
    // no translation in this locale
    localeDiv.nodeValue = 'No translation in this locale';
  container.appendChild(localeDiv);

  MainView.showOnMainView(container);
};

/**
 * @return {DOM element} html dom element which contains all available translations
 */
MainView.getAllTranslation = function() {
  var ht = document.createElement('div');
  ht.id = 'htmlTranslation';

  ht.appendChild(document.createElement('h3'));
  ht.lastChild.innerHTML = 'All Translations';
  ht.lastChild.style.color = 'olive';

  // there is translation(s) for this xml file
  for (var locale in MainView.translationInfo) {
    var localeDiv = MainView.getAllLocaleTranslation(locale);
    if (localeDiv.nodeType == 3)
      // no translation in this locale
      continue;

    ht.appendChild(localeDiv);
  }

  // FIXME: sort all translations according to user locale here

  return ht;
};

MainView.showXmlDocLocaleTranslation = function(xmlFilename, locale) {
  var container = document.createElement('div');
  container.id = 'localeTranslationDiv';

  container.appendChild(MainView.getOriginalPaliLink(xmlFilename));
  container.appendChild(document.createElement('br'));

  if (MainView.translationInfo[locale]['canon'].hasOwnProperty(xmlFilename)) {
    var sources = MainView.translationInfo[locale]['canon'][xmlFilename];

    for (var i=0; i<sources.length; i++)
      container.appendChild(MainView.getTranslationItem(xmlFilename, locale , sources[i]));
  }

  MainView.showOnMainView(container);
};

/**
 * When users click on xml file on the left side tree view, show translation of
 * xml file if there is available translation. This function returns the
 * available translation links of the xml file that users click on
 * @param {string} url The url of the xml file
 * @return {HTML DOM element} The dom elements which contains the translation
 *                            links if any.
 */
MainView.getXmlDocTranslationLink = function(url) {
  var xmlFilename = pali.basename(url);

  // check whether there is translation(s) for this xml file
  var isThereTranslation = false;
  for (var locale in MainView.translationInfo) {
    if (MainView.translationInfo[locale]['canon'].hasOwnProperty(xmlFilename)) {
      isThereTranslation = true;
      break;
    }
  }

  // there is no translation for this xml file
  if (!isThereTranslation) return document.createTextNode('');

  if (pali.startswith(url, '/translation/'))
    return MainView.getOriginalPaliLink(xmlFilename);

  var ht = document.createElement('div');
  ht.id = 'htmlTranslation';
  // there is translation(s) for this xml file
  for (var locale in MainView.translationInfo) {
    if (MainView.translationInfo[locale]['canon'].hasOwnProperty(xmlFilename)) {
      var sources = MainView.translationInfo[locale]['canon'][xmlFilename];

      var trContainer = document.createElement('div');
      trContainer.style.paddingLeft = '1em';
      for (var i=0; i<sources.length; i++)
        trContainer.appendChild(MainView.getTranslationItem(xmlFilename, locale , sources[i]));

      var aLocale = document.createElement('a');
      aLocale.href = 'javascript:void(0);';
      aLocale.name = locale;
      aLocale.onclick = function() {
        MainView.showXmlDocLocaleTranslation(xmlFilename, this.name);
      };
      aLocale.appendChild(document.createTextNode(locale));

      ht.appendChild(aLocale);
      ht.appendChild(document.createTextNode(':'));
      ht.appendChild(trContainer);
    }
  }
  var st = document.createElement('div');
  st.id = 'showTranslation';
  st.appendChild(document.createElement('span'));
  st.lastChild.innerHTML = '&#9658;';
  st.appendChild(document.createElement('span'));
  st.lastChild.innerHTML = 'See Translation of this Pāḷi Text';

  st.onclick = function() {
    if (ht.style.display == 'none') {
      ht.style.display = 'block';
      st.firstChild.innerHTML = '&#9660;';
    }
    else {
      ht.style.display = 'none';
      st.firstChild.innerHTML = '&#9658;';
    }
  };
  ht.style.display = 'none';

  var container = document.createElement('div');
  container.appendChild(st);
  container.appendChild(ht);

  return container;
};

/**
 * @param{string} xmlFilename The file name of pali texts xml
 * @param{string} locale {en_US|zh_TW|zh_CN}
 * @param{string} source Key in MainView.translationInfo['source']
 */
MainView.contrastReading = function(xmlFilename, locale, source, title) {
  MainView.showLoading(title);

  var urltr = MainView.getTranslationUrl(xmlFilename, locale, source);
  var urlpali = MainView.getPaliUrl(xmlFilename);

  if ( MainView.cache.hasOwnProperty(urlpali) &&
       MainView.cache.hasOwnProperty(urltr) ) {
    MainView.processCRXmlDoc(MainView.cache[urlpali], MainView.cache[urltr], xmlFilename);
    return;
  }

  if (!MainView.cache.hasOwnProperty(urltr)) {
    if (locale == 'zh_CN')
      urltr = urltr.replace('zh_CN', 'zh_TW');
    pali.httpGetXml(urltr, function(xmlDoc, url) {
      if (locale == 'zh_CN') {
        url = url.replace('zh_TW', 'zh_CN');
        i18n.xmlDoc2CN(xmlDoc);
      }
      MainView.cache[url] = xmlDoc;
      MainView.contrastReading(xmlFilename, locale, source, title);
    });
    return;
  }

  if (!MainView.cache.hasOwnProperty(urlpali)) {
    pali.httpGetXml(urlpali, function(xmlDoc, url) {
      MainView.cache[url] = xmlDoc;
      MainView.contrastReading(xmlFilename, locale, source, title);
    });
    return;
  }
};

MainView.showCRXmlDoc = function(paliXmlDoc, trXmlDoc, xmlFilename) {
  var container = document.createElement('div');
  container.style.padding = '1em';
  container.style.backgroundColor = '#F0F8FF';
  container.style.minHeight = '100%';

  container.appendChild(MainView.getOriginalPaliLink(xmlFilename));

  var paliBody = paliXmlDoc.getElementsByTagName('body')[0];
  var trBody = trXmlDoc.getElementsByTagName('body')[0];

  if (paliBody.childNodes.length != trBody.childNodes.length)
    console.log('two XML document body childs # not match');

  var length = Math.min(paliBody.childNodes.length,
                        trBody.childNodes.length);

  var tb = document.createElement('table');
  tb.style.width = '100%';
  for (var i=0; i<length; i++) {
    // FIXME
    if (paliBody.childNodes[i].nodeType != 1 &&
        trBody.childNodes[i].nodeType != 1) {
      continue;
    }

    if (MainView.isMSIE()) {
      var paliElem = MainView.transformXmlElement(paliBody.childNodes[i]);
      var trElem = MainView.transformXmlElement(trBody.childNodes[i]);
    } else {
      var paliElem = paliBody.childNodes[i].cloneNode(true);
      var trElem = trBody.childNodes[i].cloneNode(true);
    }
    MainView.wrapWordsInElement(paliElem);

    var td1 = document.createElement('td');
    td1.appendChild(paliElem);
    td1.style.width = '50%';

    var td2 = document.createElement('td');
    td2.appendChild(trElem);
    td2.style.width = '50%';

    var tr = document.createElement('tr');
    tr.style.textAlign = 'left';
    tr.appendChild(td1);
    tr.appendChild(td2);

    tb.appendChild(tr);
  }
  container.appendChild(tb);

  MainView.showOnMainView(container);
};

MainView.processCRXmlDoc = function(paliXmlDoc, trXmlDoc, xmlFilename) {
  if (MainView.isMSIE()) {
    MainView.showCRXmlDoc(paliXmlDoc, trXmlDoc, xmlFilename);
  } else {
    var urlXslt = '/romn/cscd/tipitaka-latn.xsl';

    // if no xslt in cache
    if (!MainView.cache.hasOwnProperty(urlXslt)) {
      // get xslt and re-run this function again
      pali.httpGetXml(urlXslt, function(xsltDoc, xsltUrl) {
        MainView.cache[xsltUrl] = xsltDoc;
        MainView.processCRXmlDoc(paliXmlDoc, trXmlDoc, xmlFilename);
      });

      return;
    }

    var xsltDoc = MainView.cache[urlXslt];
    MainView.showCRXmlDoc(MainView.transformXmlWithXslt(paliXmlDoc, xsltDoc),
                          MainView.transformXmlWithXslt(trXmlDoc, xsltDoc),
                          xmlFilename);
  }
};


MainView.canonName = {
's0505m.mul0.xml': {
  'pali': 'Suttanipāta, Uragavaggo',
  'zh_TW': '經集, 蛇品'
},
's0502m.mul0.xml': {
  'pali': 'Dhammapada, Yamakavaggo',
  'en_US': 'Dhammapada, Pairs',
  'zh_TW': '法句, 雙品'
},
's0502m.mul1.xml': {
  'pali': 'Dhammapada, Appamādavaggo',
  'en_US': 'Dhammapada, Heedfulness',
  'zh_TW': '法句, 不放逸品'
},
's0502m.mul2.xml': {
  'pali': 'Dhammapada, Cittavaggo',
  'en_US': 'Dhammapada, The Mind',
  'zh_TW': '法句, 心品'
},
's0502m.mul3.xml': {
  'pali': 'Dhammapada, Pupphavaggo',
  'en_US': 'Dhammapada, Blossoms',
  'zh_TW': '法句, 華(花)品'
},
's0502m.mul4.xml': {
  'pali': 'Dhammapada, Bālavaggo',
  'en_US': 'Dhammapada, Fools',
  'zh_TW': '法句, 愚品'
}
};

MainView.xmlFilename2CanonName = function(xmlFilename, opt_locale) {
  if (MainView.canonName.hasOwnProperty(xmlFilename)) {
    if (opt_locale) {
      if (MainView.canonName[xmlFilename].hasOwnProperty(opt_locale))
        return MainView.canonName[xmlFilename][opt_locale];
    }
    return MainView.canonName[xmlFilename]['pali'];
  }

  return xmlFilename;
};


/**
 * Check whether user browser is MSIE
 * @return {boolean} true if user browser is MSIE. false otherwise.
 */
MainView.isMSIE = function() {
  return navigator.userAgent.indexOf('MSIE') != -1;
};
