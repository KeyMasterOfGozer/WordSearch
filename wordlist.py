from dataclasses import dataclass, field
from typing import List
import json
from operator import and_, or_, contains

@dataclass
class WordList():
	words: List[str] = field(default_factory=list)
	needed: str = ''
	disallowed: str = ''
	length: int = -1
	threshold : int = 20
	wordFile: str = 'english-words/words_alpha.txt'

	def count(self):
		return len(self.words)

	def results(self):
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
