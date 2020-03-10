#Manages the knowledge base used to think.
import sys, glob
import aiml
import requests
import sqlite3

kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="./aiml/botty.aiml")
kernel.bootstrap(learnFiles="./aiml/courses.aiml")
kernel.bootstrap(learnFiles="./aiml/profs.aiml")
# kernel.learn("corpus/bot-startup.xml")
# kernel.respond("LOAD AIML B")


while True:
	s = kernel.respond(str(input("> ")))
	if s[0] == '/':
		s = s.lower()
		url = 'http://127.0.0.1:5000'+s
		print("url: ",url)
		s = requests.get(url).text
		# print(s)
	print(s)