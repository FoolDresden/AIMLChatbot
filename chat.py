#Manages the knowledge base used to think.
import sys, glob
import aiml
import requests
import sqlite3

url = "http://localhost:3000/"
kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="botty.aiml")
kernel.bootstrap(learnFiles="ai.aiml")
# kernel.learn("corpus/bot-startup.xml")
# kernel.respond("LOAD AIML B")

con = sqlite3.connect('data.db')
cursorObj = con.cursor()



while True:
	s = kernel.respond(str(input("> ")))
	if s[0] == '@':
		print(s, "::connect database")
		# r = requests.get(url)
		# data = r.json()
		# print(data)
		continue
	print(s)