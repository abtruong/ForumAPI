'''
NAME:       Alexander Truong
CWID:       889164513
CLASS:      CPSC 476
PROFESSOR:  Kenytt Averyo
ASSIGNENT:  Project 1
DUE DATE:   Sep. 26, 2018
'''

from flask import Flask, jsonify, request, Response, abort, make_response
from functools import wraps
from flask.cli import AppGroup
from datetime import datetime
import sys, json, sqlite3, click, time, uuid

# Create the flask application
app = Flask(__name__)
app.config['DEBUG'] = True

global database
global cursor

@app.cli.command('init_db')
def init_db():
    ''' Initializing a database via custom terminal command:

    Creates a custom terminal command that initializes a database.db file
    with preset tables, indices, and information inside the tables.

    To use the command, type the following:

        export FLASK_APP=WebAPI.py
        flask init_db

    ** Learned via sqlitetutorials.net **
    '''
    try:
        database = sqlite3.connect('maindb.db')
        with app.open_resource('init.sql', mode='r') as f:
            database.cursor().executescript(f.read())
        database.commit()
        print("INITIALIZED DATABASE")
        print('HELLO')
    except:
        sys.exit("FAILED -- CANNOT INITIALIZE DATABASE")
    finally:
        database.close()
app.cli.add_command(init_db)

def auth_required(func):
    ''' Authenticate user via basic authentication:

    Checks to see if a user is inside the database before allowing POST requests.
    If the user exists within the database and the password provided is correct,
    the authentication will pass and will allow the user to make a post request
    (if all other conditions are met after authentication).

    If the username does not exist in the system or the password provided is 
    incorrect, error 401 (unauthorized) will be raised.

    ** Learned via flask.pocoo.org/snippets/8/ tutorial for wrapping/decorators/basic auth **
    '''
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        cursor = database.cursor()
        cursor.execute('''SELECT EXISTS(SELECT username, password
                                        FROM Users
                                        WHERE username = ? AND password = ?)''',
                        (auth.username, auth.password))
        if cursor.fetchone()[0] == 1:
            global current_user
            current_user = auth.username
            return func(*args, **kwargs)
        return abort(401)
    return decorated

def close_db():
    print('\n\nClosing database\n\n')
    database.close()

def check_forum_exists(cursor, forum_id):
    ''' Check if forum exists:

    Checks the database to see if the specified forum exists.
    '''
    cursor.execute('''SELECT EXISTS(SELECT forum_id
                                    FROM maindb.Forums
                                    WHERE forum_id = ?)''',
                   (forum_id,))
    return cursor.fetchone()[0]

def check_thread_exists(cursor, thread_num, forum_id):
    ''' Check if thread exists:

    Checks the database to see if the specified thread_num exists with the
    correct forum_id assoicated with it.
    '''
    cursor.execute('''SELECT EXISTS(SELECT thread_num
                                    FROM maindb.Threads
                                    WHERE thread_num = ? AND forum_id = ?)''',
                   (thread_num, forum_id))
    return cursor.fetchone()[0]

def get_time():
    ''' Get current time:

    When creating a new forum/thread/post, this will get the current time of when
    the user makes a POST request and stores it into the database.
    '''
    date = datetime.now()
    day = str(date.strftime("%a"))
    day_num = str(date.strftime("%d"))
    month = str(date.strftime("%b"))
    year = str(date.year)
    hour = str(date.strftime("%H"))
    mins = str(date.strftime("%M"))
    secs = str(date.strftime("%S"))
    timestamp = "%s, %s %s %s %s:%s:%s PST" % (day, day_num, month, year, hour, mins, secs)
    return timestamp

def generate_GUID():
    sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
    sqlite3.register_adapter(uuid.UUID, lambda u: buffer(u.bytes_le))
    GUID = uuid.uuid4()
    return GUID

@app.route('/forums/', methods=['GET'])
def list_forums():
    ''' Lists all forums in the database:

    Queries the database and displays all the fourms to the URL:

        localhost:5000/forums/

    If the database has no forums, it will return an empty JSON.
    '''
    no_forums = []
    try:
        cursor.execute("SELECT * FROM maindb.Forums")
        forums = cursor.fetchall()
        list_forums = []
        for row in forums:
            list_forums.append({'id':row[0], 'name':row[1], 'creator':row[2]})
    except:
        return make_response(jsonify(no_forums), 200)
    return make_response(jsonify(list_forums), 200)

@app.route('/forums/', methods=['POST'])
@auth_required              # create_forum() = auth_required(create_forum())
def create_forum():
    ''' Create a forum in the database:

    Inserts a new forum into the database. If all conditions are met, a new entry 
    will be inserted into the Forums table. It will return a 201 HTTP status (Created) 
    JSON response with the new header location:

        localhost:5000/forums/<forum_id>

    If a condition is not met or fails, it will raise a 409 HTTP status (Conflict) response.
    '''
    request_json_data = request.get_json()
    try:
        cursor.execute('''INSERT INTO maindb.Forums (name, creator)
                        VALUES (?, ?)''',
                        (request_json_data['name'], current_user))
        database.commit()
        cursor.execute('''SELECT forum_id
                        FROM maindb.Forums
                        WHERE name = ? AND creator = ?''',
                        (request_json_data['name'], current_user))
        forum = cursor.fetchone()[0]
    except:
        return abort(409)
    response = Response(status=201, mimetype='application/json')
    response.headers['Location'] = "/forums/%s" % str(forum)
    return response

@app.route('/forums/<int:forum_id>/', methods=['GET'])
def list_threads(forum_id):
    ''' List all threads in a specified forum in the database:

    Queries the database and displays all threads of a specified forum to the URL:

        localhost:5000/forums/<forum_id>

    If the specified forum does not exist in the database, a 404 HTTP status code
    (Not Found) will be raised. Otherwise, it will return the JSON of threads with
    a 200 HTTP status code (OK).
    '''
    if check_forum_exists(cursor, forum_id) != 1:
        return abort(404)
    try:
        cursor.execute('''SELECT thread_num, title, creator, thread_time, thread_id, unix_time
                        FROM maindb.Threads
                        WHERE forum_id = ?
                        ORDER BY unix_time DESC''',
                        (forum_id,))
        threads = cursor.fetchall()
        list_threads = []
        for row in threads:
            list_threads.append({'thread_num':row[0], 'title':row[1], 'creator':row[2], 'timestamp':row[3], 'thread_id':row[4]})
    except:
        return abort(404)
    return make_response(jsonify(list_threads), 200)

@app.route('/forums/<int:forum_id>/', methods=['POST'])
@auth_required              # create_forum() = auth_required(create_forum())
def create_thread(forum_id):
    ''' Create a thread of a specified forum in the database:

    Inserts a new thread into the database. If all conditions are met, a new entry 
    will be inserted into the Threads table and is associated with the forum ID it
    was created in. It will return a 201 HTTP status (Created) JSON response with 
    the new header location:

        localhost:5000/forums/<forum_id>/<thread_num>

    If a condition is not met or fails, it will raise a 404 HTTP status (Not Found)
    response.
    '''
    request_json_data = request.get_json()
    if check_forum_exists(cursor, forum_id) != 1:
        return abort(404)
    try:
        timestamp = get_time()
        thread_id = generate_GUID()
        cursor.execute('''INSERT INTO maindb.Threads (forum_id, title, thread_text, creator, thread_time, created_time, unix_time, thread_id)
                        VALUES (?,?,?,?,?,?,?,?)''',
                        (forum_id, request_json_data['title'], request_json_data['text'], current_user, timestamp, timestamp, time.time(), thread_id))
        database.commit()
        cursor.execute('''SELECT thread_num
                        FROM maindb.Threads
                        WHERE forum_id = ? AND title = ? AND thread_text = ? AND creator = ? AND thread_id = ?''',
                        (forum_id, request_json_data['title'], request_json_data['text'], current_user, thread_id))
        thread_num = cursor.fetchone()[0]
    except:
        return abort(404)
    response = Response(status=201, mimetype='application/json')
    response.headers['Location'] = "/forums/%s/%s" % (str(forum_id), str(thread_num))
    return response
    
@app.route('/forums/<int:forum_id>/<int:thread_num>/', methods=['GET'])
def list_posts(forum_id, thread_num):
    ''' List all posts in a specified thread in the database:

    Queries the database and displays all posts of a specified thread to the URL:

        localhost:5000/forums/<forum_id>/<thread_num>

    If the specified thread does not exist in the database, a 404 HTTP status code
    (Not Found) will be raised. Otherwise, it will return the JSON of posts with
    a 200 HTTP status code (OK).
    '''
    if check_thread_exists(cursor, thread_num, forum_id) != 1:
        return abort(404)
    try:
        shard_number = thread_num % 3   # 1%3=1, 2%3=2, 3%3=0, 4%3=1, etc.
        shard = 'posts' + str(shard_number)
        cursor.execute('''SELECT creator, thread_text, created_time, thread_id
                        FROM maindb.Threads
                        WHERE thread_num = ?
                        AND forum_id = ?''',
                        (thread_num, forum_id))
        posts = cursor.fetchone()
        list_posts = [{'author':posts[0], 'text':posts[1], 'timestamp':posts[2], 'thread_id':posts[3]}]
        shard_key = posts[3]
        cursor.execute('''SELECT author, text_post, post_time, thread_id
                        FROM ?.Posts
                        WHERE ?.Posts.thread_id = ?''',
                        (shard, shard, shard_key))
        posts = cursor.fetchall()
        for row in posts:
            list_posts.append({'author':row[0], 'text':row[1], 'timestamp':row[2], 'thread_id':row[3]})
    except:
        return abort(404)
    return make_response(jsonify(list_posts), 200)

@app.route('/forums/<int:forum_id>/<int:thread_num>/', methods=['POST'])
@auth_required              # create_forum() = auth_required(create_forum())
def create_post(forum_id, thread_num):
    ''' Create a post in the database:

    Inserts a new post into the database. If all conditions are met, a new entry 
    will be inserted into the Posts table. It will return a 201 HTTP status (Created) 
    JSON response.

    If a condition is not met or fails, it will raise a 404 HTTP status (Not Found)
    response.
    '''
    request_json_data = request.get_json()
    if check_thread_exists(cursor, thread_num, forum_id) != 1:
        return abort(404)
    try:
        shard_number = thread_num % 3   # 1%3=1, 2%3=2, 3%3=0, 4%3=1, etc.
        shard = 'posts' + str(shard_number)
        timestamp = get_time()
        cursor.execute('''SELECT thread_id
                        FROM maindb.Threads
                        WHERE thread_num = ?''',
                        (thread_num,))
        shard_key = cursor.fetchone()[0]
        cursor.execute('''INSERT INTO ?.Posts (thread_id, text_post, author, post_time)
                        VALUES(?,?,?,?,?)''',
                        (shard, shard_key, request_json_data['text'], current_user, timestamp))
        database.commit()
        cursor.execute('''UPDATE maindb.Threads
                        SET thread_time = ?, unix_time = ?
                        WHERE forum_id = ? AND thread_num = ?''',
                        (timestamp, time.time(), forum_id, thread_num))
        database.commit()
    except:
        return abort(404)
    return Response(status=201, mimetype='application/json')
    
@app.route('/users/', methods=['POST'])
def create_user():
    ''' Creates a new user in the database:

    Adds a new user to the Users table in the database. Once the username and password
    are registered into the database, that user can now use POST methods in other parts
    of the forum (given his credentials are specified properly during authentication).

    If the username already exists in the database, a 409 HTTP status code (Conflict)
    will be raised. Otherwise, a JSON 201 HTTP status code (Created) will be returned.
    '''
    request_json_data = request.get_json()
    try:
        cursor.execute('''INSERT INTO Users (username, password)
                        VALUES (?, ?)''',
                        (request_json_data['username'], request_json_data['password']))
        database.commit()
    except:
        return abort(409)
    return Response(status=201, mimetype='application/json')

@app.route('/users/', methods=['PUT'])
@auth_required              # create_forum() = auth_required(create_forum())
def change_user_pw():
    ''' Change username's password:

    Allows the currently logged-in user to change his or her password. If the user logged
    in attempts to change the user's password and the request payload's username is the same
    as the user's username, the password will update in the database and return a 200 HTTP
    status code (OK). If the user logged-in attempts to change the password of another user,
    a 409 HTTP status code (Conflict) will be raised. Also, if the user logged-in attempts to
    change the password of a user not stored in the database, a 404 HTTP status code (Not Found)
    will be raised.
    '''
    request_json_data = request.get_json()
    cursor.execute('''SELECT EXISTS(SELECT username
                                    FROM Users
                                    WHERE username = ?)''',
                    (request_json_data['username'], ))
    match = cursor.fetchone()[0]
    if match == 1 and str(current_user).lower() == str(request_json_data['username']).lower():
        cursor.execute('''UPDATE Users
                        SET password = ?
                        WHERE username = ?''',
                        (request_json_data['password'], request_json_data['username']))
        database.commit()
        return Response(status=200, mimetype='application/json')
    elif match == 1 and str(current_user).lower() != str(request_json_data['username']).lower():
        return abort(409)
    else:
        return abort(404)
    
if __name__ == '__main__':
    try:
        database = sqlite3.connect('maindb.db')
        print("SUCCESS -- CONNECTION ESTABLISHED")
        cursor = database.cursor()
        app.run()
    except:
        sys.exit("FAILED -- NO DATABASE CONNECTION ESTABLISHED . . . EXITING")
    finally:
        database.close()
        print('\n\nDatabase Connection Terminated\n\n')