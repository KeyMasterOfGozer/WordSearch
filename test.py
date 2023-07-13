from wordlist import WordList

w = WordList()
w.load_words()
w.len(4)
w.force('a',1)
w.disallow('th')
w.need('b')


from phrase import Phrase
p=Phrase([4,3,9,5])
p.disallow('')
p.set(['','','',''])
p.contains(['','','',''])
p.wrongWord(['','','',''])
p.wordDisallow('',1)
p.wordDisallow('',2)
p.wordDisallow('',3)
p.wordDisallow('',4)
p.sortWords()
p.bestWords()

p.list()


# Build Lists for including þ thorn in English Language
from wordlist import WordList
w = WordList()
newWords=[]

for word in w.words:
    newWords.append(word.replace('th','þ'))

w.words=newWords
w.genLetterFreqFile()

newWordFreq={}

for word,cnt in w.wordFreq.items():
    newWordFreq[word.replace('th','þ')]=cnt

w.wordFreq=newWordFreq

w.genWordFreqFile()
