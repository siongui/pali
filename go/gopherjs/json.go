package main

import "github.com/siongui/pali/go/lib"
import "encoding/json"
import "io"

func DecodeHttpRespWord(respBody io.ReadCloser) (wi lib.WordInfo) {
	dec := json.NewDecoder(respBody)
	// handle err here?
	dec.Decode(&wi)
	return
}

func DecodeWordJson(w string) lib.WordInfo {
	wi := lib.WordInfo{}
	err := json.Unmarshal([]byte(w), &wi)
	if err != nil {
		panic(err)
	}
	return wi
}

func GetDicIndex() lib.DicIndex {
	di := lib.DicIndex{}
	err := json.Unmarshal(dicIndexJsonBlob, &di)
	if err != nil {
		panic(err)
	}
	return di
}

var dicIndexJsonBlob = []byte(`{"A":{"lang":"ja","separator":" -","name":"《パーリ語辞典》","author":"増補改訂パーリ語辞典  水野弘元著"},"B":{"lang":"my","separator":"。","name":"Pali Myanmar Dictionary","author":"Pali Word Grammar from Pali Myanmar Dictionary"},"C":{"lang":"en","separator":"\u003cbr\u003e","name":"Concise P-E Dictionary    ","author":"Concise Pali-English Dictionary by A.P. Buddhadatta Mahathera"},"D":{"lang":"zh","separator":"~","name":"《巴漢詞典》","author":"《巴漢詞典》Mahāñāṇo Bhikkhu編著"},"E":{"lang":"vi","separator":"。","name":"Pali Viet Abhi- Terms","author":"Pali Viet Abhidhamma Terms  Từ điển các thuật ngữ Vô Tỷ Pháp của ngài Tịnh Sự, được chép từ phần ghi chú thuật ngữ trong các bản dịch của ngài."},"F":{"lang":"zh","separator":"。","name":"《巴漢詞典》","author":"《巴漢詞典》明法尊者增訂"},"G":{"lang":"zh","separator":"。","name":"《巴利語字彙》","author":"四念住課程開示集要巴利語字彙（葛印卡）"},"H":{"lang":"zh","separator":" -","name":"《漢譯パーリ語辭典》","author":"漢譯パーリ語辭典 黃秉榮譯"},"I":{"lang":"en","separator":"。","name":"Pali-Dictonary from VRI","author":"Pali-Dictionary Vipassana Research Institute"},"J":{"lang":"zh","separator":"。","name":"《パーリ語辭典-勘誤表》","author":"《水野弘元-巴利語辭典-勘誤表》 Bhikkhu Santagavesaka 覓寂尊者"},"K":{"lang":"my","separator":"。","name":"Tipiṭaka Pāḷi-Myanmar Dictionary","author":"Tipiṭaka Pāḷi-Myanmar Dictionary တိပိဋက-ပါဠိျမန္မာ အဘိဓာန္"},"M":{"lang":"zh","separator":"。","name":"《巴利語彙解》","author":"巴利語彙解\u0026巴利新音譯 瑪欣德尊者"},"N":{"lang":"en","separator":"\u003cbr\u003e","name":"Buddhist Dictionary","author":"Buddhist Dictionary by NYANATILOKA MAHATHERA"},"O":{"lang":"my","separator":"。","name":"Pali Roots Dictionary","author":"Pali Roots Dictionary ဓါတ္အဘိဓာန္"},"P":{"lang":"en","separator":"\u003ci\u003e","name":"PTS P-E Dictionary","author":"PTS Pali-English dictionary The Pali Text Society's Pali-English dictionary"},"Q":{"lang":"vi","separator":"。","name":"Pali Viet Vinaya Terms","author":"Pali Viet Vinaya Terms  Từ điển các thuật ngữ về luật do tỳ khưu Giác Nguyên sưu tầm."},"R":{"lang":"my","separator":"。","name":"U Hau Sein’s Pāḷi-Myanmar Dictionary","author":"U Hau Sein’s Pāḷi-Myanmar Dictionary ပါဠိျမန္မာ အဘိဓာန္(ဦးဟုတ္စိန္)"},"S":{"lang":"ja","separator":" -","name":"《パーリ語辞典》","author":"パーリ語辞典  水野弘元著"},"T":{"lang":"zh","separator":" -","name":"《漢譯パーリ語辭典》","author":"漢譯パーリ語辭典 李瑩譯"},"U":{"lang":"vi","separator":"。","name":"Pali Viet Dictionary","author":"Pali Viet Dictionary  Bản dịch của ngài Bửu Chơn."},"V":{"lang":"en","separator":"。","name":"Pali Proper Names Dictionary","author":"Buddhist Dictionary of Pali Proper Names by G P Malalasekera"},"W":{"lang":"zh","separator":"。","name":"《巴英術語彙編》","author":"巴英術語彙編 《法的醫療》附 溫宗堃"},"X":{"lang":"zh","separator":"。","name":"《巴利語入門》","author":"《巴利語入門》釋性恩(Dhammajīvī)"},"Z":{"lang":"zh","separator":"。","name":"《巴漢佛學辭彙》","author":"巴利文-漢文佛學名相辭彙 翻譯：張文明"}}`)
