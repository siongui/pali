### How to add more contrast (parallel) readings for tipitaka website?

Answer: It is actually very easy to add more contrast readings of some specific language because this feature has been put in first priority in the beginning. First take a look at [CSCD directory](https://github.com/siongui/data/tree/master/pali/common/romn/cscd) at [data](https://github.com/siongui/data) repository. This directory contains all the Roman pali texts released by [The Pali Tipitaka](http://www.tipitaka.org/). The xml files in this directory are the <em>base</em> format of the translation. Then take a look at [translation directory](https://github.com/siongui/data/tree/master/pali/common/translation) at [data](https://github.com/siongui/data) repository. All available translations are sorted according to lagnauges, then sorted by translators in sub-directories.

I will use the first chapter [Yamakavaggo](https://github.com/siongui/data/blob/master/pali/common/romn/cscd/s0502m.mul0.xml) of Dhammapada as example. One of the traditional chinese translation is available [here](https://github.com/siongui/data/blob/master/pali/common/translation/zh_TW/2/s0502m.mul0.xml). Take a look at the original pali texts and translated texts. You will find the texts inside the <em>p</em> tag are 1-to-1 mapping. So if you want to add contrast reading of Yamakavaggo of some specifice language, you can replace the texts inside the <em>p</em> tag with corresponding translated texts of the language. If translation of some lines are not available. Just leave the origianl pali texts unchanged. After finished, make a pull requests on [data](https://github.com/siongui/data) repository, or mail the translated xml file to me (siongui@gmail.com). It is recommended to release your work in public domain.

Here another example is given. To translate the Akammaniyavaggo, the third vagga of AN 1. First take a look at [cscd dir](https://github.com/siongui/data/tree/master/pali/common/romn/cscd) on [data](https://github.com/siongui/data) repo. All templates to be translated are here, actually the xml files in this dir are orginal pali texts. The xml which contains Akammaniyavaggo is [s0401m.mul2.xml](https://github.com/siongui/data/blob/master/pali/common/romn/cscd/s0401m.mul2.xml) in this dir. Please copy this xml file to another directory and translate this file directly.

The following is something you should know when translating:

1. <em>hi</em> tag: We suggest to respect this tag and the content inside, this marks the number of gatha or paragraph so the better choice is to respect it and do not modify it and the content inside.

2. <em>pb</em> tag: Not sure what this tag is for, usually this is removed in the translation.

3. use <em>note</em> tag to mark footnote: for example,
```xml
<p><hi>...</hi> I am example <note>I am footnote of example</note> ...some other content here.... </p>
```
   In original xml files of pali texts, VRI use <em>note</em> tag to mark different version of the canon. We can remove their note tag and use this note tag to mark the notes in translation.

4. It is often the case that translators do not translate all of the pali texts in the xml file. Please leave the un-translated part <em>UNCHANGED</em>.

5. If & is used by translators in their translations, please escape it with <strong><em>\&amp;</em></strong>

6. After you finish edit the xml file, please check the char encoding of your translated file by the following command in Ubuntu Linux:
```bash
$ cd dir_of_your_translated_xml_file
$ chardet xml_file_name
```
   If you see from the output that the encoding of the xml file is UTF-8, please the first line in xml file. Change UTF-16 to UTF-8 in the first line.

7. <em>br</em> tag is allowed in the xml.

