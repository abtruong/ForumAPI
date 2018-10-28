# WebAPI

A web back-end application for querying and storing information from a database to a forum-based application using JSON. This application runs on Python using the Flask module and SQlite3 for the database. An initial schema is provided with test data. RESTful endpoints are used to handle GET, POST, and PUT methods running this python application.

## Prerequesite Packages

Be sure to have the following latest version of the packages installed:
* Flask
* SQlite3
* Pyhton3

You may also want to use a program to make HTTP requests to test different protocols, such as:
* Curl
* Postman

## Getting Started

To initialze the WebAPI.py database, perform the following code to add a custom command:

```
$ export FLASK_APP=WebAPI.py
```

Now, we can use the custom command within this API to initialize the database.db itself:

```
$ flask init_db
```

Finally, run the API to begin the Python Flask server for testing:

```
$ python3 WebAPI.py
```

## Using the API

To test GET requests, connect to your localhost machine. For example, to test all the posts within a thread of a forum, connect to:

```
http://localhost:5000/forums/1/1/
```

This will request the RESTful endpoint with a GET request and query the database for all posts within the first thread of the first forum.
