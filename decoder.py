from dataclasses import dataclass, field
from typing import List, Dict
from wordlist import WordList

@dataclass
class Decoder():
    cypher: str
    solved: str = ''
    matches: Dict = field(default_factory=dict)
    newMatches: Dict = field(default_factory=dict)
    cypherLetters: Dict = field(default_factory=dict)
    cypherLetterList: List[float] = field(default_factory=list)
    clearLetters: Dict = field(default_factory=dict)
    clearLetterList: List[float] = field(default_factory=list)
    dictionary: str = 'dictionary/popular.txt'
    wordFrequencyFile: str = 'wikipedia-word-frequency/results/enwiki-2023-04-13.txt'
    LetterFrequencyFile: str = 'letter-freq-eng-text.txt'
    wordList: WordList = WordList(selfReport=False)

    def __post_init__(self):
        self.wordList=WordList(
            dictionary = self.dictionary,
            wordFrequencyFile = self.wordFrequencyFile,
            LetterFrequencyFile = self.LetterFrequencyFile
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
        if ' ' in decryptWord:
            newWord=True
        else:
            newWord=False
        self.wordList.loadWords()
        self.wordList.selfReport=False
        self.wordList.len(len(decryptWord))
        self.wordList.selfReport=False
        self.wordList.set(decryptWord)
        return len( self.wordList.words), newWord

    def checkWords(self):
        words=self.cypher.split()
        self.newMatches={}
        for word in words:
            cnt,newWord=self.checkWord(word)
            if cnt == 0:
                print("Word {cypher} can't be solved.".format(
                    cypher=word))
            elif cnt == 1 and newWord:
                print("Word {cypher} is {solve}".format(
                    cypher=word,
                    solve=self.wordList.words[0]
                    ))
                for i in range(len(self.wordList.words[0])):
                    if self.matches[word[i]] == ' ':
                        self.newMatches[word[i]]=self.wordList.words[0][i]
        print("New Matches: {nm}".format(nm=self.newMatches))

    def solveLetter(self,old:str,new:str):
        newsub=''
        for i in range(len(self.cypher)):
            if self.cypher[i]==old:
                newsub=newsub+new
            else:
                newsub=newsub+self.solved[i]
        self.solved=newsub
        self.matches[old]=new
        self.printStatus()
        self.checkWords()

    def applyNewMatches(self):
        for old,new in self.newMatches.items():
            self.solveLetter(old,new)

    def printStatus(self):
        matchList=[]
        for i in range(len(self.cypherLetterList)):
            matchList.append(self.matches[self.cypherLetterList[i]])
        print(''.join(self.cypherLetterList))
        print(''.join(matchList))
        print(''.join(self.clearLetterList))
        print('**********')
        print(self.cypher)
        print('**********')
        print(self.solved)
