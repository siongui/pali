var i18n = i18n || {};

// supported locale
i18n.localeSet = ['en_US', 'zh_TW', 'zh_CN'];

// current locale
i18n.locale = 'en_US';

i18n.getLocale = function() {
  if (!i18n.locale)
    throw 'In i18n.getLocale: fail to access i18n.locale';
  return i18n.locale;
};

i18n.setLocale = function(locale) {
  for(var i=0; i<i18n.localeSet.length; i++) {
    if (locale == i18n.localeSet[i]) {
      i18n.locale = locale;
      return true;
    }
  }

  return false;
};


i18n.translateDocTitle = function() {
  // FIXME
  return;
  // translate document title
  if (i18n.getLocale() == 'en_US')
    document.title = 'Pāḷi Tipiṭaka';
  else
    document.title = i18n.gettext(document.title);
};

i18n.optCache = {};

i18n.processElement = function(element) {
  // If this is an 'option' element
  if (element.tagName.toLowerCase() == 'option') {
    if (!i18n.optCache.hasOwnProperty(element.value))
      i18n.optCache[element.value] = element.innerHTML;

    if (element.value.indexOf('2') != -1) {
      var tmp = i18n.optCache[element.value];
      tmp = tmp.replace('English', i18n.gettext('English'));
      tmp = tmp.replace('Japanese', i18n.gettext('Japanese'));
      tmp = tmp.replace('Chinese', i18n.gettext('Chinese'));
      element.innerHTML = tmp;
    } else
      element.innerHTML = i18n.gettext(i18n.optCache[element.value]);

    return;
  }

  if (element.lastChild.tagName) {
    if (element.lastChild.className != 'hiddenOriginalText')
      throw 'In i18n.processElement: something strange happen';
    var oriText = element.lastChild.innerHTML;
    element.replaceChild(document.createTextNode(i18n.gettext(oriText)),
                   element.firstChild);
  } else {
    // first time process this element, no hidden b element
    // only one text node child in the element
    var oriText = element.innerHTML;
    pali.removeAllChildren(element);
    element.appendChild(document.createTextNode(i18n.gettext(oriText)));
    // store original text in hidden b element
    var b = document.createElement('b');
    b.className = 'hiddenOriginalText';
    b.appendChild(document.createTextNode(oriText));
    element.appendChild(b);
  }
};

i18n.translateMainBar = function() {
  // translate main bar
  var aElems = document.getElementById('mainbar').getElementsByTagName('a');
  for (var i=0; i<aElems.length; i++)
    i18n.processElement(aElems[i]);
};

i18n.translateSettingMenu = function() {
  // translate setting menu
  var spanElems = document.getElementById('settingmenu').getElementsByTagName('span');
  for (var i=0; i<spanElems.length; i++)
    i18n.processElement(spanElems[i]);

  var optElems = document.getElementById('settingmenu').getElementsByTagName('option');
  for (var i=0; i<optElems.length; i++)
    i18n.processElement(optElems[i]);
};


i18n.processTreeViewElement = function(element) {
  if (element.tagName.toLowerCase() != 'span') return;

  if (element.className == 'treeNode') {
    if (element.lastChild.tagName) {
      if (element.lastChild.className != 'hiddenOriginalText')
        throw 'In i18n.processTreeViewElement: something strange happen';
      var oriText = element.lastChild.innerHTML;
      element.replaceChild(document.createTextNode(i18n.translateCanonText(oriText)),
                     element.firstChild);
    } else {
      // first time process this element, no hidden b element
      // only one text node child in the element
      var oriText = element.innerHTML;
      pali.removeAllChildren(element);
      element.appendChild(document.createTextNode(i18n.translateCanonText(oriText)));
      // store original text in hidden b element
      var b = document.createElement('b');
      b.className = 'hiddenOriginalText';
      b.appendChild(document.createTextNode(oriText));
      element.appendChild(b);
    }
  }

  if (element.className == 'item') {
    // this is a 'load TOC' node
    element.firstChild.nodeValue = i18n.gettext('Loading') + ' ...';
  }
};

i18n.translateTreeView = function() {
  if (!document.getElementById('translateTreeview').checked) return;

  var spanElems = document.getElementById('treeview').getElementsByTagName('span');
  for (var i=0; i<spanElems.length; i++)
    i18n.processTreeViewElement(spanElems[i]);
};

i18n.unprocessTreeViewElement = function(element) {
  if (element.tagName.toLowerCase() != 'span') return;

  if (element.className == 'treeNode') {
    if (element.lastChild.tagName) {
      if (element.lastChild.className != 'hiddenOriginalText')
        throw 'In i18n.processTreeViewElement: something strange happen';
      var oriText = element.lastChild.innerHTML;
      element.replaceChild(document.createTextNode(oriText),
                     element.firstChild);
    }
  }
};

i18n.untranslateTreeView = function() {
  var spanElems = document.getElementById('treeview').getElementsByTagName('span');
  for (var i=0; i<spanElems.length; i++)
    i18n.unprocessTreeViewElement(spanElems[i]);
};

i18n.translateMainView = function() {
  var st = document.getElementById('showTranslation');
  if (st) i18n.processElement(st.lastChild);

  var op = document.getElementById('oriPali');
  if (op) i18n.processElement(op);

  var ht = document.getElementById('htmlTranslation');
  if (ht) {
    var h3List = ht.getElementsByTagName('h3');
    if (h3List.length > 0)
      i18n.processElement(h3List[0]);

    var aElems = ht.getElementsByTagName('a');
    for (var i=0; i<aElems.length; i++)
      i18n.processElement(aElems[i]);
  }

  var ltd = document.getElementById('localeTranslationDiv');
  if (ltd) {
    var aElems = ltd.getElementsByTagName('a');
    for (var i=0; i<aElems.length; i++)
      i18n.processElement(aElems[i]);
  }
};


i18n.translateDocument = function() {
  i18n.translateDocTitle();
  i18n.translateMainBar();
  i18n.translateSettingMenu();
  i18n.translateTreeView();
  i18n.translateMainView();
};


i18n.xmlDoc2CN = function(xmlDoc) {
  if (xmlDoc.nodeType == 9) // document node
    i18n.xmlDoc2CN(xmlDoc.getElementsByTagName('body')[0]);

  if (xmlDoc.nodeType == 3) {
    // 3: text node => translate to zh_CN
    if (!TongWen)
      throw 'no TongWen JS library!';
    xmlDoc.nodeValue = TongWen.convert(xmlDoc.nodeValue, TongWen.flagSimp);
  }

  for (var i=0; i<xmlDoc.childNodes.length; i++)
    i18n.xmlDoc2CN(xmlDoc.childNodes[i]);
};


i18n.innerHTML  = function(element) {
  element.innerHTML = i18n.gettext(element.innerHTML);
};

i18n.gettext = function(text) {
  if (!i18n.db.hasOwnProperty(i18n.locale))
    return text;
  if (!i18n.db[i18n.locale].hasOwnProperty(text))
    return text;
  return i18n.db[i18n.locale][text];
};

i18n.db = {};
i18n.db['en_US'] = {
'en_US': 'English',
'zh_TW': 'Chinese (Traditional)',
'zh_CN': 'Chinese (Simplified)',
' ': ' '
};
i18n.db['zh_TW'] = {
'Pāḷi Tipiṭaka': 'Pāḷi Tipiṭaka (巴利三藏)',
'No Such Word': '無此字',
'Looking up ': '正在查詢 ',
'Home': '首頁',
'Dictionary': '字典',
'Setting': '設定',
'About': '關於',
'Contrast Reading': '比照對讀',
'Translation': '翻譯',
'Link': '連結',
'Tweet': '推文',
'Pāḷi-English': '巴利語-英文',
'Pāḷi-Japanese': '巴利語-日文',
'Pāḷi-Chinese': '巴利語-中文',
'English': '英文',
'Japanese': '日文',
'Chinese': '中文',
'en_US': '英文',
'zh_TW': '中文 (繁體)',
'zh_CN': '中文 (簡體)',
'Original Pāḷi Text': '原本巴利文字',
'See All Translation': '看所有翻譯',
'All Translations': '所有翻譯',
'See Translation': '看翻譯',
'See Translation of this Pāḷi Text': '看此巴利文件的翻譯',
'What languages of dictionaries to show?': '顯示哪種語言的字典?',
'The order of languages of dictionaries to show?': '顯示語言順序?',
'According to Language Settings in Browser': '根據瀏覽器語言設定',
'Show Tooltip When Hovering over Canon Texts': '當游標移到單字上時顯示翻譯提示',
'Translate Pāḷi-Chinese Dictionaries to Traditional Chinese': '將巴利語-中文字典轉換成傳統中文',
'double click on the word to see details': '滑鼠雙擊單字可以看詳細資料',
'Translate Pāḷi Texts on Left-side Treeview': '翻譯左側樹狀顯示裡的巴利文字',
'Loading': '載入中',
' ': ' '
};
i18n.db['zh_CN'] = (function() {
  if (typeof TongWen == 'undefined')
    throw 'no TongWen JS library!';
  var pairs = {};
  for (var key in i18n.db['zh_TW'])
    pairs[key] = TongWen.convert(i18n.db['zh_TW'][key], TongWen.flagSimp);
  return pairs;
})();

i18n.translateCanonText = function(canonText) {
  var tmp = canonText.replace(/\./g, '');
  tmp = tmp.replace(/\d/g, '');
  tmp = tmp.replace(/-/g, '');
  tmp = tmp.replace(/\s/g, '');
  tmp = tmp.replace(/\(/g, '');
  tmp = tmp.replace(/\)/g, '');
  var text = i18n.gettextCanon(tmp);

  if (canonText.indexOf(text) == -1) {
    if (i18n.getLocale() == 'en_US')
      text = '"' + text + '"';
    return canonText.replace(tmp, tmp + ' ' + text);
  }
  return canonText;
};

i18n.gettextCanon = function(text) {
  if (!i18n.tipitaka.hasOwnProperty(i18n.locale))
    return text;
  if (!i18n.tipitaka[i18n.locale].hasOwnProperty(text))
    return text;
  return i18n.tipitaka[i18n.locale][text];
};

i18n.tipitaka = {};
// http://www.accesstoinsight.org/tipitaka/index.html
// http://www.xin-yuan.com/cityzen/jiangtan/AHAN/ahan.htm
i18n.tipitaka['en_US'] = {
//'Vinayapiṭaka': 'The Book of the Discipline',
  'Dīghanikāya': 'Long Discourses',
    'Sīlakkhandhavaggapāḷi':'The Division Concerning Morality',
      'Brahmajālasuttaṃ': 'The All-embracing Net of Views',
      'Sāmaññaphalasuttaṃ': 'The Fruits of the Contemplative Life',
    'Mahāvaggapāḷi':'The Large Division',
//      'Mahāpadānasuttaṃ': '',
      'Mahānidānasuttaṃ': 'The Great Causes Discourse',
//      'Mahāparinibbānasuttaṃ': '',
//      'Mahāsudassanasuttaṃ': '',
//      'Janavasabhasuttaṃ': '',
//      'Mahāgovindasuttaṃ': '',
      'Mahāsamayasuttaṃ': 'The Great Assembly/The Great Meeting',
      'Sakkapañhasuttaṃ': "Sakka's Questions",
      'Mahāsatipaṭṭhānasuttaṃ': 'The Great Frames of Reference',
//      'Pāyāsisuttaṃ': '',
    'Pāthikavaggapāḷi':'The Pāthika Division',
//      'Pāthikasuttaṃ': '',
//      'Udumbarikasuttaṃ': '',
      'Cakkavattisuttaṃ': 'The Wheel-turning Emperor',
//      'Aggaññasuttaṃ': '',
//      'Sampasādanīyasuttaṃ': '',
//      'Pāsādikasuttaṃ': '',
//      'Lakkhaṇasuttaṃ': '',
      'Siṅgālasuttaṃ': "The Buddha's Advice to Sigalaka/The Discourse to Sigala",
      'Āṭānāṭiyasuttaṃ': 'Discourse on Āṭānāṭiya',
//      'Saṅgītisuttaṃ': '',
//      'Dasuttarasuttaṃ': '',
  'Majjhimanikāya': 'Middle-length Discourses',
  'Saṃyuttanikāya': 'Grouped" Discourses',
  'Aṅguttaranikāya': 'Further-factored Discourses',
  'Khuddakanikāya': 'Division of Short Books',
//'Abhidhammapiṭaka': '',
  'Dhammasaṅgaṇīpāḷi': 'Enumeration of Phenomena',
  'Vibhaṅgapāḷi': 'The Book of Analysis',
  'Dhātukathāpāḷi': 'Discourse on Elements',
  'Puggalapaññattipāḷi': 'A Designation of Human Types',
  'Kathāvatthupāḷi': 'Points of Controversy',
//  'Yamakapāḷi': '',
//  'Paṭṭhānapāḷi': '',
' ': ' '
};
// http://www.therawikipedia.org/wiki/%E5%A2%9E%E6%94%AF%E9%83%A8
// http://yifertw.blogspot.tw/2008/04/9-2008421.html
i18n.tipitaka['zh_TW'] = {
'Vinayapiṭaka': '律藏',
  'Pārājikapāḷi': '波羅夷品',
//    'Verañjakaṇḍaṃ': '',
    'Pārājikakaṇḍaṃ': '波羅夷 (他勝,斷頭)章',
    'Saṅghādisesakaṇḍaṃ': '僧殘 (僧伽胝施沙)章',
    'Aniyatakaṇḍaṃ': '不定章',
    'Nissaggiyakaṇḍaṃ': '捨墮 (尼薩耆波逸提)章',
  'Pācittiyapāḷi': '波逸提品',
    'Pācittiyakaṇḍaṃ': '波逸提 (單墮)章',
    'Pāṭidesanīyakaṇḍaṃ': '悔過 (波胝提舍尼)章',
    'Sekhiyakaṇḍaṃ': '眾學章',
    'Adhikaraṇasamathā': '滅諍',
    'bhikkhunīvibhaṅgo': '比丘尼分別',
  'Mahāvaggapāḷi': '大品',
    'Mahākhandhako': '大篇 (大犍度)',
    'Uposathakkhandhako': '伍波薩他篇 (布薩犍度)',
    'Vassūpanāyikakkhandhako': '入雨安居篇 (入雨安居犍度)',
    'Pavāraṇākkhandhako': '自恣篇 (自恣犍度)',
    'Cammakkhandhako': '皮革篇 (皮革犍度)',
    'Bhesajjakkhandhako': '藥篇 (藥犍度)',
    'Kathinakkhandhako': '咖提那篇 (迦絺那衣犍度)',
    'Cīvarakkhandhako': '衣篇 (衣犍度)',
    'Campeyyakkhandhako': '瞻巴篇 (瞻波犍度)',
    'Kosambakakkhandhako': '高賞比篇 (拘晱彌犍度)',
  'Cūḷavaggapāḷi': '小品',
    'Kammakkhandhakaṃ': '甘馬篇 (羯摩犍度)',
    'Pārivāsikakkhandhakaṃ': '別住篇 (別住犍度)',
    'Samuccayakkhandhakaṃ': '集篇 (集犍度)',
    'Samathakkhandhakaṃ': '止篇 (滅諍犍度)',
    'Khuddakavatthukkhandhakaṃ': '小事篇 (小犍度)',
    'Senāsanakkhandhakaṃ': '坐卧處篇 (臥坐具犍度)',
    'Saṅghabhedakakkhandhakaṃ': '破僧篇 (破僧犍度)',
    'Vattakkhandhakaṃ': '行儀篇 (儀法犍度)',
    'Pātimokkhaṭṭhapanakkhandhakaṃ': '遮誦戒篇 (遮說戒犍度)',
    'Bhikkhunikkhandhakaṃ': '比庫尼篇 (比丘尼犍度)',
    'Pañcasatikakkhandhakaṃ': '五百篇 (五百結集犍度)',
    'Sattasatikakkhandhakaṃ': '七百篇 (七百結集犍度)',
  'Parivārapāḷi': '附隨',
//    'Soḷasamahāvāro': '',
    'Samuṭṭhānasīsasaṅkhepo': '等起攝頌 (等起)',
    'Antarapeyyālaṃ': '無間省略',
    'Khandhakapucchāvāro': '問犍度章',
    'Ekuttarikanayo': '增一法',
    'Uposathādipucchāvissajjanā': '伍波薩他初解答章 (布薩初解答以及制戒義利論)',
    'Gāthāsaṅgaṇikaṃ': '伽陀集',
    'Adhikaraṇabhedo': '諍事分解',
    'Aparagāthāsaṅgaṇikaṃ': '別伽陀集',
    'Codanākaṇḍaṃ': '呵責品',
    'Cūḷasaṅgāmo': '小諍',
    'Mahāsaṅgāmo': '大諍',
    'Kathinabhedo': '咖提那衣分解 (迦絺那衣分解)',
    'Upālipañcakaṃ': '伍巴離五法 (優婆離五法)',
    'Atthāpattisamuṭṭhānaṃ': '等起',
    'Dutiyagāthāsaṅgaṇikaṃ': '第二伽陀集',
    'Sedamocanagāthā': '發汗偈',
    'Pañcavaggo': '五品',
'Suttapiṭaka': '經藏',
  'Dīghanikāya': '長部',
    'Sīlakkhandhavaggapāḷi':'戒蘊品',
      'Brahmajālasuttaṃ': '梵網經',
      'Sāmaññaphalasuttaṃ': '沙門果經',
      'Ambaṭṭhasuttaṃ': '阿摩晝經',
      'Soṇadaṇḍasuttaṃ': '種德經',
      'Kūṭadantasuttaṃ': '究羅檀頭經',
      'Mahālisuttaṃ': '摩訶梨經',
      'Jāliyasuttaṃ': '闍利經',
      'Mahāsīhanādasuttaṃ': '迦葉獅子吼經',
      'Poṭṭhapādasuttaṃ': '布吒婆樓經',
      'Subhasuttaṃ': '須婆經',
      'Kevaṭṭasuttaṃ': '堅固經',
      'Lohiccasuttaṃ': '露遮經',
      'Tevijjasuttaṃ': '三明經',
    'Mahāvaggapāḷi':'大品',
      'Mahāpadānasuttaṃ': '大本經',
      'Mahānidānasuttaṃ': '大緣經',
      'Mahāparinibbānasuttaṃ': '大般涅槃經',
      'Mahāsudassanasuttaṃ': '大善見王經',
      'Janavasabhasuttaṃ': '闍尼沙經',
      'Mahāgovindasuttaṃ': '大典尊經',
      'Mahāsamayasuttaṃ': '大會經',
      'Sakkapañhasuttaṃ': '帝釋所問經',
      'Mahāsatipaṭṭhānasuttaṃ': '大念處經',
      'Pāyāsisuttaṃ': '弊宿經',
    'Pāthikavaggapāḷi':'波梨品',
      'Pāthikasuttaṃ': '波梨經',
      'Udumbarikasuttaṃ': '優曇婆邏獅子吼經',
      'Cakkavattisuttaṃ': '轉輪聖王獅子吼經',
      'Aggaññasuttaṃ': '起世因本經',
      'Sampasādanīyasuttaṃ': '自歡喜經',
      'Pāsādikasuttaṃ': '清淨經',
      'Lakkhaṇasuttaṃ': '三十二相經',
      'Siṅgālasuttaṃ': '教授屍迦羅越經',
      'Āṭānāṭiyasuttaṃ': '阿吒曩胝經',
      'Saṅgītisuttaṃ': '等誦經',
      'Dasuttarasuttaṃ': '十上經',
  'Majjhimanikāya': '中部',
    'Mūlapaṇṇāsapāḷi': '根本五十經編',
      'Mūlapariyāyavaggo': '根本法門品',
      'Sīhanādavaggo': '師子吼品',
      'Opammavaggo': '譬喻品',
      'Mahāyamakavaggo': '大雙品',
      'Cūḷayamakavaggo': '小雙品',
    'Majjhimapaṇṇāsapāḷi': '中分五十經編',
      'Gahapativaggo': '居士品',
      'Bhikkhuvaggo': '比丘品',
      'Paribbājakavaggo': '遊行者品',
      'Rājavaggo': '王品',
      'Brāhmaṇavaggo': '婆羅門品',
    'Uparipaṇṇāsapāḷi': '後分五十經編',
      'Devadahavaggo': '天臂品',
      'Anupadavaggo': '緊隨品',
      'Suññatavaggo': '空品',
      'Vibhaṅgavaggo': '分別品',
      'Saḷāyatanavaggo': '六處品',
  'Saṃyuttanikāya': '相應部',
    'Sagāthāvaggapāḷi': '有偈篇',
      'Devatāsaṃyuttaṃ': '諸天相應',
      'Devaputtasaṃyuttaṃ': '天子相應',
      'Kosalasaṃyuttaṃ': '憍薩羅相應',
      'Mārasaṃyuttaṃ': '魔羅相應',
      'Bhikkhunīsaṃyuttaṃ': '比丘尼相應',
      'Brahmasaṃyuttaṃ': '梵天相應',
      'Brāhmaṇasaṃyuttaṃ': '婆羅門相應',
      'Vaṅgīsasaṃyuttaṃ': '婆耆沙長老相應',
      'Vanasaṃyuttaṃ': '森林相應',
      'Yakkhasaṃyuttaṃ': '夜叉相應',
      'Sakkasaṃyuttaṃ': '帝釋天帝相應',
    'Nidānavaggapāḷi': '因緣篇',
      'Nidānasaṃyuttaṃ': '因緣相應',
      'Abhisamayasaṃyuttaṃ': '現觀相應',
      'Dhātusaṃyuttaṃ': '界相應',
      'Anamataggasaṃyuttaṃ': '無始相應',
      'Kassapasaṃyuttaṃ': '迦葉相應',
      'Lābhasakkārasaṃyuttaṃ': '利得與供養相應',
      'Rāhulasaṃyuttaṃ': '羅睺羅相應',
      'Lakkhaṇasaṃyuttaṃ': '勒叉那相應',
      'Opammasaṃyuttaṃ': '譬喻相應',
      'Bhikkhusaṃyuttaṃ': '比丘相應',
    'Khandhavaggapāḷi': '蘊篇',
      'Khandhasaṃyuttaṃ': '蘊相應',
      'Rādhasaṃyuttaṃ': '羅陀相應',
      'Diṭṭhisaṃyuttaṃ': '見相應',
      'Okkantasaṃyuttaṃ': '入相應',
      'Uppādasaṃyuttaṃ': '生相應',
      'Kilesasaṃyuttaṃ': '煩惱相應',
      'Sāriputtasaṃyuttaṃ': '舍利弗相應',
      'Nāgasaṃyuttaṃ': '龍相應',
      'Supaṇṇasaṃyuttaṃ': '金翅鳥相應',
      'Gandhabbakāyasaṃyuttaṃ': '乾闥婆相應',
      'Valāhakasaṃyuttaṃ': '雲相應',
      'Vacchagottasaṃyuttaṃ': '婆磋種相應',
      'Jhānasaṃyuttaṃ': '禪定相應',
    'Saḷāyatanavaggapāḷi': '六處篇',
      'Saḷāyatanasaṃyuttaṃ': '六處相應',
      'Vedanāsaṃyuttaṃ': '受相應',
      'Mātugāmasaṃyuttaṃ': '女人相應',
      'Jambukhādakasaṃyuttaṃ': '閻浮車相應',
      'Sāmaṇḍakasaṃyuttaṃ': '沙門出家相應',
      'Moggallānasaṃyuttaṃ': '目犍連相應',
      'Cittasaṃyuttaṃ': '質多相應',
      'Gāmaṇisaṃyuttaṃ': '聚落主相應',
      'Asaṅkhatasaṃyuttaṃ': '無為相應',
      'Abyākatasaṃyuttaṃ': '無記相應',
//    'Mahāvaggapāḷi': '大篇',
      'Maggasaṃyuttaṃ': '道相應',
      'Bojjhaṅgasaṃyuttaṃ': '覺支相應',
      'Satipaṭṭhānasaṃyuttaṃ': '念處相應',
      'Indriyasaṃyuttaṃ': '根相應',
      'Sammappadhānasaṃyuttaṃ': '正勤相應',
      'Balasaṃyuttaṃ': '力相應',
      'Iddhipādasaṃyuttaṃ': '神足相應',
      'Anuruddhasaṃyuttaṃ': '阿那律相應',
//      'Jhānasaṃyuttaṃ': '靜慮相應',
      'Ānāpānasaṃyuttaṃ': '入出息相應',
      'Sotāpattisaṃyuttaṃ': '入流 (須陀洹)相應',
      'Saccasaṃyuttaṃ': '諦相應',
  'Aṅguttaranikāya': '增支部',
    'Ekakanipātapāḷi': '一集',
      'Rūpādivaggo': '色等品',
      'Nīvaraṇappahānavaggo': '斷蓋品',
      'Akammaniyavaggo': '無堪忍品',
      'Adantavaggo': '無調品',
      'Paṇihitaacchavaggo': '向與隱覆品',
      'Accharāsaṅghātavaggo': '彈指品',
      'Vīriyārambhādivaggo': '發精進等品',
      'Kalyāṇamittādivaggo': '善友等品',
      'Pamādādivaggo': '放逸等品',
//      'Dutiyapamādādivaggo': '',
      'Adhammavaggo': '非法等品',
      'Anāpattivaggo': '無范等品',
      'Ekapuggalavaggo': '一人品',
      'Etadaggavaggo': '是第一品',
      'Aṭṭhānapāḷi': '無有是處品',
      'Ekadhammapāḷi': '一法品',
      'Pasādakaradhammavaggo': '種子品',
      'Aparaaccharāsaṅghātavaggo': '末伽梨品',
      'Kāyagatāsativaggo': '不放逸品',
      'Amatavaggo': '靜慮品',
    'Dukanipātapāḷi': '二集',
      'Kammakaraṇavaggo': '科刑罰品',
      'Adhikaraṇavaggo': '靜論品',
      'Bālavaggo': '愚人品',
      'Samacittavaggo': '等心品',
      'Parisavaggo': '會眾品',
      'Puggalavaggo': '人品',
      'Sukhavaggo': '樂品',
      'Sanimittavaggo': '有品',
      'Dhammavaggo': '法品',
//      'Bālavaggo': '愚者品',
      'Āsāduppajahavaggo': '希望品',
      'Āyācanavaggo': '希求品',
      'Dānavaggo': '施品',
      'Santhāravaggo': '覆護品',
      'Samāpattivaggo': '入定品',
      'Kodhapeyyālaṃ': '忿品',
      'Akusalapeyyālaṃ': '(律廣說)品',
//      'Vinayapeyyālaṃ': '',
//      'Rāgapeyyālaṃ': '',
    'Tikanipātapāḷi': '三集',
//      'Bālavaggo': '愚人品',
      'Rathakāravaggo': '車匠品',
//      'Puggalavaggo': '補特羅品',
      'Devadūtavaggo': '天使品',
//      'Cūḷavaggo': '小品',
//      'Brāhmaṇavaggo': '婆羅門品',
//      'Mahāvaggo': '大品',
      'Ānandavaggo': '阿難品',
      'Samaṇavaggo': '沙門品',
      'Loṇakapallavaggo': '掬鹽品',
      'Sambodhavaggo': '等覺品',
      'Āpāyikavaggo': '惡趣品',
      'Kusināravaggo': '古西那拉品',
      'Yodhājīvavaggo': '戰士品',
      'Maṅgalavaggo': '吉祥品',
      'Acelakavaggo': '裸形品',
//      'Kammapathapeyyālaṃ': '',
//      'Rāgapeyyālaṃ': '',
    'Catukkanipātapāḷi': '四集',
    'Pañcakanipātapāḷi': '五集',
    'Chakkanipātapāḷi': '六集',
    'Sattakanipātapāḷi': '七集',
    'Aṭṭhakādinipātapāḷi': '八集',
    'Navakanipātapāḷi': '九集',
    'Dasakanipātapāḷi': '十集',
    'Ekādasakanipātapāḷi': '十一集',
      'Nissayavaggo': '依止品',
      'Anussativaggo': '憶念品',
      'Sāmaññavaggo': '沙門品',
      'Rāgapeyyālaṃ': '貪品',
  'Khuddakanikāya': '小部',
    'Khuddakapāṭhapāḷi': '小誦',
    'Dhammapadapāḷi': '法句',
    'Udānapāḷi': '自說',
    'Itivuttakapāḷi': '如是語',
    'Suttanipātapāḷi': '經集',
      'Uragavaggo': '蛇品',
      'Cūḷavaggo': '小品',
      'Mahāvaggo': '大品',
      'Aṭṭhakavaggo': '八頌經品',
      'Pārāyanavaggo': '彼岸道品',
    'Vimānavatthupāḷi': '天宮事',
    'Petavatthupāḷi': '餓鬼事',
    'Theragāthāpāḷi': '長老偈',
    'Therīgāthāpāḷi': '長老尼偈',
    'Apadānapāḷi': '譬喻',
    'Buddhavaṃsapāḷi': '佛種姓 (諸佛史)',
    'Cariyāpiṭakapāḷi': '所行藏',
    'Jātakapāḷi': '本生',
    'Mahāniddesapāḷi': '大義釋',
    'Cūḷaniddesapāḷi': '小義釋',
    'Paṭisambhidāmaggapāḷi': '無礙解道',
    'Nettippakaraṇapāḷi': '導論',
    'Milindapañhapāḷi': '彌林達問經 (彌林達王問經,那先比丘經)',
    'Peṭakopadesapāḷi': '藏釋 (三藏知津)',
'Abhidhammapiṭaka': '論藏 (阿毘達摩)',
  'Dhammasaṅgaṇīpāḷi': '法集論',
  'Vibhaṅgapāḷi': '分別論',
  'Dhātukathāpāḷi': '界說論',
  'Puggalapaññattipāḷi': '人施設論',
  'Kathāvatthupāḷi': '論事',
  'Yamakapāḷi': '雙對論',
  'Paṭṭhānapāḷi': '發趣論',
' ': ' '
};
i18n.tipitaka['zh_CN'] = (function() {
  if (typeof TongWen == 'undefined')
    throw 'no TongWen JS library!';
  var pairs = {};
  for (var key in i18n.tipitaka['zh_TW'])
    pairs[key] = TongWen.convert(i18n.tipitaka['zh_TW'][key], TongWen.flagSimp);
  return pairs;
})();
