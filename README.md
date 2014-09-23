#Schemaspy


Schemaspy jar and datbase jdbc drivers and a python wrapper to schemaspy, named schemaspy.py
This package provides easy installation of schemaspy on Unix-like platforms.

For thoses who doesn't know what is it:
SchemaSpy analyzes database metadata to reverse engineer dynamic Entity Relationship (ER) diagrams (LGPL, Database, Front-Ends, MySQL, SQLite).

See also: http://schemaspy.sourceforge.net/

#Install
```
sudo su
cd /opt
git clone https://github.com/wolfprogrammer/schemaspybin
```
#Usage

##Schemaspy

Schemaspy python command line wrapper.

```
$ /opt/schemaspy.py 

usage: schemaspy.py [-h] [--database DATABASE] [--output OUTPUT] [--path PATH]
                    [--supported]

Schemaspy Python Wrapper

optional arguments:
  -h, --help            show this help message and exit
  --database DATABASE, -d DATABASE
                        Database Type
  --output OUTPUT, -o OUTPUT
                        Output directory
  --path PATH, -p PATH  Database path
  --supported           Print all supported databases

Example:

./schemaspy.py -p [dbtype]://[user][:password]@hostname[:port]/database

SQLite Schema
./schemaspy.py -p sqlite:///home/tux/.zotserver/zotero.sqlite  -o zotero3

Postgres SQL Schema
./schemaspy.py -p postgresql://postgres:postgres@localhost/biblivre3 -o biblivre3


```

## SQL Tables
sqltables.py is a SQLAlchemy-based database analyser.


Features:

* Explore datbase with Ipython
* Generate graphical schema
* Show tables and columns
* Generate database python-SQLAlchemy table code.
* Examples provided.

```
$ /opt/schemaspy/sqltables.py 
usage: /opt/schemaspy/sqltables.py [-h] [--database DATABASE] [--path PATH]
                                   [--tables] [--table TABLE] [--explore]
                                   [--schema]

SlQL Table constructor

optional arguments:
  -h, --help            show this help message and exit
  --database DATABASE, -d DATABASE
                        Database type
  --path PATH, -p PATH  Database URL
  --tables, -ts         Print database tables
  --table TABLE, -t TABLE
                        Print table columns
  --explore, -e         Interactively explore the database
  --schema, -s          Create schema

Create python SQL Alchemy tables of SQL databases

Example:

./sqltables.py -d sqlite -p /home/tux/.zotserver/zotero.sqlite  > tables.py
./sqltables.py  -d postgresql -p postgres:postgres@localhost/biblivre3 > tables.py

```
