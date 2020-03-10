import os
import datetime
import json
from flask import Flask
from flask import request


def create_app(test_config=None):
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
            return 'I don\'t think I can help you'

    @app.route('/prof/<path:profName>')
    def searchProf(profName):
        c = db.get_db()
        response = c.execute('SELECT data FROM prof WHERE profName = ?', (profName,)).fetchone()
        # print(response[0])
        if response is not None:
            return response[0]
        else:
            return 'I don\'t think I can help you'


    @app.route('/chat', methods = ['POST'])
    def postChat():
        c = db.get_db()
        print(request.form)
        print(type(request.form))
        print(type(json.dumps(request.form)))
        json_obj = json.loads(json.dumps(request.form))
        print(type(json_obj))
        print(json_obj['postedBy'])
        c.execute('INSERT INTO chat VALUES (?,?,?)', (str(datetime.datetime.now()),str(json_obj['postedBy']), str(json_obj['data'])))
        
        c.commit()
        # return 'Written in db'

    @app.route('/chat', methods = ['GET'])
    def getChat():
        c = db.get_db()
        chats = c.execute('SELECT * FROM chat')
        chats_json = json.dumps( [dict(i) for i in chats] )
        chats_obj = json.loads(chats_json)
        # print(chats_obj[0])
        return chats_json

    return app