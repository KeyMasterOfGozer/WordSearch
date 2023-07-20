import json
import sys
import logging
import discord
from decoder import Decoder

logger = logging.getLogger(__name__)
stdout = logging.StreamHandler(stream=sys.stdout)
fmt = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)
stdout.setFormatter(fmt)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

Verbosity = 0
ConfigFile = 'discord.json'
# Read in Security File
with open(ConfigFile,"r") as f:
	Config = json.load(f)

TOKEN = Config["Tokens"]["11House-Crypt"]["Token"]
Languages = Config["Languages"]
logger.debug(Languages)
                
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
    logger.debug(input)
    logger.debug(parts)

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
            logger.debug(parts)
        else:
            logger.debug("Not a command")
            return None

    try:
        logger.debug("Command: "+parts[1].upper())
        if parts[1].upper() == "NEWCYPHER":
            cypher = ' '.join(parts[2:])
            logger.info("New Cypher:\n"+cypher)
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
            logger.debug(retstr)
        elif parts[1].upper() == "LANGUAGE":
            logger.debug("Language Command")
            invalidParams="""{Author}: The **Language** command must have 1 parameter.
It must be one of {lang}.
Example:
!language ThornedEnglish""".format(
					Author=author,
                    lang=json.dumps(list(Languages.keys()))
		            )
            if len(parts)<3:
                logger.debug("Not Enough Language Parameters")
                retstr= invalidParams
            else:
                if parts[2] not in Languages.keys():
                    logger.debug("Not a valid Language [{lang}].".format(lang=parts[2]))
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
                    logger.info(retstr)
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
                logger.info("SolveLetter [{old}] [{new}]".format(old=parts[2],new=parts[3]))
                retstr = "```"+decoder._solveLetter(parts[2],parts[3])+"```"
        elif parts[1].upper() == "APPLYNEWMATCHES":
           logger.info("ApplyNewMatches")
           retstr = "```"+decoder._applyNewMatches()+"```"
        elif parts[1].upper() == "PRINTSTATUS":
           logger.info("PrintStatus")
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
                logger.info("CheckWord [{word}]".format(word=parts[2]))
                cnt,decryptWord=decoder.checkWord(parts[2])
                retstr = "```{cnt} possibilities for '{cryptWord}'='{decryptWord}':\n{WordList}```".format(
                     cnt=cnt,
                     cryptWord=parts[2],
                     decryptWord=decryptWord,
                     WordList=listWords(decoder.wordList.words)
                )
                
        elif parts[1].upper() in ["LOGLEVEL"]:
            if parts[2].upper() == "DEBUG":
                logger.setLevel(logging.DEBUG)
            elif parts[2].upper() == "INFO":
                logger.setLevel(logging.INFO)
            retstr= "LogLevel set to "+parts[2].upper()
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
