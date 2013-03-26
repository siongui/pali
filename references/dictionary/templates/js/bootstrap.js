/* Reference: http://ntt.cc/2008/02/10/4-ways-to-dynamically-load-external-javascriptwith-source.html */
function LoadJS(url) {
  var ext = document.createElement('script');
  ext.setAttribute("type","text/javascript");
  ext.setAttribute("src", url);
  document.getElementsByTagName("head")[0].appendChild(ext);
}

function LoadCSS(url) {
  var ext = document.createElement('link');
  ext.setAttribute("type", "text/css");
  ext.setAttribute("rel", "stylesheet");
  ext.setAttribute("href", url);
  document.getElementsByTagName("head")[0].appendChild(ext);
}

function LoadFavicon(url) {
  var ext = document.createElement('link');
  ext.setAttribute("rel", "shortcut icon");
  ext.setAttribute("href", url);
  document.getElementsByTagName("head")[0].appendChild(ext);
}

/*
keyword: javascript get url parameter 
http://stackoverflow.com/questions/979975/how-to-get-the-value-from-url-parameter
http://stackoverflow.com/questions/1403888/get-url-parameter-with-jquery
http://papermashup.com/read-url-get-variables-withjavascript/
*/
window['queryURL'] = (function() {
  // This function is anonymous, is executed immediately and the return value is assigned to queryURL
  var queryPairs = {};
  if (!window.location.search) {return queryPairs;}
  var variables = window.location.search.substring(1).split("&");
  for (var i=0; i < variables.length; i++) {
    /* http://stackoverflow.com/questions/747641/what-is-the-difference-between-decodeuricomponent-and-decodeuri */
    var pair = decodeURIComponent(variables[i]).split("=");
    if (pair.length != 2) {console.log('strange query string: '+variables[i]);continue;}
    if (typeof pair[0] == "undefined") {
      continue;
    } else if (typeof pair[0] == null) {
      continue;
    } else {
      queryPairs[pair[0]] = pair[1];
    }
  }
  return queryPairs;
})();

if (window.location.host == 'siongui.pythonanywhere.com' || window.location.host == 'siongui.webfactional.com') {
  if (queryURL['redirect'] != 'no') {
    var cb = function() {
      window.location = 'http://palidictionary.appspot.com' + window.location.pathname + window.location.search;
    };
    var qry = '?callback=' + encodeURIComponent('('+cb.toString()+')');
    var ext = document.createElement('script');
    ext.setAttribute('src', 'http://palidictionary.appspot.com/lookup' + qry);
    document.getElementsByTagName("head")[0].appendChild(ext);
  }
}

/* Load Google Web Fonts */
LoadCSS("http://fonts.googleapis.com/css?family=Gentium+Basic|Special+Elite&subset=latin,latin-ext");
/* Load JS, CSS and Favicon */
if (queryURL['ugcfh'] == "yes") {
  /* use google code to serve files */
  var prefix = 'http://pali.googlecode.com/git/static/';
  LoadCSS(    prefix + "css/palidict.css");
  LoadFavicon(prefix + "favicon.ico");
  LoadJS(     prefix + "jsonPrefixWords.js");
  LoadJS(     prefix + "js/jsdeploader.js");
} else {
  LoadCSS(    "/css/palidict.css");
  LoadFavicon("/favicon.ico");
  LoadJS(     "/js/jsonPrefixWords.js");
  if (queryURL['compiledjs'] == 'yes' || window.location.host != 'localhost:8080') {
    LoadJS(   "/js/pali-prd.js");
  }
  else {
    LoadJS(   "/js/jsdeploader.js");
  }
}
