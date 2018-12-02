# NoSQL Implementation of WebAPI Using Cassandra/ScyllaDB

A web back-end application for querying and storing information of a NoSQL database to a forum-based application using JSON. This application runs on Python using the Flask module, Docker, and Cassandra/ScyllaDB for the databases using CQL. An initial schema is provided with test data. RESTful endpoints are used to handle GET, POST, and PUT methods running this python application. 

This project is a derivative of the WebAPI folder; however, instead of a relational database, it has been ported over to a NoSQL database, specifically ScyllaDB. Instead of having to use SQL statements and a relational database schema, ScyllaDB uses a NoSQL schema where most information is stored in one big table (in this case, "entity_tables") using a keyspace. All statements that were writtein via SQL or sqlite3 have been changed to Cassandra's version: CQL.

The keyspaces are names within a cluster that signify which "database" we are connecting to. The clusters are important for a NoSQL database as it allows replication of all data to other clusters of ScyllaDB.

Docker is a necessity for this project. It allows the user to run a separate instance of a server on a local machine for development purposes. 

---

## Prerequesite Packages

Be sure to have the following latest version of the packages installed:
* Flask
* Docker
* Pyhton3

You may also want to use a program to make HTTP requests to test different protocols, such as:
* Curl
* Postman

Have the DataStax Python Cassandra Driver installed:

```
$ sudo apt install --yes python3-cassandra
```

---

## Getting Started with Docker

First and foremost, ensure you have Docker installed on your local machine to be able to run ScyllaDB:

```
$ sudo apt install --yes docker.io
$ sudo usermod -aG docker $USER
```

After docker successfully installs, start a single instance of ScyllaDB:

```
$ docker run --name scylla -d scylladb/scylla --smp 1 --memory 1G --overprovisioned 1 --developer-mode 1 --experimental 1
```

To make sure Docker began the ScyllaDB process properly:

```
$ docker exec -it scylla nodetool status
```

---

## Getting Started with the WebAPI

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

---

## Using the API

To test GET requests, connect to your localhost machine. For example, to test all the posts within a thread of a forum, connect to:

```
http://localhost:5000/forums/1/1/
```

This will request the RESTful endpoint with a GET request and query the database for all posts within the first thread of the first forum.

---

## Managing ScyllaDB with Docker and CQLSH

With Docker installed and the instance of ScyllaDB running, you can execute CQL commands using:

```
$ docker exec -it scylla cqlsh
```

If you had chosen a different name when running a new instance of ScyllaDB, be sure to replace "scylla" with the name you chose.

To start or stop ScyllaDB:

```
$ docker (start|stop) scylla
```

To remove ScyllaDB and start over:

```
$ docker rm -f scylla && docker rmi scylladb/scylla
```
