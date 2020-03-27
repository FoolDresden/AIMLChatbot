import os
import datetime
import json
import sys, glob
import aiml
import requests
import sqlite3


from flask import Flask
from flask import request
from flask import redirect

from pytrends.request import TrendReq



def create_app(test_config=None):

    # kernel = aiml.Kernel()
    # kernel.bootstrap(learnFiles="./flaskr/aiml/botty.aiml")
    # kernel.bootstrap(learnFiles="./flaskr/aiml/courses.aiml")
    # kernel.bootstrap(learnFiles="./flaskr/aiml/profs.aiml")
    # kernel.bootstrap(learnFiles="./flaskr/aiml/jobtrends.aiml")


    users = {}

    # pytrends = TrendReq(hl='en-US', tz=360)
    # pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1)
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)


    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    

    from . import db
    db.init_app(app)

    @app.route('/field/<path:courseName>')
    def searchCourse(courseName):
        c = db.get_db()
        response = c.execute('SELECT data FROM field WHERE fieldName = ?', (courseName,)).fetchone()
        # print(response[0])
        if response is not None:
            return response[0]
        else:
            return 'I do not know about that field. Sorry.'

    @app.route('/prof/<path:profName>')
    def searchProf(profName):
        c = db.get_db()
        response = c.execute('SELECT data FROM prof WHERE profName = ?', (profName,)).fetchone()
        # print(response[0])
        if response is not None:
            return response[0]
        else:
            return 'I do not know about that prof. Sorry.'


    @app.route('/chat', methods = ['POST'])
    def postChat():
        
        c = db.get_db()
        json_obj = json.loads(json.dumps(request.form))
        print(json_obj)
        c.execute('INSERT INTO chat VALUES (?,?,?,?)', (str(datetime.datetime.now()),json_obj['postedBy'], 'Botty', json_obj['data']))
        

        msg = json_obj['data'].lower()
        print("msg: ",msg)

        if users.get(json_obj['postedBy'], "NA") == "NA":
            kernel = aiml.Kernel()
            kernel.bootstrap(learnFiles="./flaskr/aiml/botty.aiml")
            kernel.bootstrap(learnFiles="./flaskr/aiml/courses.aiml")
            kernel.bootstrap(learnFiles="./flaskr/aiml/profs.aiml")
            kernel.bootstrap(learnFiles="./flaskr/aiml/jobtrends.aiml")
            users[json_obj['postedBy']] = kernel

        # rsp = getResponse(msg)
        rsp = users[json_obj['postedBy']].respond(msg)
        # print("response: ",rsp)   
        if rsp[0]=='/':
            url = 'http://127.0.0.1:5000'+rsp
            rsp = requests.get(url).text
            # rsp = redirect(rsp)

        print(rsp)
        c.execute('INSERT INTO chat VALUES (?,?,?,?)', (str(datetime.datetime.now()),'Botty', json_obj['postedBy'], rsp))
        c.commit()

        return rsp
        # return 'Written in db'

    @app.route('/chat', methods = ['GET'])
    def getChat():
        c = db.get_db()
        chats = c.execute('SELECT * FROM chat')
        chats_json = json.dumps( [dict(i) for i in chats] )
        chats_obj = json.loads(chats_json)
        # print(chats_obj[0])
        return chats_json

    @app.route('/chat/<path:user>', methods = ['GET'])
    def getUserChat(user):
        # return user
        c = db.get_db()
        chats = c.execute('SELECT * FROM chat WHERE postedBy=? OR postedTo=?', (user,user))
        chats_json = json.dumps( [dict(i) for i in chats] )
        chats_obj = json.loads(chats_json)
        # # print(chats_obj[0])
        return chats_json

    @app.route('/jobTrends/<path:jobName>')
    def getJobTrends(jobName):
        c = db.get_db()
        response = c.execute('SELECT data FROM jobtrends WHERE jobName = ?', (jobName,)).fetchone()
        # print(response[0])
        if response is not None:
            return response[0]
        else:
            return 'I do not know about that job. Sorry.'
    

    return app
