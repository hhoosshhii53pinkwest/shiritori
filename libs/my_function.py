# -*- coding: utf-8 -*-
import json
import random
import collections


def mid(text,s,e):
	return text[s-1:s+e-1]

def left(text,e):
	return text[:e]

def right(text,s):
	return text[-s:]

def getkunimeilist():
    dic = {}
    for key in COUNTRYDATA:
        if not key["no"] in dic.keys() :
            dic[key["no"]]=key["name"]
    return dic

# 辞書{'ア':['アイスランド','アイルランド'....],'イ':['イエメン','イギリス'....].....} の形にするが最後にンがつくものは除外
def makekanalistNotnn():
	kanalist = {}
	for i in range(1,len(KATAKANA)+1):
		kanas = []
		j = 1
		for key in COUNTRYNAMELIST:
			if left(COUNTRYNAMELIST[key],1) == mid(KATAKANA,i,1) and right(COUNTRYNAMELIST[key],1) != "ン" :
				kanas.append(COUNTRYNAMELIST[key])
				j = j +1
		kanalist[mid(KATAKANA,i,1)] = kanas
	return kanalist

# 辞書{'ア':['アイスランド','アイルランド'....],'イ':['イエメン','イギリス'....].....} の形にするが「ン」で終わるものを取得
def makekanalistGetnn():
	kanalist = {}
	for i in range(1,len(KATAKANA)+1):
		kanas = []
		j = 1
		for key in COUNTRYNAMELIST:
			if left(COUNTRYNAMELIST[key],1) == mid(KATAKANA,i,1) and right(COUNTRYNAMELIST[key],1) == "ン" :
				kanas.append(COUNTRYNAMELIST[key])
				j = j +1
		kanalist[mid(KATAKANA,i,1)] = kanas
	return kanalist

# makekanalistNotnnのリストから指定した文字で始まる国名を適当に選ぶ
def kunichoice(kana):
	val =""
	if len(stock[kana]) == 0 :
		if len(nstock[kana]) != 0 :
			val = random.choice(nstock[kana])
			memoryRemark(val)
			delnstock(kana,val)
		val= val + "・・・もう【"+kana+"】から始まる国名は答えられません、負けました。リセットしてください"
		if penalty !=0 :
			val= val +" ペナルティ合計は(" +str(penalty) +"回)でした"
	else :
		val = random.choice(stock[kana])
		memorylastword(val)
		reqstockappend(val)
		delstock(kana,val)
		rest = len(stock[kana])
		memoryRemark(val)
		val = val + "・・・【"+kana+"】のこり【"+str(rest)+"】" + "次のことばは【"+getshiri(val)+"】です"
	return val

# その国名がしりとりで存在するかどうか
def checkExistenceKuni(req):
	if req in COUNTRYNAMELIST.values():
		return True
	else :
		return False

# その国名がそもそも存在するかどうか
def checkExistenceAllKuni(req):
	for key in COUNTRYDATA:
		if req == key["name"] :
			return True
	return False

# しりとりメソッド
def shiritori(req):
	atama = left(req,1)
	shiri = getshiri(req)
	if shiri == "ン":
		global penalty
		penalty = penalty +1
		return "「ン」で終わるやつは駄目です ペナルティ(" +str(penalty) +"回)"
	else :
		if req in stock[atama]:
			delstock(atama,req)
		return kunichoice(shiri)

# 末尾の文字を調整する
def getshiri(req):
	shiri = right(req,1)
	if shiri in "ァィゥェォッャュョヮヵヶ" :
		shiri = shiri.replace("ァ","ア")
		shiri = shiri.replace("ィ","イ")
		shiri = shiri.replace("ゥ","ウ")
		shiri = shiri.replace("ェ","エ")
		shiri = shiri.replace("ォ","オ")
		shiri = shiri.replace("ッ","ツ")
		shiri = shiri.replace("ャ","ヤ")
		shiri = shiri.replace("ュ","ユ")
		shiri = shiri.replace("ョ","ヨ")
		shiri = shiri.replace("ヮ","ワ")
		shiri = shiri.replace("ヵ","カ")
		shiri = shiri.replace("ヶ","ケ")
	# 長音対策
	if shiri == "ー" :
		shiri = mid(req,len(req)-1,1)
	return shiri

# 一度使ったものはストックから消す
def delstock(kana,val):
	stock[kana].remove(val)

# 一度使ったものはストックから消す
def delnstock(kana,val):
	nstock[kana].remove(val)

# 一度使ったものを覚える
def reqstockappend(req):
	reqstock.append(req)

# 一度使ったことがあるかどうかしらべる
def checkExistencereq(req):
	if req in reqstock:
		return True
	else:
		return False

# 何回言われてるか調べて返す
def countreqstock(req):
	global penalty
	penalty = penalty +1
	return req + "は【" + str(reqstock.count(req)+1) + "】回目です。できれば違う国名を言ってください ペナルティ(" +str(penalty) +"回)"

#　リセット
def reset():
	global stock
	global nstock
	global lastWord
	global reqstock
	global penalty 
	penalty = 0
	lastWord =""
	stock = makekanalistNotnn()
	nstock = makekanalistGetnn()
	reqstock.clear()

# ヒント
def hint(req):
	global penalty
	if req in stock:
		penalty = penalty + 1
		return stock[req]
	else:
		return "カタカナ一文字でお願いします"

# 詳細機能
def getkunidetail(req):
	ret = ""
	for key in COUNTRYDATA:
		if key["name"] == req :
			ret = ret + str(key) + "\n"
	return ret

# 最後の文字を覚える
def memorylastword(req):
	global lastWord
	lastWord = getshiri(req)

# しりとりになってるか調べる
def checkTruelastword(req):
	if lastWord != left(req,1) and not lastWord=="":
		return False
	else :
		return True

# しりとりになってないメッセージ
def forgivelastword(req):
	global penalty
	penalty = penalty + 1
	return req + "はしりとりになっていません。【"+lastWord+"】から始まる国名を言ってください ペナルティ(" +str(penalty) +"回)"


# 呼ばれたものを記憶
def memoryRemark(req):
	remarkstock.append(req)

# ランキングカウント
def remarkRanking():
	ret =""
	i = 0
	c = collections.Counter(remarkstock)
	for item in c.most_common() :
		i=i+1
		if i > 5 :
			break
		ret = ret + str(item[0]) + "　" + str(item[1]) + "回"+ "\n"
	return ret



# 定数群
KATAKANA = "アイウエオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤユヨラリルレロワヲンヴ"
COUNTRYDATA = json.load(open("C:/shiritori-country/libs/country_data.json","r",encoding="utf-8"))
COUNTRYNAMELIST = getkunimeilist()

# 変数群
stock = makekanalistNotnn()
nstock = makekanalistGetnn()
remarkstock=[]
reqstock =[]
lastWord =""
penalty =0


