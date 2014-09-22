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


