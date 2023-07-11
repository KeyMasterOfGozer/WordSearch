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
