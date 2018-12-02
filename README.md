# Forum API

Welcome to the Forum API! Here, you can find three different implementations of a WebAPI.py that handle the back-end of a website. Each of these three implementations allow storing and querying information from a database. The three different implementations are:

* Relational Database
* Sharded Database
* NoSQL Database

Every Web API is written in Python3.

---

## WebAPI Folder: Relational Database

An implementation of a relational database server involving only one database file. All data is stored into and queried from a local .db database file "maindb.db" utilizing sqlite3.

---

## Sharding Folder: Sharded Database

Derivative of the WebAPI folder that shards the relational database "maindb.db" into four separate .db database files:

* maindb.db
* shard_0.db
* shard_1.db
* shard_2.db

The sharded databases contains a sharded portion of the "posts" table for the Web API with the rest of the data stored in the "maindb.db" file. All of these .db databases are also local. Utilizes sqlite3.

---

## ScyllaDB Folder: NoSQL Database

Derivative of the WebAPI folder that no longer relies on sqlite3 and relational databases, but now relies on NoSQL, a non-relational database schema. All sqlite3 queries have been ported to CQL, a NoSQL querying language that is based on SQL without certain functions it provides, such as:

* JOINS
* OR or NOT
* Updates based only on PRIMARY KEY or an indexed key
* And more...

Database files are also no longer local. This application utilizes Docker to run a separate instance of a server on a local machine, in this case, ScyllaDB.

---

## NOTE:

All commands provided in each of the three methods are intended for a Debian-based Linux Operating system, such as:

* Linux Mint
* Ubuntu
* SparkyLinux
* Rapsbian
* And more...

The Web APIs utilize one or more of the following dependencies:

* Python3
* Sqlite3
* Flask
* Docker
* Cassandra DataStax

---

##### Acknowledgement:

_All instructions provided in all folders were taught and provided by [Kenytt Avery](https://twitter.com/ProfAvery)._


