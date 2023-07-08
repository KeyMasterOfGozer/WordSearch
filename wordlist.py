from dataclasses import dataclass, field
from typing import List

LETTERS=[
    {"values":"e","weight":18},
    {"values":"t","weight":17},
    {"values":"ainos","weight":16},
    {"values":"h","weight":15},
    {"values":"r","weight":14},
    {"values":"d","weight":13},
    {"values":"l","weight":12},
    {"values":"u","weight":11},
    {"values":"cm","weight":10},
    {"values":"f","weight":9},
    {"values":"wy","weight":8},
    {"values":"gp","weight":7},
    {"values":"b","weight":6},
    {"values":"v","weight":5},
    {"values":"k","weight":4},
    {"values":"q","weight":3},
    {"values":"jx","weight":2},
    {"values":"z","weight":1},
    ]

@dataclass
class WordList():
	words: List[str] = field(default_factory=list)
	needed: str = ''
	disallowed: str = ''
	length: int = -1
	threshold : int = 20
	wordFile: str = 'english-words/words_alpha.txt'
	selfReport: bool = True
	skips:str=''
	sortedList: List[str] = field(default_factory=list)
	bestWord:str=''
	bestIndex:int=0
	prefChars:str=''

	def count(self):
		return len(self.words)

	def results(self):
		if self.selfReport:
			cnt = self.count()
			if cnt <= self.threshold:
				print("Word List:")
				for word in self.words:
					print(word)
			else:
				print("Word Count: {cnt}".format(cnt=cnt))

	def __post_init__(self):
		if len(self.words) == 0: 
			self.load_words()
		if self.length > 0: self.len(self.length)

	def load_words(self,FileName=''):
		if FileName != '': self.wordFile = FileName
		with open(self.wordFile) as word_file:
			self.words = set(word_file.read().split())
		newList=[]
		for word in self.words:
			if 1 in [c in word for c in 'aeiouy']:
				newList.append(word)
		self.words = newList
		with open('banned.txt') as word_file:
			banned = set(word_file.read().split())
		for word in banned:
			self.remove(word)
		self.results()

	def len(self,length:int):
		newList=[]
		for word in self.words:
			if len(word) == length:
				newList.append(word)
		self.words = newList
		self.length = length
		self.results()
		
	def force(self,letter:str,position:int):
		newList=[]
		for word in self.words:
			if word[position-1] == letter[0]:
				newList.append(word)
		self.words = newList
		self.results()

	def ban(self,letter:str,position:int):
		newList=[]
		for word in self.words:
			if word[position-1] != letter[0]:
				newList.append(word)
		self.words = newList
		self.results()

	def remove(self,word:str):
		if word in self.words: self.words.remove(word)

	def disallow(self,charList: str):
		newList=[]
		for word in self.words:
			if 1 not in [c in word for c in charList]:
				newList.append(word)
		self.words = newList
		self.disallowed = ''.join(sorted(list(set(self.disallowed+charList))))
		self.results()

	def need(self,charList: str):
		newList=[]
		for word in self.words:
			if 0 not in [c in word for c in charList]:
				newList.append(word)
		self.words = newList
		self.needed = ''.join(sorted(list(set(self.needed+charList))))
		self.results()

	def numMatches(self,ustr:str,charList:str):
		cnt=0
		for letter in charList:
			if letter in ustr:
				cnt += 1
		return cnt

	def wordVal(self,word:str):
		value=0
		ustr=''.join(sorted(list(set(word))))
		for letter in LETTERS:
			charList=''.join(sorted(list(set(letter["values"])-set(self.skips))))
			if len(charList)> 0:
				value += self.numMatches(ustr,charList)*letter["weight"]
		if len(self.prefChars)> 0:
			value += self.numMatches(ustr,self.prefChars)*10
		return value

	def sortList(self):
		self.sortedList = sorted(self.words, key=self.wordVal, reverse=True)

	def show(self,num:int=10,verbose:bool=False):
		def printList(name:str,l:List[str]):
			items=""
			for item in l[0:num]:
				items= items+" "+item
			if len(l)<num+1:
				elp=""
			else:
				elp="..."
			print("{name}: {length}".format(name=name,length=len(l)))
			print("\t[{words}{elp}]".format(words=items.strip(),elp=elp))
		printList('words',self.words)
		printList('sortedList',self.sortedList)
		print("bestWord: {s}".format(s=self.bestWord))
		if verbose:
			print("needed: {s}".format(s=self.needed))
			print("disallowed: {s}".format(s=self.disallowed))
			print("length: {s}".format(s=self.length))
			print("skips: {s}".format(s=self.skips))
