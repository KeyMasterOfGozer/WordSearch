from dataclasses import dataclass, field
from typing import List, Dict
from wordlist import WordList

@dataclass
class Decoder():
    cypher: str
    solved: str = ''
    matches: Dict = field(default_factory=dict)
    used: Dict = field(default_factory=dict)
    newMatches: Dict = field(default_factory=dict)
    cypherLetters: Dict = field(default_factory=dict)
    cypherLetterList: List[str] = field(default_factory=list)
    clearLetters: Dict = field(default_factory=dict)
    clearLetterList: List[str] = field(default_factory=list)
    dictionary: str = 'dictionary/popular.txt'
    wordFrequencyFile: str = 'wikipedia-word-frequency/results/enwiki-2023-04-13.txt'
    LetterFrequencyFile: str = 'letter-freq-eng-text.txt'
    wordList: WordList = field(default_factory=WordList)

    def __post_init__(self):
        self.wordList=WordList(
            dictionary = self.dictionary,
            wordFrequencyFile = self.wordFrequencyFile,
            LetterFrequencyFile = self.LetterFrequencyFile,
            selfReport=False
        )
        self.getCypherLetters()
        self.cypherLetterList=list(self.cypherLetters.keys())
        self.cypherLetterList=sorted(self.cypherLetterList,key=self.getCypherLetterVal,reverse=True)
        self.clearLetters=self.wordList.letterFreq
        self.clearLetterList=list(self.clearLetters.keys())
        self.clearLetterList=sorted(self.clearLetterList,key=self.getClearLetterVal,reverse=True)
        self.initMatches()

    def getCypherLetters(self):
        for letter in self.cypher:
            if letter.isalpha():
                if letter in self.cypherLetters:
                    self.cypherLetters[letter]+=1
                else:
                    self.cypherLetters[letter]=1
                self.solved=self.solved+'-'
            else:
                self.solved=self.solved+letter

    def initMatches(self):
        for letter in self.cypher:
            if letter.isalpha():
                self.matches[letter]=' '
        for letter in self.clearLetterList:
            if letter.isalpha():
                self.used[letter]=' '
 
    def getCypherLetterVal(self,key:str):
        return self.cypherLetters[key]

    def getClearLetterVal(self, key:str):
        return self.clearLetters[key]

    def checkWord(self,cypherWord:str):
        self.wordList.loadWords()
        decryptWord=''
        for letter in cypherWord:
            if letter.isalpha():
                decryptWord = decryptWord + self.matches[letter]
        self.wordList.loadWords()
        self.wordList.len(len(decryptWord))
        self.wordList.set(decryptWord)
        return len( self.wordList.words), decryptWord

    def _checkWords(self):
        words=self.cypher.split()
        retstr=''
        self.newMatches={}
        for word in words:
            cnt,decryptWord=self.checkWord(word)
            if cnt == 0:
                retstr = retstr + "Word {cypher} can't be solved({solve}).\n".format(
                    cypher=word,
                    solve=decryptWord
                    )
            elif cnt == 1 and ' ' in decryptWord:
                retstr = retstr + "Word {cypher} is {solve}\n".format(
                    cypher=word,
                    solve=self.wordList.words[0]
                    )
                for i in range(len(self.wordList.words[0])):
                    if self.matches[word[i]] == ' ':
                        self.newMatches[word[i]]=self.wordList.words[0][i]
        retstr = retstr + "New Matches: {nm}".format(nm=self.newMatches)
        return retstr

    def checkWords(self):
        print(self._checkWords())

    def _solveLetter(self,old:str,new:str):
        newsub=''
        for i in range(len(self.cypher)):
            if self.cypher[i]==old:
                newsub=newsub+new
            else:
                newsub=newsub+self.solved[i]
        self.solved=newsub
        self.matches[old]=new
        self.used[new]=old
        retstr = self._printStatus()
        retstr = retstr + self._checkWords()
        return retstr

    def solveLetter(self,old:str,new:str):
        print(self._solveLetter(old,new))
 
    def _applyNewMatches(self):
        retstr = ''
        for old,new in self.newMatches.items():
            retstr = self._solveLetter(old,new)
        return retstr

    def applyNewMatches(self):
        print(self._applyNewMatches())

    def _printStatus(self):
        matchList=[]
        for i in range(len(self.cypherLetterList)):
            matchList.append(self.matches[self.cypherLetterList[i]])
        usedList=[]
        for i in range(len(self.clearLetterList)):
            usedList.append(self.used[self.clearLetterList[i]])
        retstr="""
**********
 Cypher Frequency Order: {cypherLetters}
                Matches: {matches}
                   Used: {used}
Natural Frequency Order: {clearLetters}
**********
{cypher}
**********
{solved}
**********
""".format(
            cypherLetters=''.join(self.cypherLetterList),
            matches=''.join(matchList),
            used=''.join(usedList),
            clearLetters=''.join(self.clearLetterList),
            cypher=self.cypher,
            solved=self.solved
            )
        return retstr

    def printStatus(self):
        print(self._printStatus())