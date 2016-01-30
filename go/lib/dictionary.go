/*
The format of DicIndex:
DicIndex = object of key-value pairs, where
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

type DictInfo struct {
	Lang      string `json:"lang"`
	Separator string `json:"separator"`
	Name      string `json:"name"`
	Author    string `json:"author"`
}

// book id <-> book info
type DicIndex map[string]DictInfo

// book id <-> word explanation
type WordInfo map[string]string
