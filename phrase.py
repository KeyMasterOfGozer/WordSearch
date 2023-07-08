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
            print("Word {i}:".format(i=i))
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
                        self.sortedList.insert(i,thisWord)
                        break
                    i+=1
    
    def bestWords(self):
        skips=''
        for word in self.sortedList:
            word.skips=skips
            i=0
            found=False
            for thisWord in word.sortedList:
                if 1 not in [c in thisWord for c in word.skips] and not found:
                    found=True
                    word.bestWord=thisWord
                    word.bestIndex=i
                    skips = ''.join(sorted(list(set(skips+thisWord))))
                i+=1
            if not found:
                thisWord=word.sortedList[0]
                word.bestWord=thisWord
                word.bestIndex=0
                skips = ''.join(sorted(list(set(skips+thisWord))))
        bestPhrase=''
        for word in self.words:
            bestPhrase += ' '+word.bestWord
        bestPhrase=bestPhrase.strip()
        print(bestPhrase)
               

