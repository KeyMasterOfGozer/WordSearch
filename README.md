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
d.solveLetter('j','e')
d.solveLetter('y','t')
d.applyNewMatches()
```

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
