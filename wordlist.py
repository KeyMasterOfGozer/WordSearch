from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class WordList():
	words: List[str] = field(default_factory=list)
	needed: str = ''
	disallowed: str = ''
	length: int = -1
	threshold : int = 20
	dictionary: str = 'dictionary/popular.txt'
	wordFrequencyFile: str = 'wikipedia-word-frequency/results/enwiki-2023-04-13.txt'
	LetterFrequencyFile: str = 'letter-freq-eng-text.txt'
	selfReport: bool = True
	skipInit: bool = False
	skips:str=''
	sortedList: List[str] = field(default_factory=list)
	bestWord:str=''
	bestIndex:int=0
	prefChars:str=''
	wordFreq: Dict = field(default_factory=dict)
	letterFreq: Dict = field(default_factory=dict)

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
		if not self.skipInit:
			self.loadWordFreq()
			self.loadLetterFreq()
			if len(self.words) == 0: 
				self.loadWords()
			if self.length > 0: self.len(self.length)

	def loadWords(self,FileName=''):
		if FileName != '': self.dictionary = FileName
		with open(self.dictionary) as word_file:
			self.words = set(word_file.read().split())
		newList=['a','i']
		for word in self.words:
			if 1 in [c in word for c in 'aeiouy']:
				newList.append(word)
		self.words = newList
		with open('banned.txt') as word_file:
			banned = set(word_file.read().split())
		for word in banned:
			self.remove(word)
		tmpList = sorted(self.words, key=self.wordFreqVal, reverse=True)
		self.words=tmpList
		self.results()

	def loadWordFreq(self,FileName=''):
		if FileName != '': self.wordFrequencyFile = FileName
		with open(self.wordFrequencyFile) as word_file:
			wordFreqList = list(set(word_file.read().split('\n')))
		wordFreq={}
		for word in wordFreqList:
			w=word.split(' ')
			if len(w)>1:
				if w[0] not in wordFreq:
					wordFreq[w[0]]=int(w[1])
		self.wordFreq=wordFreq

	def loadLetterFreq(self,FileName=''):
		if FileName != '': self.LetterFrequencyFile = FileName
		with open(self.LetterFrequencyFile) as word_file:
			letterFreqList = list(set(word_file.read().split('\n')))
		letterFreq={}
		for letter in letterFreqList:
			l=letter.split(' ')
			if len(l)>1:
				letterFreq[l[0]]=float(l[1])
		self.letterFreq=letterFreq

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

	def wordFreqVal(self,word:str):
		if word not in self.wordFreq:
			return 0
		else:
			return self.wordFreq[word]

	def wordVal(self,word:str):
		value=0
		ustr=''.join(sorted(list(set(word))))
		for letter,weight in self.letterFreq.items():
			charList=''.join(sorted(list(set(letter)-set(self.skips))))
			if len(charList)> 0:
				value += self.numMatches(ustr,charList)*weight
		if len(self.prefChars)> 0:
			value += self.numMatches(ustr,self.prefChars)*3
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

	def set(self,word:str):
		length=len(word)
		if self.length > 0 and self.length < length:
			length=self.length
			print("Parameter is longer than Word, only using first {n} characters.".format(n=length))
		for i in range(length):
			if word[i].isalpha():
				currentSelfReport=self.selfReport
				self.selfReport=False
				self.force(word[i],i+1)
				self.selfReport=currentSelfReport
		self.results()

	def contains(self,word:str):
		length=len(word)
		if self.length > 0 and self.length < length:
			length=self.length
			print("Parameter is longer than Word, only using first {n} characters.".format(n=length))
		for i in range(length):
			if word[i].isalpha():
				selfReport=self.selfReport
				self.selfReport=False
				self.need(word[i])
				self.ban(word[i],i+1)
				self.selfReport=selfReport
		self.results()

	def genLetterFreqFile(self,filename:str='letter-freq-gen.txt'):
		letters={}
		totalLetters=0

		for word in self.words:
			for letter in word:
				if letter in letters:
					letters[letter]+=1
				else:
					letters[letter]=1
				totalLetters+=1

		with open(filename,'w') as word_file:
			i=0
			for letter, cnt in letters.items():
				if i!=0: word_file.write("\n")
				i+=1
				word_file.write("{letter} {percent:.2f}".format(
					letter=letter,
					percent=cnt/totalLetters*100))

	def genWordFreqFile(self,filename:str='word-freq-gen.txt'):
		with open(filename,'w') as word_file:
			i=0
			for word, cnt in self.wordFreq.items():
				if i!=0: n=word_file.write("\n")
				i+=1
				n=word_file.write("{word} {cnt}".format(
					word=word,
					cnt=cnt))

	def genWordFile(self,filename:str='word-gen.txt'):
		with open(filename,'w') as word_file:
			i=0
			for word in self.words:
				if i!=0: n=word_file.write("\n")
				i+=1
				n=word_file.write(word)
