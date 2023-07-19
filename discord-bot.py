import json
import discord
from decoder import Decoder


Verbosity = 0
ConfigFile = 'discord.json'
# Read in Security File
with open(ConfigFile,"r") as f:
	Config = json.load(f)

TOKEN = Config["Tokens"]["11House-Crypt"]["Token"]
Languages = Config["Languages"]

def Message(msg,lvl=0):
	# Send a message based on Debug level
	if lvl <= Verbosity:
		print(msg)
                
def listWords(WordList:list):
    retstr=''
    i=1
    for word in WordList:
        if i%5!=1: retstr=retstr+" "
        retstr=retstr+word
        if i%5==0: retstr=retstr+"\n"
        i+=1
    return retstr

def parse(input,author):
	# parse the input string from the message so that we can see what we need to do
    parts = input.strip().split()
    Message(input,1)
    Message(parts,1)

    global decoder
    global language
    global Languages

    AuthorName = author

	#drop out if this is not a Roll command
    if len(parts) == 0:
        return None
    if parts[0].upper() not in ['!','/','\\']:
		#Try to make a command if first character is !
        if parts[0][0]=="!":
            pt=["!",parts[0][1:]]
            pt.extend(parts[1:])
            parts=pt
            Message(parts,1)
        else:
            Message("Not a command",1)
            return None

    try:
        Message("Command: "+parts[1].upper(),1)
        if parts[1].upper() == "NEWCYPHER":
            cypher = ' '.join(parts[2:])
            Message(cypher,1)
            decoder = Decoder(cypher,
                    dictionary=Languages[language]["dictionary"],
                    wordFrequencyFile=Languages[language]["wordFrequencyFile"],
                    LetterFrequencyFile=Languages[language]["LetterFrequencyFile"]
		        )
			#give user message so he knows it's saved
            retstr = "{Author} posed a new Cypher:\n{cypher}".format(
				Author=author,
		        cypher=decoder._printStatus()
		        )
            Message(retstr,1)
        elif parts[1].upper() == "LANGUAGE":
            invalidParams="""{Author}: The **Language** command must have 1 parameter.
It must be one of {langs}.
Example:
!language ThornedEnglish""".format(
					Author=AuthorName,
                    lang=Languages.keys()
		            )
            if len(parts)<3:
                retstr= invalidParams
            else:
                if parts[2] not in Languages.keys():
                     retstr = invalidParams
                else:
                    tempCypher = decoder.cypher
                    language=parts[2]
                    decoder = Decoder(tempCypher,
                        dictionary=Languages[language]["dictionary"],
                        wordFrequencyFile=Languages[language]["wordFrequencyFile"],
                        LetterFrequencyFile=Languages[language]["LetterFrequencyFile"]
                        )
                    retstr = "{Author}: {output}".format(
                        Author=AuthorName,
                        output="```"+decoder._printStatus()+"```"
                        )
        elif parts[1].upper() == "SOLVELETTER":
            if len(parts)<4:
                retstr= """{Author}: The **SolveLetter** command must have 2 parameters.
1) Cypher Letter to be replaced
2) Clear Text Letter to replace it with
Example:
!SolveLetter j e""".format(
					Author=AuthorName
		            )
            else:
                retstr = "```"+decoder._solveLetter(parts[2],parts[3])+"```"
        elif parts[1].upper() == "APPLYNEWMATCHES":
           retstr = "```"+decoder._applyNewMatches()+"```"
        elif parts[1].upper() == "PRINTSTATUS":
           retstr = "```"+decoder._printStatus()+"```"
        elif parts[1].upper() == "CHECKWORD":
            if len(parts)<3:
                retstr= """{Author}: The **CheckWord** command must have 1 parameter.
It must be the cyphered word to test.
Example:
!CheckWord jxmtz""".format(
					Author=AuthorName
		            )
            else:
                cnt,decryptWord=decoder.checkWord(parts[2])
                retstr = "```{cnt} possibilities for '{cryptWord}'='{decryptWord}':\n{WordList}```".format(
                     cnt=cnt,
                     cryptWord=parts[2],
                     decryptWord=decryptWord,
                     WordList=listWords(decoder.wordList.words)
                )
                
        elif parts[1].upper() in ["HELP"]:
            retstr = '''
My Key words are "!", "/", or "\\"
Load a Language with:```!Language English```
Load a new Cypher with:```!Cypher
Some Cypher Text
Other lines of cypher```
Match a Letter with:```!SolveLetter j e```
Apply solved words' letters with:```!ApplyNewMatches```
To Print the current state of the puzzle:```!PrintStatus```
Check possible clear word matches with currently solved letters with the **CheckWord** command:```!CheckWord jsdek```
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

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
decoder = Decoder('')
language= 'English'

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
