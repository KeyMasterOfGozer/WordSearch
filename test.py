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
w.genWordFile()
w.genLetterFreqFile()

newWordFreq={}

for word,cnt in w.wordFreq.items():
    newWordFreq[word.replace('th','þ')]=cnt

w.wordFreq=newWordFreq

w.genWordFreqFile()


# Load WordList from newly gened files
w=WordList(	
    dictionary = 'word-gen.txt',
	wordFrequencyFile = 'word-freq-gen.txt',
	LetterFrequencyFile = 'letter-freq-gen.txt'
    )


# Decode
cypher="""f qtsl rjxxflj htsyfnsx qtyx tk
xyfynxynhfq hqzjx ymfy hfs gj
zxji yt fsfqdxj bmfy ymj rtxy
kwjvzjsy qjyyjwx fwj, fsi jajs
ymj rtxy htrrts ufnwx tw ywnuqjx
tk qjyyjwx hfs mjqu yt gwjfp
ymj htij"""
from decoder import Decoder
d=Decoder(cypher)
d.printStatus()
d.solveLetter('j','e')
d.solveLetter('y','t')
d.applyNewMatches()

d.checkWord('gwjfp')
d.wordList.show(20)



# Decode with Thorn Included Cypher
cypher="""ieþtw sft adpwy le þsdt syvswctm,
anl xt oeef mhsdd lskt xtpf
chswctm le gpvt xtpf defy xtpf
aenwlr meiw,
me xsl meew xt ipwt þsr bdei.
"""
from decoder import Decoder
d=Decoder(
    cypher=cypher,
    dictionary = 'word-gen.txt',
	wordFrequencyFile = 'word-freq-gen.txt',
	LetterFrequencyFile = 'letter-freq-gen.txt'
    )
d.printStatus()
d.solveLetter('t','e')
d.solveLetter('e','o')
d.solveLetter('s','a')
d.solveLetter('f','r')
d.solveLetter('w','n')
d.solveLetter('m','s')
d.applyNewMatches()
d.applyNewMatches()
d.solveLetter('d','l')
d.solveLetter('p','i')
d.applyNewMatches()
d.solveLetter('l','t')
d.applyNewMatches()
d.solveLetter('l','t')
d.solveLetter('x','þ')
d.checkWord('þsdt')
d.wordList.show(20)
d.solveLetter('þ','m')
d.checkWord('ieþtw')
d.wordList.show(20)
d.solveLetter('i','w')
d.solveLetter('o','p')
d.solveLetter('k','k')
d.solveLetter('g','g')
d.solveLetter('b','f')
"""
**********
 Cypher Frequency Order:teswfdplmxiþaycvnhrokgb
                Matches:eoanrlitsþwmbdcvuhypkgf
Natural Frequency Order:eisarntolcdugpmhbyfkvwþxzjq
**********
ieþtw sft adpwy le þsdt syvswctm,
anl xt oeef mhsdd lskt xtpf
chswctm le gpvt xtpf defy xtpf
aenwlr meiw,
me xsl meew xt ipwt þsr bdei.

**********
women are blind to male advances,
but þe poor shall take þeir
chances to give þeir lord þeir
bounty sown,
so þat soon þe wine may flow.

**********
"""

