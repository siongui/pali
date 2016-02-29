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

const HtmlTemplateSuggestedWords = `
{{range $word := .}}
<div>{{$word}}</div>
{{end}}`

type PaliDictionarySetting struct {
	IsShowWordPreview bool   `json:"isPreview"`
	P2en              bool   `json:"p2en"`
	P2ja              bool   `json:"p2ja"`
	P2zh              bool   `json:"p2zh"`
	P2vi              bool   `json:"p2vi"`
	P2my              bool   `json:"p2my"`
	DicLangOrder      string `json:"dicLangOrder"`
}

func IdExps2BookNameWordExps(ies []IdExp, di BookIdAndInfos) []BookNameWordExp {
	var result []BookNameWordExp

	for _, ie := range ies {
		result = append(result, BookNameWordExp{
			BookName:    di[ie.Id].Author,
			Explanation: template.HTML(ie.Exp),
		})
	}

	return result
}
