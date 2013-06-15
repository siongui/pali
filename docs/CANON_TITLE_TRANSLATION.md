### How to translate the pali text title (canon title) to my language on tipitaka website?

Answer: We will show how to do this by example. Say, we want to translate pali text title into French.

1. Pick your [language locale](http://www.roseindia.net/tutorials/I18N/locales-list.shtml). In our example, it is <em>fr_FR</em>.

2. Copy template from translation of other languages: [English template](https://github.com/siongui/pali/blob/master/common/locale/en_US/LC_MESSAGES/PaliTextTitle.py) and [Traditional Chinese template](https://github.com/siongui/pali/blob/master/common/locale/zh_TW/LC_MESSAGES/PaliTextTitle.py). Put the template at <strong>{{ PALI_REPOSITORY }}/common/locale/{{ your_language_locale }}/LC_MESSAGES/PaliTextTitle.py</strong>. In our example, put template at <strong>{{ PALI_REPOSITORY }}/common/locale/fr_FR/LC_MESSAGES/PaliTextTitle.py</strong>.

3. Start to translate: Follow the same format to translate pali texts to your language. If you do not know how to translate some pali text title, comment out the line (add a leading # in the line).

4. You do not have to translate all titles before you make the pull request at the [pali](https://github.com/siongui/pali) repository on the github. Actually it is recommended that you make pull request every time you finish part of the translation. If you are not familiar with pull request, you can also mail the translation to me (siongui@gmail.com). However, it is always recommended to use pull request.

5. It is recommended to release your translation in public domain.

