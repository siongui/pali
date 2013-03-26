/**
 * @fileoverview treeview library
 */

pali.require('base');

/**
 * New implementation of TreeView library
 */
TreeView2 = function(idTreeViewDiv) {
  this.treeview_ = document.getElementById(idTreeViewDiv);
  if (!this.treeview_) throw 'tree view div error';

  if (!jsonTreeviewToc)
    throw 'no jsonTreeViewToc';

  var elems = TreeView2.traverseTree(jsonTreeviewToc);

  var treeRoot = document.createElement('div');
  var title = document.createElement('div');
  title.appendChild(document.createTextNode('Tipiṭaka (Mūla)'));
  title.style.paddingBottom = '.25em';
  treeRoot.appendChild(title);
  treeRoot.appendChild(elems);

  this.treeview_.insertBefore(treeRoot, this.treeview_.firstChild);
};

TreeView2.traverseTree = function(info) {
  if (typeof info != 'object')
    throw 'argument must be object';

  // @see http://stackoverflow.com/questions/4775722/javascript-check-if-object-is-array
  if( Object.prototype.toString.call( info ) == '[object Array]' ) {
    var container = document.createElement('div');
    container.style.marginLeft = '.4em';
    container.style.paddingLeft = '.4em';
    container.style.borderLeft = '1px dotted blue';

    for (var i=0; i<info.length; i++) {
      if (!info[i].hasOwnProperty('text'))
        throw 'items in array must has key "text"!';

      var title = document.createElement('div');
      title.className = 'item';

      title.appendChild(document.createTextNode('+'));

      var nodeName = document.createElement('span');
      nodeName.className = 'treeNode';
      // FIXME: use innerHTML?
      nodeName.appendChild(document.createTextNode(info[i]['text']));
      nodeName.onclick = TreeView2.onNodeclick;

      title.appendChild(nodeName);
      container.appendChild(title);

      var child = TreeView2.traverseTree(info[i]);
      child.style.display = 'none';
      container.appendChild(child);

      // remove + sign of leaf node
      if (child.tagName.toLowerCase() == 'span' &&
          child.style.cursor == 'pointer') {
        // leaf node
        title.firstChild.nodeValue = '';
      }
    }

    return container;
  }
  if (info.hasOwnProperty('text')) {
    if (info.hasOwnProperty('child')) {
      if (info.hasOwnProperty('action'))
        throw 'has both action and child';

      return TreeView2.traverseTree(info['child']);
    }

    if (info.hasOwnProperty('action')) {
      if (info.hasOwnProperty('child'))
        throw 'has both action and child';

      // this is a 'load canon' node
      var article = document.createElement('span');
      article.style.cursor = 'pointer';
      // FIXME: use innerHTML?
      article.appendChild(document.createTextNode(
        info['action'] + '%%%' + info['text']));
      return article;
    }

    throw 'has text, but no childs and action';
  }

  throw 'error: end of traverse tree';
};

/**
 * @this {Dom element}
 */
TreeView2.onNodeclick = function() {
  var pn = this.parentNode.nextSibling;
  if (pn.tagName.toLowerCase() == 'span' &&
      pn.style.cursor == 'pointer') {
    // pn is a 'load canon' node
    var fileAndCanonName = pn.innerHTML.split('%%%');
    MainView.loadPaliXmlDoc(pali.basename(fileAndCanonName[0]),
                            fileAndCanonName[1]);
    return;
  }
  if (pn.style.display == 'none') {
    this.previousSibling.nodeValue = '-';
    pn.style.display = 'block';
  }
  else {
    this.previousSibling.nodeValue = '+';
    pn.style.display = 'none';
  }
};



/**
 * @deprecated
 */
TreeView = function(tocFilename, idTreeViewDiv) {
  this.treeview_ = document.getElementById(idTreeViewDiv);
  if (!this.treeview_) throw 'tree view div error';

  this.loadRootTocXml(TreeView.getTocUrl(tocFilename));
};

TreeView.getTocUrl = function(filename) {
  return '/romn/toc/' + filename;
};

TreeView.prototype.loadRootTocXml = function(url) {
  pali.httpGetXml(url, this.parseRootTocXmlDoc.bind(this) );
};

TreeView.prototype.parseRootTocXmlDoc = function(xmlDoc, url) {
  var elems = TreeView.traverseTree(xmlDoc.documentElement);

  var treeRoot = document.createElement('div');
  var title = document.createElement('div');
  title.appendChild(document.createTextNode('Tipiṭaka (Mūla)'));
  title.style.paddingBottom = '.25em';
  treeRoot.appendChild(title);
  treeRoot.appendChild(elems);

  this.treeview_.insertBefore(treeRoot, this.treeview_.firstChild);
  i18n.translateTreeView();
};

TreeView.traverseTree = function(element) {
  // JavaScript XML processing
  // @see http://www.w3schools.com/dom/dom_examples.asp
  if (element.hasChildNodes()) {
    if (element.nodeType != 1)
      throw 'node has childs and node type != 1';

    var container = document.createElement('div');
    container.style.marginLeft = '.4em';
    container.style.paddingLeft = '.4em';
    container.style.borderLeft = '1px dotted blue';
    for (var i=0; i<element.childNodes.length; i++) {
      var child = TreeView.traverseTree(element.childNodes[i]);
      if (child.nodeType == 3) continue;
      if (child.nodeType == 8) continue;

      var title = document.createElement('div');
      title.className = 'item';

      title.appendChild(document.createTextNode('+'));

      var nodeName = document.createElement('span');
      nodeName.className = 'treeNode';
      // FIXME: use innerHTML?
      nodeName.appendChild(document.createTextNode(element.childNodes[i].getAttribute("text")));
      nodeName.onclick = TreeView.onNodeclick;

      title.appendChild(nodeName);
      container.appendChild(title);

      child.style.display = 'none';
      container.appendChild(child);

      // remove + sign of leaf node
      if (child.tagName.toLowerCase() == 'span' &&
          child.style.cursor == 'pointer') {
        // leaf node
        title.firstChild.nodeValue = '';
      }
    }

    return container;
  } else {
    // 3: TEXT_NODE
    if (element.nodeType == 3) return element;
    // 8: COMMENT_NODE
    if (element.nodeType == 8) return element;

    if (element.nodeType != 1)
      throw 'node has no child and node type != 1, 3, 8';

    if (element.getAttribute("src")) {
      // this is a 'load TOC' node
      var article = document.createElement('span');
      article.className = 'item';
      article.style.paddingLeft = '.5em';
      article.appendChild(document.createTextNode(i18n.gettext('Loading') + ' ...'));
      var filename = document.createElement('span');
      filename.style.display = 'none';
      // FIXME: use innerHTML?
      filename.appendChild(document.createTextNode(element.getAttribute("src")));
      article.appendChild(filename);
      return article;
    }

    if (element.getAttribute("action")) {
      // this is a 'load canon' node
      var article = document.createElement('span');
      article.style.cursor = 'pointer';
      // FIXME: use innerHTML?
      article.appendChild(document.createTextNode(
        element.getAttribute("action") + 
        '%%%' +
        element.getAttribute("text")));
      return article;
    }

    throw 'ELEMENT_NODE has no child and no property src and action';
  }
};

/**
 * @this {Dom element}
 */
TreeView.onNodeclick = function() {
  var pn = this.parentNode.nextSibling;
  if (pn.tagName.toLowerCase() == 'span') {
    if (pn.style.cursor == 'pointer') {
      // pn is a 'load canon' node
      var fileAndCanonName = pn.innerHTML.split('%%%');
      MainView.loadPaliXmlDoc(pali.basename(fileAndCanonName[0]),
                              fileAndCanonName[1]);
      return;
    } else {
      // pn is a 'load TOC' node
      var url = TreeView.getTocUrl(pali.basename(pn.lastChild.innerHTML));
      TreeView.appendTocXml(url, pn);
    }
  }
  if (pn.style.display == 'none') {
    this.previousSibling.nodeValue = '-';
    pn.style.display = 'block';
  }
  else {
    this.previousSibling.nodeValue = '+';
    pn.style.display = 'none';
  }
};

TreeView.appendTocXml = function(url, replacedNode) {
  var callback = function(xmlDoc, url) {
    var child = TreeView.traverseTree(xmlDoc.documentElement);
    replacedNode.parentNode.replaceChild(child, replacedNode);
    i18n.translateTreeView();
  };
  pali.httpGetXml(url, callback);
};
