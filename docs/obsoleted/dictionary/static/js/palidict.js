pali.require('base');
pali.require('data2dom');
pali.require('dropdown');
pali.require('draggable');
pali.require('inputsuggest');
pali.require('lookup');

if (queryURL['track'] != "no") {
  if (window.location.host != 'localhost:8080') {
  /* Load Google Analytics Code */
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-32179549-1']);
_gaq.push(['_trackPageview']);
(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
  }
}

// check if dom is ready enough to do initService()
if (window.opera) {
  checkOpera();
} else {
  checkOtherBrowsers();
}

function checkOpera() {
  if (document.readyState == "complete") initService();
  else setTimeout(checkOpera, 50);
}

function checkOtherBrowsers() {
  if (document.getElementById('locale')) initService();
  else setTimeout(checkOtherBrowsers, 50);
}

function initService() {
  // start input suggest
  var suggest = new pali.InputSuggest("PaliInput", "suggest");

  // start dropdown menu
  var langDropdown = new pali.Dropdown('lang-dropdown', 'menuDiv-lang-dropdown');
  var siteDropdown = new pali.Dropdown('site-dropdown', 'menuDiv-site-dropdown');

  // start lookup object and callback
  var myLookup = new Lookup('PaliInput', 'inputForm', 'result',
                            'suggestedWordPreview', 'suggest',
                            getLookupUrl(), getLookupMethod(),
                            'leftHistoryArrow', 'rightHistoryArrow');

  // check which site user is at, and fill site innerHTML
  if (window.location.host == 'siongui.pythonanywhere.com')
    {document.getElementById('site').innerHTML = getStringBackupSite1();}
  else if (window.location.host == 'siongui.webfactional.com')
    {document.getElementById('site').innerHTML = getStringBackupSite2();}
  else {document.getElementById('site').innerHTML = getStringMainSite();}
  document.getElementById('site').style.wordSpacing = "normal";

  // check user's locale, and fill lang innerHTML
  var locale = document.getElementById('locale').innerHTML.split('~')[0];
  if (locale == 'zh_CN') {document.getElementById('lang').innerHTML = '中文 (简体)';}
  else if (locale == 'zh_TW') {
    document.getElementById('lang').innerHTML = '中文 (繁體)';
    document.getElementById('toTraditionalCht').checked = true;
  } else {document.getElementById('lang').innerHTML = 'English';}
  document.getElementById('lang').style.wordSpacing = "normal";

  /**
   * make keypad toggle-able (show if hidden, hide if shown)
   * @this {DOM Element} Here refer to the element with id='displayText'
   */
  document.getElementById('displayText').onclick = function() {
    var kb = document.getElementById("keyboard");
    if(kb.style.display == "block") {
      kb.style.display = "none";
      this.innerHTML = getStringShowKeypad();
    }
    else {
      kb.style.display = "block";
      this.innerHTML = getStringHideKeypad();
      kb.style.left = pali.getOffset(this).left + "px";
    }
  };

  // make keypad draggable
  var drag = new pali.Draggable('keyboard');

  // bind the click function of input element inside keypad
  var keypad = document.getElementById('keyboard');
  var buttons = keypad.getElementsByTagName('input');
  for (var i=0; i < buttons.length; i++) {
    /**
     * @this {DOM Element} Here refer to the button element
     */
    buttons[i].onclick = function() {
      document.getElementById("PaliInput").value += this.value;
      document.getElementById("PaliInput").focus();
    };
  }

  document.getElementById('linkHome').href = "javascript:void(0);";
  document.getElementById('linkHome').onclick = function() {
    window.location = "/" + window.location.search;
  };

  document.getElementById('linkBrowse').href = "javascript:void(0);";
  document.getElementById('linkBrowse').onclick = function() {
    document.getElementById("result").innerHTML = "";
  };

  document.getElementById('linkSetting').href = "javascript:void(0);";
  document.getElementById('linkSetting').onclick = function() {
    var st = document.getElementById("setting-menu");
    if (st.style.display == 'block') st.style.display = 'none';
    else st.style.display = 'block';
  };
  /**
   * @this {DOM Element} Here refer to the checkbox element
   */
  document.getElementById('word-preview-option').onchange = function() {
    if (this.checked) myLookup.enableWordPreview();
    else myLookup.disableWordPreview();
  };

  document.getElementById('linkAbout').href = "javascript:void(0);";
  document.getElementById('linkAbout').onclick = function() {
    document.getElementById("result").innerHTML =
    document.getElementById("about").innerHTML;
  };

  document.getElementById('linkLink').href = "javascript:void(0);";
  document.getElementById('linkLink').onclick = function() {
    document.getElementById("result").innerHTML =
    document.getElementById("link").innerHTML;
  };

  document.getElementById('siteItem1').href = "javascript:void(0);";
  document.getElementById('siteItem1').onclick = onSiteClick;
  document.getElementById('siteItem2').href = "javascript:void(0);";
  document.getElementById('siteItem2').onclick = onSiteClick;
  document.getElementById('siteItem3').href = "javascript:void(0);";
  document.getElementById('siteItem3').onclick = onSiteClick;

  document.getElementById('langItem1').href = "javascript:void(0);";
  document.getElementById('langItem1').onclick = onLocaleClick;
  document.getElementById('langItem2').href = "javascript:void(0);";
  document.getElementById('langItem2').onclick = onLocaleClick;
  document.getElementById('langItem3').href = "javascript:void(0);";
  document.getElementById('langItem3').onclick = onLocaleClick;

  initBrowseLinks();

  document.getElementById('PaliInput').focus();
  if (window.location.host == 'localhost:8080') {
    document.getElementById('toTraditionalCht').checked = true;
    document.getElementById('word-preview-option').checked = true;
    myLookup.enableWordPreview();
  }
}

/**
 * Browse Dictionary in AJAX way
 */
function initBrowseLinks() {
  if (queryURL['ajaxbrowse'] == 'no') {
    return;
  }

  var brdic = document.getElementById('brdic');
  var prefixes = brdic.getElementsByTagName('a');
  for (var i=0; i < prefixes.length; i++) {
    prefixes[i].href = 'javascript:void(0);';
    prefixes[i].onclick = onBrowsePrefixClick;
  }

  var prefixWordsList = document.getElementById('prefixWordsList');
  if (!prefixWordsList) return;
  var prefixWords = prefixWordsList.getElementsByTagName('a');
  for (var i=0; i < prefixWords.length; i++) {
    prefixWords[i].href = 'javascript:void(0);';
    prefixWords[i].onclick = onBrowseWordClick;
  }
}

/**
 * @this {DOM Element}
 */
function onBrowsePrefixClick() {
  if (!dicPrefixWordLists) return;
  if (!dicPrefixWordLists.hasOwnProperty(this.innerHTML))
    throw "Impossible Case in onBrowsePrefixClick";

  var container = Data2dom.createWordsList(dicPrefixWordLists[this.innerHTML]);
  var aElems = container.getElementsByTagName('a');
  for (var i=0; i < aElems.length; i++) {
    aElems[i].href = 'javascript:void(0);';
    aElems[i].onclick = onBrowseWordClick;
  }

  document.getElementById('result').innerHTML = '';
  document.getElementById('result').appendChild(container);
}

/**
 * @this {DOM Element}
 */
function onBrowseWordClick() {
  document.getElementById('result').innerHTML = getStringLookingUp();
  var word = this.title;
  var method = getLookupMethod();
  if (method == 'jsonp') {
    Lookup.jsonp(word, getLookupUrl(), 
      '('+ onBrowseWordClickCallback.toString() +')');
  } else if (method == 'post') {
    var failCallback = function() {
      document.getElementById('result').innerHTML = 'XMLHttpRequest Post Err!';
      throw "XMLHttpRequest Post Err!";
    };
    Lookup.httppost(word, getLookupUrl(),
                    onBrowseWordClickCallback, failCallback);
  } else {
    var failCallback = function() {
      document.getElementById('result').innerHTML = getStringNoSuchWord();
      throw 'In onBrowseWordClick: http get failed';
    };
    Lookup.httpget(word, onBrowseWordClickCallback, failCallback);
  }
}

var onBrowseWordClickCallback = function(jsonData) {
  document.getElementById('result').innerHTML = '';
  document.getElementById('result').appendChild(
    Data2dom.createLookupTable(jsonData));
};

/**
 * @this {DOM Element}
 */
function onSiteClick() {
  var url = window.location.pathname;
  if (this.id == 'siteItem2') { url = 'http://siongui.pythonanywhere.com' + url; }
  else if (this.id == 'siteItem3') { url = 'http://siongui.webfactional.com' + url; }
  else { url = 'http://palidictionary.appspot.com' + url; }

  if (window.location.host == 'localhost:8080' ||
      window.location.host == 'pali.googlecode.com') {
    queryURL['track'] = 'no';
    queryURL['redirect'] = 'no';
  }

  var count = 0;
  for (var key in queryURL) {
    if (count == 0) { url += '?' + key + '=' + queryURL[key]; }
    else { url += '&' + key + '=' + queryURL[key]; }
    count ++;
  }

  window.location = url;
}

/**
 * @this {DOM Element}
 */
function onLocaleClick() {
  var locale = '';
  if (this.id == 'langItem2') { locale = 'zh_CN'; }
  else if (this.id == 'langItem3') { locale = 'zh_TW'; }
  else { locale = 'en_US'; }

  queryURL['locale'] = locale;
  var count = 0;
  var url = window.location.pathname;
  for (var key in queryURL) {
    if (count == 0) { url += '?' + key + '=' + queryURL[key]; }
    else { url += '&' + key + '=' + queryURL[key]; }
    count ++;
  }

  window.location = url;
}

function getLookupUrl() {
  if (queryURL['lookup'] == "gae")
    return "http://palidictionary.appspot.com/lookup";
  if (queryURL['lookup'] == "paw")
    return "http://siongui.pythonanywhere.com/lookup";
  if (queryURL['lookup'] == "wfn")
    return "http://siongui.webfactional.com/lookup";
  return "/lookup";
}

function getLookupMethod() {
  if (queryURL['method'] == "jsonp") return 'jsonp';
  if (queryURL['method'] == "post") return 'post';
  if (queryURL['method'] == "get") return 'get';
  return 'get';
}
