# Welcome to Botty the Chatbot!

Hi. Welcome and please do say hi to **Botty** as he is the resident chatbot and he is who you shall be setting up on a **Flask** server

Please follow the following instructions in order to deploy the flask app (if it does not work, feel free to drop me a call) :

# Setting the environment
1. Clone the repo
2. Setup the virtual environment 
	```pipenv install```
3. Setup the flask server
	```export FLASK_APP=flaskr```
	```export FLASK_ENV=development```
	```flask run```

# Calling the API	
The API has one main endpoint ```/chat``` and will be used to interact with Botty
1. GET ```/chat``` allows one to see all the chats 
2. POST ```/chat/<chat here>``` allows one to post to the server and receive a response

