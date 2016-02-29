package lib

import "strings"

type IdExp struct {
	Id  string
	Exp string
}

func BookIdWordExps2IdExpsAccordingToSetting(
	wi BookIdWordExps,
	di BookIdAndInfos,
	setting PaliDictionarySetting,
	navigatorLanguages string) []IdExp {
	var result []IdExp

	var enIdExps []IdExp
	var jaIdExps []IdExp
	var zhIdExps []IdExp
	var viIdExps []IdExp
	var myIdExps []IdExp

	for bookId, explanation := range wi {
		if di[bookId].Lang == "en" && setting.P2en {
			enIdExps = append(enIdExps, IdExp{bookId, explanation})
			continue
		}
		if di[bookId].Lang == "ja" && setting.P2ja {
			jaIdExps = append(jaIdExps, IdExp{bookId, explanation})
			continue
		}
		if di[bookId].Lang == "zh" && setting.P2zh {
			zhIdExps = append(zhIdExps, IdExp{bookId, explanation})
			continue
		}
		if di[bookId].Lang == "vi" && setting.P2vi {
			viIdExps = append(viIdExps, IdExp{bookId, explanation})
			continue
		}
		if di[bookId].Lang == "my" && setting.P2my {
			myIdExps = append(myIdExps, IdExp{bookId, explanation})
			continue
		}
	}

	// show en first
	if setting.DicLangOrder == "en" {
		result = append(result, enIdExps...)
		enIdExps = nil
	}
	// show ja first
	if setting.DicLangOrder == "ja" {
		result = append(result, jaIdExps...)
		jaIdExps = nil
	}
	// show zh first
	if setting.DicLangOrder == "zh" {
		result = append(result, zhIdExps...)
		zhIdExps = nil
	}
	// show vi first
	if setting.DicLangOrder == "vi" {
		result = append(result, viIdExps...)
		viIdExps = nil
	}
	// show my first
	if setting.DicLangOrder == "my" {
		result = append(result, myIdExps...)
		myIdExps = nil
	}

	// re-order according to browser NavigatorLanguages API
	for _, navigatorLanguage := range strings.Split(navigatorLanguages, ",") {
		lang := strings.TrimSpace(navigatorLanguage)[:2]
		if lang == "en" {
			result = append(result, enIdExps...)
			enIdExps = nil
			continue
		}
		if lang == "ja" {
			result = append(result, jaIdExps...)
			jaIdExps = nil
			continue
		}
		if lang == "zh" {
			result = append(result, zhIdExps...)
			zhIdExps = nil
			continue
		}
		if lang == "vi" {
			result = append(result, viIdExps...)
			viIdExps = nil
			continue
		}
		if lang == "my" {
			result = append(result, myIdExps...)
			myIdExps = nil
			continue
		}
	}

	result = append(result, myIdExps...)
	result = append(result, viIdExps...)
	result = append(result, zhIdExps...)
	result = append(result, jaIdExps...)
	result = append(result, enIdExps...)

	return result
}
