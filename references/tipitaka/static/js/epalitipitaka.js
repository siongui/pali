function initService() {
  var width = document.getElementById('wrapper').offsetWidth;

  var treeviewWidth = 16*15;
  var viewwrapperWidth = 7;
  var mainviewWidth = width - treeviewWidth - viewwrapperWidth;

  var treeview = document.getElementById('treeview');
  treeview.style.width = treeviewWidth + 'px';

  var viewwrapper = document.getElementById('viewwrapper');
  viewwrapper.style.width = viewwrapperWidth + 'px';

  var viewarrow = document.getElementById('viewarrow');
  viewarrow.style.borderTop = viewwrapperWidth + 'px solid transparent';
  viewarrow.style.borderBottom = viewwrapperWidth + 'px solid transparent';
  viewarrow.style.borderRight = viewwrapperWidth + 'px solid blue';

  var mainview = document.getElementById('mainview');
  mainview.style.width = mainviewWidth + 'px';

  if (window.location.pathname == '/') {
    // user visits home url. show About and Translation
    mainview.appendChild(document.getElementById('aboutDiv').getElementsByTagName('div')[0].cloneNode(true));
    mainview.lastChild.appendChild(MainView.getAllTranslation());
    mainview.lastChild.lastChild.style.marginTop = '1em';
    mainview.lastChild.lastChild.style.textAlign = 'left';
  } else {
    // for testing purpose
    if (queryURL['track'] == "no") {
      var aElems = mainview.getElementsByTagName('a');
      for (var i=0; i<aElems.length; i++) {
        if (aElems[i].href.indexOf('/canon') != -1)
          aElems[i].href += '?track=no';
      }
    }

    // make "See Translation" link toggle-able if there is such link
    var st = document.getElementById('showTranslation');
    if (st) {
      var ht = document.getElementById('htmlTranslation')
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
    }

    // wrap pali words in div with id "palitexts" if there is such div
    var pt = document.getElementById('palitexts');
    if (pt) MainView.wrapWordsInElement(pt);

    // wrap pali words in table with id "contrastReadingTable" if there is such table
    var crt = document.getElementById('contrastReadingTable');
    if (crt) {
      var trElems = crt.getElementsByTagName('tr');
      for (var i=0; i<trElems.length; i++)
        MainView.wrapWordsInElement(trElems[i].childNodes[0]);
    }
  }

  var mytreeview = new TreeView2('treeview');

  var movableCol = new MovableCol('treeview', 'viewarrow', 'viewseparator', 'mainview');

  var aboutAnchor = document.getElementById('aboutAnchor');
  aboutAnchor.href = 'javascript:void(0);';
  aboutAnchor.onclick = function() {
    mainview.innerHTML  = document.getElementById('aboutDiv').innerHTML;
  };

  var translationAnchor = document.getElementById('translationAnchor');
  translationAnchor.href = 'javascript:void(0);';
  translationAnchor.onclick = function() {
    var container = document.createElement('div');
    container.style.minHeight = '100%';
    container.style.padding = '1em';
    container.style.backgroundColor = '#F0F8FF'
    container.appendChild(MainView.getAllTranslation());
    MainView.showOnMainView(container);
  };

  var linkAnchor = document.getElementById('linkAnchor');
  linkAnchor.href = 'javascript:void(0);';
  linkAnchor.onclick = function() {
    mainview.innerHTML  = document.getElementById('linkDiv').innerHTML;
  };

  var settingAnchor = document.getElementById('settingAnchor');
  settingAnchor.href = "javascript:void(0);";
  settingAnchor.onclick = function() {
    var st = document.getElementById("settingmenu");
    if (st.style.display == 'block') st.style.display = 'none';
    else st.style.display = 'block';
  };

  // check user's locale, and fill lang innerHTML
  var locale = document.getElementById('locale').innerHTML.split('~')[0];
  // if user's locale is zh_TW, translate Chinese dictionary to Tradictional Chinese
  if (locale == 'zh_TW')
    document.getElementById('toTraditionalCht').checked = true;

  document.getElementById('translateTreeview').onclick = function() {
    if (this.checked)
      i18n.translateTreeView();
    else
      i18n.untranslateTreeView();
  };

  if(!i18n.setLocale(locale))
    throw 'init locale: something strange happen';
  i18n.translateDocument();

  var lang = document.getElementById('lang');
  lang.value = locale;
  lang.onchange = function() {
    if (i18n.getLocale() == this.value) return;
    if (!i18n.setLocale(this.value))
      throw 'In i18n.changeDocumentLanguage: set locale failed!';

    i18n.translateDocument();
  };

  // for testing purpose
  if (window.location.host == 'localhost:8080') {
    document.getElementById('toTraditionalCht').checked = true;
    document.getElementById('translateTreeview').checked = true;

    lang.value = 'zh_TW';
    if (!i18n.setLocale('zh_TW'))
      throw 'In i18n.changeDocumentLanguage: set locale failed!';
    i18n.translateDocument();

    var aElems = mainview.getElementsByTagName('a');
    for (var i=0; i<aElems.length; i++) {
      if (aElems[i].href == "http://palidictionary.appspot.com/")
        aElems[i].href += '?track=no';
    }
    var aElems = document.getElementById('mainbar').getElementsByTagName('a');
    aElems[0].href = 'http://epalitipitaka.appspot.com/?track=no';
    aElems[0].target = "_blank";
    aElems[1].href += '?track=no';
  }

  // All preliminery word done. make website visiable now.
  document.getElementById('hideAll').style.display = 'none';
}

initService();

if (queryURL['track'] != "no") {
  if (window.location.host != 'localhost:8080') {
    /* Load Google Analytics Code */
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-32179549-3']);
    _gaq.push(['_trackPageview']);

    (function() {
      var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
      ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
      var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    })();
  }
}
