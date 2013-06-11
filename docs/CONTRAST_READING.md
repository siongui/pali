### How to add more contrast (parallel) readings for tipitaka website?

Answer: First take a look at [CSCD directory](https://github.com/siongui/data/tree/master/pali/common/romn/cscd) at [data](https://github.com/siongui/data) repository. This directory contains all the Roman pali texts released by [The Pali Tipitaka](http://www.tipitaka.org/). The xml files in this directory are the <strong><em>base</em></strong> format (i.e., template) of the translation. Then take a look at [translation directory](https://github.com/siongui/data/tree/master/pali/common/translation) at [data](https://github.com/siongui/data) repository. All available translations are sorted according to lagnauges, then sorted by translators in sub-directories.

I will use the first chapter [Yamakavaggo](https://github.com/siongui/data/blob/master/pali/common/romn/cscd/s0502m.mul0.xml) of Dhammapada as example. One of the Traditional Chinese translation is available [here](https://github.com/siongui/data/blob/master/pali/common/translation/zh_TW/2/s0502m.mul0.xml). Take a look at the original pali texts and translated texts. You will find the texts inside the <strong><em>p</em></strong> tag are 1-to-1 mapping. So if you want to add contrast reading of Yamakavaggo of some specifice language, first you copy [Yamakavaggo xml file](https://github.com/siongui/data/blob/master/pali/common/romn/cscd/s0502m.mul0.xml) to your working directory, then edit the xml file and replace the pali texts inside the <em>p</em> tag with corresponding translated texts of the language. If translation of some lines are not available, please leave the origianl pali texts unchanged. After finished, make a pull requests on [data](https://github.com/siongui/data) repository, or mail the translated xml file to me (siongui@gmail.com). It is recommended to release your work in public domain.

Here another example is given. To translate the Akammaniyavaggo, the third vagga of AN 1. First take a look at [cscd directory](https://github.com/siongui/data/tree/master/pali/common/romn/cscd) on [data](https://github.com/siongui/data) repository. All templates to be translated are put here, actually the xml files in this directory are orginal pali texts. The xml file which contains Akammaniyavaggo is [s0401m.mul2.xml](https://github.com/siongui/data/blob/master/pali/common/romn/cscd/s0401m.mul2.xml) in this directory. Please copy this xml file to another directory and translate this file directly.

The following is what you may need to know when translating:

1. <strong><em>hi</em></strong> tag: We suggest to respect this tag and the content inside, this marks the number of gatha or paragraph so the better choice is to respect it and do not modify it and the content inside.

2. <strong><em>pb</em></strong> tag: Not sure what this tag is for, usually this is removed in the translation.

3. use <strong><em>note</em></strong> tag to mark footnote: for example,
```xml
<p><hi> ... </hi> I am example <note>I am footnote of example</note> </p>
```
   In original xml files of pali texts, VRI use <em>note</em> tag to mark different version of the canon. We can remove their note tag and use this note tag to mark the notes in translation.

4. It is often the case that translators do not translate all of the pali texts in the xml file. Please leave the un-translated part <strong><em>UNCHANGED</em></strong>.

5. If & is used by translators in their translations, please escape it with <strong><em>\&amp;</em></strong>

6. After you finish to edit the xml file, please check the char encoding of your translated file by the following command in Ubuntu Linux:
```bash
$ cd dir_of_your_translated_xml_file
$ chardet xml_file_name
```
   If you see from the output that the encoding of the xml file is UTF-8, please modify the first line in xml file. Change <strong>UTF-16</strong> to <strong>UTF-8</strong> in the first line.

7. <strong><em>br</em></strong> tag is allowed in the xml file of translations.

