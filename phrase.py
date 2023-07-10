from dataclasses import dataclass, field
from typing import List
from wordlist import WordList

@dataclass
class Phrase():
    wordLengths: List[int] = field(default_factory=list)
    words: List[WordList] = field(default_factory=list)
    disallowed: str = ''
    sortedList: List[WordList] = field(default_factory=list)

    def wordReport(self,toReport:bool):
        for word in self.words:
            word.selfReport = toReport

    def results(self):
        i=1
        for word in self.words:
            print("*****\nWord {i}:".format(i=i))
            word.selfReport = True
            word.results()
            i+=1
 
    def __post_init__(self):
        if len(self.wordLengths) != 0: 
            for word in self.wordLengths:
                self.words.append(WordList(length=word,selfReport=False))
            self.wordReport(True)
            self.results()

    def disallow(self,charList: str):
        for word in self.words:
            self.wordReport(False)
            word.disallow(charList)
            self.wordReport(True)
        self.disallowed = ''.join(sorted(list(set(self.disallowed+charList))))
        self.results()

    def prefChars(self,charList: str):
        for word in self.words:
            word.prefChars=charList

    def wordSet(self,word:str,position:int):
        self.words[position-1].set(word)

    def wordContains(self,word:str,position:int):
        self.words[position-1].contains(word)

    def wordDisallow(self,word:str,position:int):
        self.words[position-1].disallow(''.join(filter(str.isalnum, word)))

    def set(self,wordList:List[str]):
        length=len(wordList)
        if len(self.words) < length:
            length=len(self.words)
            print("Parameter is longer than Words in Phrase, only using first {n} words.".format(n=length))
        for i in range(length):
            self.wordSet(wordList[i],i+1)

    def contains(self,wordList:List[str]):
        length=len(wordList)
        if len(self.words) < length:
            length=len(self.words)
            print("Parameter is longer than Words in Phrase, only using first {n} words.".format(n=length))
        for i in range(length):
            self.wordContains(wordList[i],i+1)

    def wrongWord(self,wordList:List[str]):
        length=len(wordList)
        if len(self.words) < length:
            length=len(self.words)
            print("Parameter is longer than Words in Phrase, only using first {n} words.".format(n=length))
        charList=''
        for i in range(length):
            filteredWord=''.join(filter(str.isalnum, wordList[i]))
            charList=charList+filteredWord
            for j in range(len(wordList[i])):
                if wordList[i][j].isalpha():
                    self.words[i].ban(wordList[i][j],j+1)
        self.prefChars(charList)

    def sortWords(self):
        for word in self.words:
            word.sortList()
            if len(self.sortedList)==0:
                self.sortedList.insert(0,word)
            else:
                i=0
                for thisWord in self.sortedList:
                    thisVal=thisWord.wordVal(thisWord.sortedList[0])
                    sVal=self.sortedList[i].wordVal(self.sortedList[i].sortedList[0])
                    if sVal >= thisVal:
                        self.sortedList.insert(i,word)
                        break
                    i+=1
    
    def bestWords(self):
        skips=''
        n=1
        for word in self.sortedList:
            #print("Word {i}:".format(i=n))
            #word.show()
            word.skips=skips
            i=0
            found=False
            for thisWord in word.sortedList:
                if 1 not in [c in thisWord for c in word.skips] and not found:
                    found=True
                    word.bestWord=thisWord
                    word.bestIndex=i
                    skips = ''.join(sorted(list(set(word.skips+thisWord))))
                i+=1
            if not found:
                thisWord=word.sortedList[0]
                word.bestWord=thisWord
                word.bestIndex=0
                skips = ''.join(sorted(list(set(word.skips+thisWord))))
            #print("Picked word: {s}".format(s=word.bestWord))
            n+=1
        bestPhrase=''
        for word in self.words:
            bestPhrase += ' '+word.bestWord
        bestPhrase="Best Guess: "+bestPhrase.strip()
        print(bestPhrase)
        bestPhrase=''
        for word in self.words:
            bestPhrase += ' '+word.words[0]
        bestPhrase="Freq Words: "+bestPhrase.strip()
        print(bestPhrase)
        bestPhrase=''
        for word in self.words:
            bestPhrase += ' '+word.sortedList[0]
        bestPhrase="Top Sorted: "+bestPhrase.strip()
        print(bestPhrase)
               
    def show(self,num:int=5):
        i=1
        for word in self.words:
            print("*****\nWord {i}:".format(i=i))
            word.selfReport = True
            word.show(num)
            i+=1
       
    def list(self,num:int=50):
        def printRow(row:List[str]):
            line = row[0]
            for word in row[1:]:
                line = line + " " + word
            print(line)

        i=0
        while i < num:
            row = []
            stuffOnRow=False
            j=0
            while j < len(self.words):
                #print("i={i},j={j},word='{word}'".format(i=i,j=j,word=self.words[j].sortedList[i]))
                if len(self.words[j].sortedList)<=i:
                    row.append("".ljust(self.words[j].length))
                else:
                    row.append(self.words[j].sortedList[i])
                    stuffOnRow=True
                j += 1
            if stuffOnRow: printRow(row)
            i += 1
