# Cryptogram Solver Discord Bot
I created the Decoder class to help me do Cryptogram solving.  It works great for me, but I wanted to share it with my friends.  They can't neccessarily easily use a python session, so it was essesntially only usable by me.  Since we already use a Discord server to meet up for our games, I decided to implement a quick interface for the Decoder class from within Discord.  I think it works great.

The discord bot requires a file "discord.json" in the folder of the script.  it must look like:

```javascript
{
	"Tokens":{
		"11House-Crypt":{
			"Token":"aroiusyghtbflaiwhgtlihw4itrehawilughtliuaygw4tliuawl4uktwgWsttw",
			"ClientID":"1232413434323543242345",
			"SecretKey":"awoiurtghl234hru234hgtb3j24bgtjgb34tbl3"
		}
	},
	"Languages": {
		"English":{
			"dictionary" : "dictionary/popular.txt",
			"wordFrequencyFile" : "wikipedia-word-frequency/results/enwiki-2023-04-13.txt",
			"LetterFrequencyFile" : "letter-freq-eng-text.txt"	
		},
		"ThornedEnglish":{
			"dictionary" : "word-gen.txt",
			"wordFrequencyFile" : "word-freq-gen.txt",
			"LetterFrequencyFile" : "letter-freq-gen.txt"	
		}
	}
}
```

I found this tutorial helpful in creating an app and getting it logged into our Discord Server.
(https://discordpy.readthedocs.io/en/stable/discord.html)

I jsut run the python with:
```bash
python3 discord-bot.py
```
The new discord.py stuff requires python 3.8 or better.