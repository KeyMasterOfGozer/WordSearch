import json
import discord
import re
from decoder import Decoder


Verbosity = 0
SecurityFile = 'discord.json'
# Read in Security File
with open(SecurityFile,"r") as f:
	Security = json.load(f)

TOKEN = Security["Token"]

def Message(msg,lvl=0):
	# Send a message based on Debug level
	if lvl <= Verbosity:
		print(msg)

def parse(input,author,MultiLine=0):
	# parse the input string from the message so that we can see what we need to do
    parts = input.strip().split()
    Message(parts,1)

    AuthorName = author

	#drop out if this is not a Roll command
    if len(parts) == 0 or parts[0].upper() not in ['!','/','\\']:
		#Try to make a command if first character is !
        if parts[0][0]=="!":
            pt=["!",parts[0][1:],parts[1:]]
            parts=pt
        else:
            Message("Not a command",1)
            return None

    try:
        Message("Command: "+parts[1].upper(),1)
        if parts[1].upper() == "NEWCYPHER":
            cypher = ''.join(parts[2:])
            decoder = Decoder(cypher,
		        dictionary=language["dictionary"],
                wordFrequencyFile=language["wordFrequencyFile"],
                LetterFrequencyFile=language["LetterFrequencyFile"]
		        )
			#give user message so he knows it's saved
            retstr = "{Author} posed a new Cypher:\n{cypher}".format(
				Author=author,
		        cypher=decoder.cypher
		        )
        elif parts[1].upper() == "DICTIONARY":
            if len(parts)<5:
                retstr= """{Author}: The **dictionary** command must have 3 parameters.
Dictionary, Word Frequency File Name, and Letter Frequency Filename.
Example:
!dictionary dictionary/popular.txt wikipedia-word-frequency/results/enwiki-2023-04-13.txt letter-freq-eng-text.txt""".format(
					Author=AuthorName
		            )
            else:
                tempCypher = decoder.cypher
                language["dictionary"]=parts[2]
                language["wordFrequencyFile"]=parts[3]
                language["LetterFrequencyFile"]=parts[4]
                decoder = Decoder(tempCypher,
                    dictionary=language["dictionary"],
                    wordFrequencyFile=language["wordFrequencyFile"],
                    LetterFrequencyFile=language["LetterFrequencyFile"]
                    )
                retstr = "{Author}: {output}".format(
                     Author=AuthorName,
                     output=decoder._printStatus()
                     )
        elif parts[1].upper() == "USE":
			# run the macro
            retstr = ""
        elif parts[1].upper() in ["HELP"]:
            retstr = '''
My Key words are "!", "/", or "\\"
Make simple roll with:```/roll 2d6+4```
Add description text:```/roll 2d6+4 Sword Damage```
Print some text with no roll:```! echo Suck it monsters!!!!```
Can roll multiple kinds of dice:```! 3d6+2d4-4```
Use a semi-colon to execute multiple commands!
***Macros***
**Save**:```! define init 1d20+5 Intitative```
**Use**:```! use init```or just ```! init```
**List** your existing macros:```! list```
**Load** up set of macros:```! load {'dex':'! 1d20+9 Dex Save','str':'! 1d20+5 Str Save'}```
***Variables***
**Set**:```! set Proficiency +4```
**Use**:```! d20{Proficiency}+1 Sword to Hit```
Variables are essentially string replacements.  If you need to add or subtract, make sure to put plus and minus signs in the variable, or in the macro, but not both.

Macros can call macros.  Example:
A Gun Attack:```/roll define gun 1d20+12 Gun to hit```
Damage for the gun attack:```/roll define gun-dam 1d8+6 Piercing Damage```
Combo macro that uses the other 2 multiple times:```/roll define atk echo **Normal Gun Attack**; ! echo 1st Shot:; ! use gun; ! use gun-dam; ! echo 2nd Shot:; ! use gun; ! use gun-dam```
'''
        else:
            retstr = '{Author}, your command was not understood.'.format(Author=author)
    except Exception as e:
        print(e)
        retstr = None

    return retstr


#########################################################################
# Main Program
#########################################################################


client = discord.Client()
decoder = Decoder('')
language= {
    'dictionary':'dictionary/popular.txt',
    'wordFrequencyFile':'wikipedia-word-frequency/results/enwiki-2023-04-13.txt',
    'LetterFrequencyFile':'letter-freq-eng-text.txt'
    }

# This block is the work horse part
@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
	# get the output for the given message
	output = parse(message.content,message.author.display_name)
	if output is not None:
		await message.channel.send(output)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run(TOKEN)
