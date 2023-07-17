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
			decoder = Decoder(cypher)
			#give user message so he knows it's saved
			retstr = "{Author} posed a new Cypher:\n{cypher}".format(
				Author=author,
		        cypher=decoder.cypher
		        )
		elif parts[1].upper() == "ECHO":
			retstr = "{Author}: {rollreturn}".format(Author=AuthorName,rollreturn=replaceVars(" ".join(parts[2:]),Users[author]['vars']))
		elif parts[1].upper() == "USE":
			Users=refreshDataFile(author)
			# run the macro
			retstr = parse(Users[author]['macros'][parts[2]],author,MultiLine)
		elif parts[1].upper() == "LIST":
			Users=refreshDataFile(author)
			# build list of stored commands
			retstr = "\n{Author}'s Macros:".format(Author=author)
			for key,value in Users[author]['macros'].items():
				retstr += "\n{MacroName}:\t{MacroText}".format(MacroName=key,MacroText=value)
			retstr += "\n{Author}'s Variables:".format(Author=author)
			for key,value in Users[author]['vars'].items():
				retstr += "\n{MacroName}:\t{MacroText}".format(MacroName=key,MacroText=value)
		elif parts[1].upper() == "LOAD":
			Users=refreshDataFile(author)
			# build list of stored commands
			if len(parts) > 2 and parts[2].lstrip()[0] == "{":
				Users[author]['macros'].update(json.loads(" ".join(parts[2:])))
				retstr = "\n{Author} added or updated Macros".format(Author=author)
				# save to DB file for next time
				with open(UserFile,"w") as f:
					f.write(json.dumps(Users,indent=2))
			else:
				retstr = "\n{Author}'s Macro string was not recognized JSON:".format(Author=author)
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
