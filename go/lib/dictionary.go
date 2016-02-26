/*
The format of BookIdAndInfos:
BookIdAndInfos = object of key-value pairs, where
  key = id of the dictionary
  value = [cell1, cell2, cell3, cell4], where
    cell1 = language of the dictionary.
            zh: Chinese
            ja: Japanese
            en: English
            vi: Vietnamese
            my: Burmese(Myanmar)
    cell2 = separator, used to get short explanation of the word.
    cell3 = short name of the dictionary
    cell4 = name and author of the dictionary

References:
http://stackoverflow.com/questions/10858787/what-are-the-uses-for-tags-in-go
*/
package lib

import "html/template"

type BookInfo struct {
	Lang      string `json:"lang"`
	Separator string `json:"separator"`
	Name      string `json:"name"`
	Author    string `json:"author"`
}

// book id <-> book info
type BookIdAndInfos map[string]BookInfo

// book id <-> word explanation
type BookIdWordExps map[string]string

type BookNameWordExp struct {
	BookName    string
	Explanation template.HTML
}

const HtmlTemplateBookNameWordExps = `
{{range $bnwe := .}}
<article class="word-explanation">
  <header>{{$bnwe.BookName}}</header>
  <p>{{$bnwe.Explanation}}</p>
</article>
{{end}}`

func BookIdWordExps2BookNameWordExps(wi BookIdWordExps, di BookIdAndInfos) []BookNameWordExp {
	var bnwes []BookNameWordExp
	for bookId, explanation := range wi {
		bnwes = append(bnwes, BookNameWordExp{
			BookName:    di[bookId].Author,
			Explanation: template.HTML(explanation),
		})
	}
	return bnwes
}

type PaliDictionarySetting struct {
	IsShowWordPreview bool   `json:"isPreview"`
	P2en              bool   `json:"p2en"`
	P2ja              bool   `json:"p2ja"`
	P2zh              bool   `json:"p2zh"`
	P2vi              bool   `json:"p2vi"`
	P2my              bool   `json:"p2my"`
	DicLangOrder      string `json:"dicLangOrder"`
}

// book id <-> BookIdWordExps
type mapBookId2BookNameWordExp map[string]BookNameWordExp

func combineBookId2BookNameWordExp(langsbi2bnwe ...mapBookId2BookNameWordExp) []BookNameWordExp {
	var result []BookNameWordExp
	for _, bi2bnwe := range langsbi2bnwe {
		for _, bnwe := range bi2bnwe {
			result = append(result, bnwe)
		}
	}
	return result
}

func BookIdWordExps2BookNameWordExpsAccordingToSetting(wi BookIdWordExps, di BookIdAndInfos, setting PaliDictionarySetting) []BookNameWordExp {
	enBookId2BookNameWordExp := mapBookId2BookNameWordExp{}
	jaBookId2BookNameWordExp := mapBookId2BookNameWordExp{}
	zhBookId2BookNameWordExp := mapBookId2BookNameWordExp{}
	viBookId2BookNameWordExp := mapBookId2BookNameWordExp{}
	myBookId2BookNameWordExp := mapBookId2BookNameWordExp{}

	for bookId, explanation := range wi {
		if di[bookId].Lang == "en" && setting.P2en {
			enBookId2BookNameWordExp[bookId] = BookNameWordExp{
				BookName:    di[bookId].Author,
				Explanation: template.HTML(explanation),
			}
			continue
		}
		if di[bookId].Lang == "ja" && setting.P2ja {
			jaBookId2BookNameWordExp[bookId] = BookNameWordExp{
				BookName:    di[bookId].Author,
				Explanation: template.HTML(explanation),
			}
			continue
		}
		if di[bookId].Lang == "zh" && setting.P2zh {
			zhBookId2BookNameWordExp[bookId] = BookNameWordExp{
				BookName:    di[bookId].Author,
				Explanation: template.HTML(explanation),
			}
			continue
		}
		if di[bookId].Lang == "vi" && setting.P2vi {
			viBookId2BookNameWordExp[bookId] = BookNameWordExp{
				BookName:    di[bookId].Author,
				Explanation: template.HTML(explanation),
			}
			continue
		}
		if di[bookId].Lang == "my" && setting.P2my {
			myBookId2BookNameWordExp[bookId] = BookNameWordExp{
				BookName:    di[bookId].Author,
				Explanation: template.HTML(explanation),
			}
			continue
		}
	}

	if setting.DicLangOrder == "en" {
		return combineBookId2BookNameWordExp(
			enBookId2BookNameWordExp,
			zhBookId2BookNameWordExp,
			jaBookId2BookNameWordExp,
			viBookId2BookNameWordExp,
			myBookId2BookNameWordExp)
	}
	if setting.DicLangOrder == "ja" {
		return combineBookId2BookNameWordExp(
			jaBookId2BookNameWordExp,
			zhBookId2BookNameWordExp,
			enBookId2BookNameWordExp,
			viBookId2BookNameWordExp,
			myBookId2BookNameWordExp)
	}
	if setting.DicLangOrder == "zh" {
		return combineBookId2BookNameWordExp(
			zhBookId2BookNameWordExp,
			jaBookId2BookNameWordExp,
			enBookId2BookNameWordExp,
			viBookId2BookNameWordExp,
			myBookId2BookNameWordExp)
	}
	if setting.DicLangOrder == "vi" {
		return combineBookId2BookNameWordExp(
			viBookId2BookNameWordExp,
			enBookId2BookNameWordExp,
			zhBookId2BookNameWordExp,
			jaBookId2BookNameWordExp,
			myBookId2BookNameWordExp)
	}
	if setting.DicLangOrder == "my" {
		return combineBookId2BookNameWordExp(
			myBookId2BookNameWordExp,
			enBookId2BookNameWordExp,
			zhBookId2BookNameWordExp,
			jaBookId2BookNameWordExp,
			viBookId2BookNameWordExp)
	}

	// TODO: According to Language Settings in Browser
	return combineBookId2BookNameWordExp(
		enBookId2BookNameWordExp,
		zhBookId2BookNameWordExp,
		jaBookId2BookNameWordExp,
		viBookId2BookNameWordExp,
		myBookId2BookNameWordExp)
}
