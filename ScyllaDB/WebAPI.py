'''
NAMES:      Alexander Truong (889164513)
CLASS:      CPSC 476
PROFESSOR:  Kenytt Avery
ASSIGNENT:  Project 3
DUE DATE:   Dec. 05, 2018
'''

from flask import Flask, jsonify, request, Response, abort, make_response
from functools import wraps
from flask.cli import AppGroup
from datetime import datetime
from cassandra.cluster import Cluster
import sys, json, click, time, uuid

# Create the flask application
app = Flask(__name__)
app.config['DEBUG'] = True



############################
#    CONNECT TO CLUSTER    #
############################

def cluster_connection():
    cluster = Cluster(['172.17.0.2'])
    return cluster

def keyspace_connection():
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('forum')
    return session



###########################
#        TIMESTAMP        #
###########################

def get_time():
    ''' 
    Get current time:

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



#############################
#    INITIALIZE DATABASE    #
#############################

@app.cli.command('init_db')
def init_db():
    ''' 
    Initializing a schema via custom terminal command:

    Creates a custom terminal command that initializes a schema
    with preset tables, indices, and information inside the tables,
    all located on ScyllaDB running on Docker.
    '''
    try:
        cluster = cluster_connection()
        session = cluster.connect()
        with app.open_resource('init.cql', mode='r') as f:
            contents = f.read()
            queries = contents.split(";")

            for index, query in enumerate(queries):
                if index != len(queries)-1:
                    session.execute(query)
                    
    except:
        sys.exit("Error -- ScyllaDB Schema Not Initialized")
    finally:
        print("ScyllaDB Schema Initialized")
        session.shutdown()
app.cli.add_command(init_db)



##########################
#       BASIC AUTH       #
##########################

def auth_required(func):
    '''
    Authenticate user via basic authentication:

    Checks to see if a user is inside the database before allowing POST requests.
    If the user exists within the cluster and the password provided is correct,
    the authentication will pass and will allow the user to make a post request
    (if all other conditions are met after authentication).

    If the username does not exist in the system or the password provided is 
    incorrect, error 401 (unauthorized) will be raised.
    '''
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        session = keyspace_connection()

        if check_user_CQL(session, auth.username, auth.password) == True:
            global current_user
            current_user = auth.username
            return func(*args, **kwargs)
        return abort(401)
    return decorated



##########################
#         FORUMS         #
##########################

# GET REQUEST
@app.route('/forums/', methods=['GET'])
def list_forums():
    ''' 
    Lists all forums in the database:

    Queries the cluster and displays all the fourms to the URL:
        localhost:5000/forums/
    If the cluster has no forums, it will return an empty JSON.
    '''
    try:
        no_forums = []
        session = keyspace_connection()

        rows = select_forums_CQL(session)
        query_forums = []

        for id, name, creator in rows:
            query_forums.append({'id':id, 'name':name, 'creator':creator})
        list_forums = sorted(query_forums, key=lambda k: k['id'], reverse=False)
    except:
        return make_response(jsonify(no_forums), 200)
    finally:
        session.shutdown()
    return make_response(jsonify(list_forums), 200)

# POST REQUEST
@app.route('/forums/', methods=['POST'])
@auth_required              # create_forum() = auth_required(create_forum())
def create_forum():
    ''' 
    Create a forum in the database:

    Inserts a new forum into the database. If all conditions are met, a new entry 
    will be inserted into the Forums table. It will return a 201 HTTP status (Created) 
    JSON response with the new header location:
        localhost:5000/forums/<forum_id>
    If a condition is not met or fails, it will raise a 409 HTTP status (Conflict) response.
    '''
    try:
        session = keyspace_connection()
        request_json_data = request.get_json()
        forum_id = get_num_rows_CQL(session, 'forums', 0, 0)
        insert_forum_CQL(session, forum_id, request_json_data['name'], current_user)
    except:
        return abort(409)
    finally:
        session.shutdown()
    response = Response(status=201, mimetype='application/json')
    response.headers['Location'] = "/forums/%s" % str(forum_id)
    return response



###########################
#         THREADS         #
###########################

# GET REQUEST
@app.route('/forums/<int:forum_id>/', methods=['GET'])
def list_threads(forum_id):
    ''' 
    List all threads in a specified forum in the database:

    Queries the database and displays all threads of a specified forum to the URL:
        localhost:5000/forums/<forum_id>
    If the specified forum does not exist in the database, a 404 HTTP status code
    (Not Found) will be raised. Otherwise, it will return the JSON of threads with
    a 200 HTTP status code (OK).
    '''
    try:
        session = keyspace_connection()

        if check_forum_exists_CQL(session, forum_id) != True:
            return abort(404)

        rows = select_threads_CQL(session)
        query_threads = []

        for forum_id_check, thread_id, topic, creator, time_recent, time_created, epoch in rows:
            if forum_id == forum_id_check:
                query_threads.append({
                    'thread_id' : thread_id, 
                    'title' : topic, 
                    'creator' : creator, 
                    'timestamp' : time_recent, 
                    'time_created' : time_created,
                    'time_epoch' : epoch
                })
        list_threads = sorted(query_threads, key=lambda k: k['time_epoch'], reverse=True)
    except:
        return abort(404)
    finally:
        session.shutdown()
    return make_response(jsonify(list_threads), 200)

# POST REQUEST
@app.route('/forums/<int:forum_id>/', methods=['POST'])
@auth_required              # create_thread() = auth_required(create_thread())
def create_thread(forum_id):
    ''' 
    Create a thread of a specified forum in the database:

    Inserts a new thread into the database. If all conditions are met, a new entry 
    will be inserted into the Threads table and is associated with the forum ID it
    was created in. It will return a 201 HTTP status (Created) JSON response with 
    the new header location:
        localhost:5000/forums/<forum_id>/<thread_num>
    If a condition is not met or fails, it will raise a 404 HTTP status (Not Found)
    response.
    '''
    try:
        session = keyspace_connection()
        request_json_data = request.get_json()
    
        if check_forum_exists_CQL(session, forum_id) != True:
            return abort(404)
    
        timestamp = get_time()
        thread_id = get_num_rows_CQL(session, 'threads', forum_id, 0)
        insert_thread_CQL(session, forum_id, thread_id, request_json_data['title'], current_user, timestamp, timestamp)
        insert_post_CQL(session, forum_id, thread_id, 1, current_user, request_json_data['text'], timestamp)
    except:
        return abort(404)
    finally:
        session.shutdown()
    response = Response(status=201, mimetype='application/json')
    response.headers['Location'] = "/forums/%s/%s" % (str(forum_id), str(thread_id))
    return response



###########################
#          POSTS          #
###########################

# GET REQUEST
@app.route('/forums/<int:forum_id>/<int:thread_id>/', methods=['GET'])
def list_posts(forum_id, thread_id):
    ''' 
    List all posts in a specified thread in the database:

    Queries the database and displays all posts of a specified thread to the URL:
        localhost:5000/forums/<forum_id>/<thread_num>
    If the specified thread does not exist in the database, a 404 HTTP status code
    (Not Found) will be raised. Otherwise, it will return the JSON of posts with
    a 200 HTTP status code (OK).
    '''

    try:
        session = keyspace_connection()

        if check_thread_exists_CQL(session, forum_id, thread_id) != True:
            return abort(404)

        rows = select_posts_CQL(session)
        query_posts = []

        for forum_id_check, thread_id_check, post_id, post_creator, post_text, post_time in rows:
            if forum_id_check == forum_id and thread_id_check == thread_id:
                query_posts.append({
                    'post_id' : post_id,
                    'author' : post_creator,
                    'text' : post_text,
                    'post_time' : post_time
                })
        list_posts = sorted(query_posts, key=lambda k: k['post_id'], reverse=False)
    except:
        return abort(404)
    finally:
        session.shutdown()
    return make_response(jsonify(list_posts), 200)

# POST REQUEST
@app.route('/forums/<int:forum_id>/<int:thread_id>/', methods=['POST'])
@auth_required              # create_forum() = auth_required(create_forum())
def create_post(forum_id, thread_id):
    ''' 
    Create a post in the database:

    Inserts a new post into the database. If all conditions are met, a new entry 
    will be inserted into the Posts table. It will return a 201 HTTP status (Created) 
    JSON response.

    If a condition is not met or fails, it will raise a 404 HTTP status (Not Found)
    response.
    '''
    try:
        session = keyspace_connection()
        request_json_data = request.get_json()

        if check_thread_exists_CQL(session, forum_id, thread_id) != True:
            return abort(404)

        timestamp = get_time()
        post_id = get_num_rows_CQL(session, 'posts', forum_id, thread_id)
        insert_post_CQL(session, forum_id, thread_id, post_id, current_user, request_json_data['text'], timestamp)
        
        rows = get_unique_id_of_thread_CQL(session, forum_id, thread_id)
        for uuid, forum_id_check, thread_id_check in rows:
            if forum_id_check == forum_id and thread_id_check == thread_id:
                unique_id = uuid

        update_most_recent_thread_time_CQL(session, unique_id, timestamp)
    except:
        return abort(404)
    finally:
        session.shutdown()
    return Response(status=201, mimetype='application/json')



###########################
#          USERS          #
###########################

# POST REQUEST
@app.route('/users/', methods=['POST'])
def create_user():
    ''' 
    Creates a new user in the database:

    Adds a new user to the Users table in the database. Once the username and password
    are registered into the database, that user can now use POST methods in other parts
    of the forum (given his credentials are specified properly during authentication).

    If the username already exists in the database, a 409 HTTP status code (Conflict)
    will be raised. Otherwise, a JSON 201 HTTP status code (Created) will be returned.
    '''
    try:
        session = keyspace_connection()
        request_json_data = request.get_json()

        if check_username_exists_CQL(session, request_json_data['username']) == False:
            insert_user_CQL(session, request_json_data['username'], request_json_data['password'])
        else:
            return abort(409)
    except:
        return abort(409)
    finally:
        session.shutdown()
    return Response(status=201, mimetype='application/json')

# PUT REQUEST
@app.route('/users/', methods=['PUT'])
@auth_required              # create_forum() = auth_required(create_forum())
def change_user_pw():
    ''' 
    Change username's password:

    Allows the currently logged-in user to change his or her password. If the user logged
    in attempts to change the user's password and the request payload's username is the same
    as the user's username, the password will update in the database and return a 200 HTTP
    status code (OK). If the user logged-in attempts to change the password of another user,
    a 409 HTTP status code (Conflict) will be raised. Also, if the user logged-in attempts to
    change the password of a user not stored in the database, a 404 HTTP status code (Not Found)
    will be raised.
    '''
    try:
        session = keyspace_connection()
        request_json_data = request.get_json()
    except:
        return abort(404)

    if current_user.upper() != request_json_data['username'].upper():
        return abort(409)

    if check_username_exists_CQL(session, request_json_data['username']) != True: 
        return abort(404)

    exact_username = get_username_exact_CQL(session, current_user)
    update_user_password(session, exact_username, request_json_data['password'])

    session.shutdown()

    return Response(status=200, mimetype='application/json')
    


###########################
#         QUERIES         #
###########################

# Check user exists for basic authentication
def check_user_CQL(session, auth_username, auth_password):
    rows = session.execute(
        '''
        SELECT username, password
        FROM users
        '''
    )
    for username, password in rows:
        if username.upper() == auth_username.upper() and password == auth_password:
            return True
    return False

# Check if forum exists in the table 'entity_tables'
def check_forum_exists_CQL(session, forum_id_check):
    rows = session.execute(
        '''
        SELECT forum_id
        FROM entity_tables
        WHERE entity_name = %s
        ''', ('forums',)
    )
    for row in rows:
        if str(row.forum_id) == str(forum_id_check):
            return True
    return False

# Check if thread exists in the table 'entity_tables'
def check_thread_exists_CQL(session, forum_id_check, thread_id_check):
    rows = session.execute(
        '''
        SELECT forum_id, thread_id
        FROM entity_tables
        WHERE entity_name = %s
        ''', ('threads',)
    )
    for forum_id, thread_id in rows:
        if str(forum_id) == str(forum_id_check) and str(thread_id) == str(thread_id_check):
            return True
    return False

# Check if username exists in the table 'users'
def check_username_exists_CQL(session, username):
    rows = session.execute(
        '''
        SELECT username
        FROM users
        '''
    )
    for row in rows:
        if (row.username).upper() == username.upper():
            return True
    return False

# Get exact username in the table 'users' for case-sensitivity
def get_username_exact_CQL(session, username):
    rows = session.execute(
        '''
        SELECT username
        FROM users
        '''
    )
    for row in rows:
        if (row.username).upper() == username.upper():
            return row.username
    return ""

# Get total count of rows + 1 for new id
def get_num_rows_CQL(session, entity_name, forum_id, thread_id):
    rows = session.execute(
        '''
        SELECT forum_id, thread_id
        FROM entity_tables
        WHERE entity_name = %s
        ''', (entity_name,)
    )
    
    count = 1

    if entity_name == 'forum':
        for _ in rows:
            count = count + 1
    elif entity_name == 'threads':
        for forum_id_check, _ in rows:
            if forum_id_check == forum_id:
                count = count + 1
    elif entity_name == 'posts':
        for forum_id_check, thread_id_check in rows:
            if forum_id_check == forum_id and thread_id_check == thread_id:
                count = count + 1

    return count

# Get unique_id from 'entity_tables' where 'entity_name' is 'threads'
def get_unique_id_of_thread_CQL(session, forum_id, thread_id):
    rows = session.execute(
        '''
        SELECT unique_id, forum_id, thread_id
        FROM entity_tables
        WHERE entity_name = %s
        ''', ('threads',)
    )
    return rows

# Select all forums
def select_forums_CQL(session):
    rows = session.execute(
        '''
        SELECT forum_id, forum_topic, forum_creator
        FROM entity_tables
        WHERE entity_name = %s
        ''', ('forums',)
    )
    return rows

# Select all threads
def select_threads_CQL(session):
    rows = session.execute(
        '''
        SELECT forum_id, thread_id, thread_topic, thread_creator, thread_time, thread_created, thread_epoch
        FROM entity_tables
        WHERE entity_name = %s
        ''', ('threads',)
    )
    return rows

# Select all posts
def select_posts_CQL(session):
    rows = session.execute(
        '''
        SELECT forum_id, thread_id, post_id, post_creator, post_text, post_time
        FROM entity_tables
        WHERE entity_name = %s
        ''', ('posts',)
    )
    return rows

# Insert into forums
def insert_forum_CQL(session, forum_id, name, creator):
    session.execute(
        '''
        INSERT INTO entity_tables (entity_name, unique_id, forum_id, forum_topic, forum_creator)
        VALUES (%s, uuid(), %s, %s, %s)
        ''', ('forums', forum_id, name, creator)
    )

# Insert into threads
def insert_thread_CQL(session, forum_id, thread_id, name, creator, time_recent, time_created):
    session.execute(
        '''
        INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, thread_topic, thread_creator, thread_time, thread_created, thread_epoch)
        VALUES (%s, uuid(), %s, %s, %s, %s, %s, %s, %s)
        ''', ('threads', forum_id, thread_id, name, creator, time_recent, time_created, int(time.time() - 1500000000))
    )

# Insert into posts
def insert_post_CQL(session, forum_id, thread_id, post_id, post_creator, post_text, post_time):
    session.execute(
        '''
        INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time)
        VALUES (%s, uuid(), %s, %s, %s, %s, %s, %s)
        ''', ('posts', forum_id, thread_id, post_id, post_creator, post_text, post_time)
    )

# Insert into users
def insert_user_CQL(session, username, password):
    session.execute(
        '''
        INSERT INTO users (username, password)
        VALUES (%s, %s)
        ''', (username, password)
    )

# Update user password
def update_user_password(session, username, new_password):
    session.execute(
        '''
        UPDATE users
        SET password = %s
        WHERE username = %s
        ''', (new_password, username)
    )

# Update the most recent thread time after a post has been made in that thread
def update_most_recent_thread_time_CQL(session, unique_id, thread_time):
    session.execute(
        '''
        UPDATE entity_tables
        SET thread_time = %s, thread_epoch = %s
        WHERE unique_id = %s
        ''', (thread_time, int(time.time() - 1500000000), unique_id)
    )


if __name__ == '__main__':
    app.run()