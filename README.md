# WordSearch helper

This is intended as a helper to find guesses to plug in for wordl type games.  
 
## Classes

There are 3 main components written as python classes. It's my preference to use it from a python commandline, but the classes could be used by anohter program as well.

### WordList
This class loads a dictionary of words (default is [Dolph's popular English words](https://github.com/dolph/dictionary), but any dictionary can be set), which it uses to build a WordList that can be filtered through various commands to whittle down a minimal list of words to pick from.

It sorts words based on number of uses in Wikipedia via the [Wikipedia Word Frequency](https://github.com/IlyaSemenov/wikipedia-word-frequency) project by Ilya Semenov to help pick more common words.

To help pick a word when you have no information, it uses uses a table of letter frequncies in the English language (this is a setting, so other languages or variations could also be used.) to try to pick words with the most likelihood of getting some letter information for the word, while taking any filters you've given it into account.

You can initialize your WordList like this:
```python
from wordlist import WordList
w = WordList()
```
There are several filters that can be applied.

#### Len (Length)
This filters the word list to only words of this length.
```python
# Filter down to only words with 3 letters
w.len(3)
```
#### Set/Force
This is for *green* letters in Wordl.  Letters that are in the word and in the correct location.
```python
# Filter down to only words with an A in the 3 character.
w.force('a',3)
# Set the filter for multiple letters
# in this case H in then second letter and A in the 3 letter
w.set(' ha ')
```

#### Contains/Need/Ban
This is for *yellow* letters in Wordl.  Letters that are in the word but in the wrong location.
```python
# Filter down to only words with an A in some position.
w.need('a')
# Filter down to words that don't have A in the 3rd position
w.ban('a',3)
# Set the filter for multiple letters, doing NEED and BAN
# in this case, the word must have H and A somewhere, but
#  H can't be in then second position and A can't be 3rd
w.set(' ha ')
```

#### Disallow
This is for *black* letters in Wordl.  Letters that are not in the word.
```python
# Filter out words that have A, B, or C in any position.
w.disallow('abc')
```

### Decoder
This class makes use of the WordLost class to help a user decypher a simple substitution cypher.

#### Load up the cypher
```python
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
```
The printStatus() function will print out where you currently are in the solve.
```
>>> d.printStatus()
jyfxtsqwhmrnkziulgdbvap

etaoinshrdlcumwfgypbvkjxqz
**********
f qtsl rjxxflj htsyfnsx qtyx tk
xyfynxynhfq hqzjx ymfy hfs gj
zxji yt fsfqdxj bmfy ymj rtxy
kwjvzjsy qjyyjwx fwj, fsi jajs
ymj rtxy htrrts ufnwx tw ywnuqjx
tk qjyyjwx hfs mjqu yt gwjfp
ymj htij
**********
- ---- ------- -------- ---- --
----------- ----- ---- --- --
---- -- ------- ---- --- ----
-------- ------- ---, --- ----
--- ---- ------ ----- -- -------
-- ------- --- ---- -- -----
--- ----
```
Notice the first line shows the letters used in the cypher text in order of its frequency used in the text.  The third line shows expected letter frequency in the loaded language's letter frequency file.  In this case, "j" is the most used letter in the cypher, so it is likely "e", since that's the most used letter in English.  Also, the second characters "y" probably matches to "t".  Let's try that.

#### solveLetter(old:str,new:str)
```python
d.solveLetter('j','e')
d.solveLetter('y','t')
```
solveLetter() applies the matches to the solve text and shows the matches in the second line when it automatically does a printStatus() for you.

If you think you have a wrong Match, you can back it out by applying a space to replace the wrong match to "Erase" it.
```python
d.solveLetter('x',' ')```

```
>>> d.solveLetter('y','t')
jyfxtsqwhmrnkziulgdbvap
et
etaoinshrdlcumwfgypbvkjxqz
**********
f qtsl rjxxflj htsyfnsx qtyx tk
xyfynxynhfq hqzjx ymfy hfs gj
zxji yt fsfqdxj bmfy ymj rtxy
kwjvzjsy qjyyjwx fwj, fsi jajs
ymj rtxy htrrts ufnwx tw ywnuqjx
tk qjyyjwx hfs mjqu yt gwjfp
ymj htij
**********
- ---- -e----e ---t---- --t- --
-t-t--t---- ---e- t--t --- -e
--e- t- ------e ---t t-e ---t
--e--e-t -ette-- --e, --- e-e-
t-e ---t ------ ----- -- t----e-
-- -ette-- --- -e-- t- --e--
t-e ---e
Word xyfynxynhfq is statistical
Word qjyyjwx is letters
Word qjyyjwx is letters
New Matches: {'x': 's', 'f': 'a', 'n': 'i', 'h': 'c', 'q': 'l', 'w': 'r'}
```

Notice how at the bottom, it shows any words that only have 1 match in the dictionary.  These words are likely found.  It also tells you the letter matches that you haven't yet applied if these words are correct.  You can get it to automatically fill in those with the applyNewMatches() function.

#### applyNewMatches()
This function will cycle through applying all the new Matches found in the previous solveLetter().  it will do this by running solveLetter() for each match found.
```python
d.applyNewMatches()
```
Notice that after applying all those matches, we find more matched words with more New Matches.  You can simply run applyNewMatches() again to fill in the newly found words.
```
jyfxtsqwhmrnkziulgdbvap
etas  lrc  i
etaoinshrdlcumwfgypbvkjxqz
**********
f qtsl rjxxflj htsyfnsx qtyx tk
xyfynxynhfq hqzjx ymfy hfs gj
zxji yt fsfqdxj bmfy ymj rtxy
kwjvzjsy qjyyjwx fwj, fsi jajs
ymj rtxy htrrts ufnwx tw ywnuqjx
tk qjyyjwx hfs mjqu yt gwjfp
ymj htij
**********
a l--- -essa-e c--tai-s l-ts --
statistical cl-es t-at ca- -e
-se- t- a-al-se --at t-e --st
-re--e-t letters are, a-- e-e-
t-e --st c----- -airs -r tri-les
-- letters ca- -el- t- -rea-
t-e c--e
Word rjxxflj is message
Word hqzjx is clues
Word fsfqdxj is analyse
Word ywnuqjx can't be solved(tri les).
New Matches: {'r': 'm', 'l': 'g', 'z': 'u', 's': 'n', 'd': 'y'}
```
Notice also that a word was found that can't be solved.  This means there is no word in the dictionary that can match this pattern.  In many cases this can indicated that you have a badly matches letter.  In this case, the word in the cypher "triples" is simply not in this dictionary.  Sometimes, a cypher might contain proper names of other words that might not be in the dictionary.

Continue using applyNewMatches() until no new matches are found.
```
jyfxtsqwhmrnkziulgdbvap
etasonlrc mifu  g y qv
etaoinshrdlcumwfgypbvkjxqz
**********
f qtsl rjxxflj htsyfnsx qtyx tk
xyfynxynhfq hqzjx ymfy hfs gj
zxji yt fsfqdxj bmfy ymj rtxy
kwjvzjsy qjyyjwx fwj, fsi jajs
ymj rtxy htrrts ufnwx tw ywnuqjx
tk qjyyjwx hfs mjqu yt gwjfp
ymj htij
**********
a long message contains lots of
statistical clues t-at can -e
use- to analyse --at t-e most
frequent letters are, an- even
t-e most common -airs or tri-les
of letters can -el- to -rea-
t-e co-e
Word ywnuqjx can't be solved(tri les).
New Matches: {}
```
#### See possible word matches
You can make use of the WordList object to see if there are good matches for a cyphered word.
```python
>>> d.checkWord('gwjfp')
(12, ' rea ')
>>> d.wordList.show(20)
words: 12
	[great areas break dream treat cream bread freak dread tread wreak creak]
sortedList: 0
	[]
bestWord:
```
Looks like in this case, there are 12 possible matches for "gwjfp"=" rea ".  You can show them and see if any of them seem to match the cypher.  If so, then you can solveLetter() for any of those matches and continue.


### Phrase
This class is designed for [Phrazle](https://solitaired.com/phrazle) and other multiple word Wordl clones.
```python
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
```
