from wordlist import WordList

w = WordList()
w.load_words()
w.len(4)
w.force('a',1)
w.disallow('th')
w.need('b')


from phrase import Phrase
p=Phrase([5,6])
p.disallow('ohrla')
p.words[0].disallow('e')
p.words[0].force('t',2)
p.words[0].need('is')
p.words[1].disallow('is')
p.words[1].force('d',6)
p.words[1].need('en')
p.results()

from phrase import Phrase
p=Phrase([3,3,5,2,4])
p.sortWords()
p.bestWords()



if 'pfg' in p.words[0].words: p.words[0].words.remove('pfg')
