#!/usr/bin/env python2
#
# Schemaspy python wrapper
#
#

import os
import sys
import time
import shutil

INSTALL = "/opt"

# this script absolute path
this = os.path.abspath(__file__)
# this script directory
thisdir = os.path.dirname(this)

HOME = os.path.expanduser("~")
USERNAME = os.path.basename(HOME)

listdir = os.listdir
join = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
basename = os.path.basename
isfile = os.path.isfile
isdir = os.path.isdir
exists = os.path.exists
chdir = os.chdir
cwd = os.getcwd
pwd = os.getcwd()
copy = shutil.copy
sleep = time.sleep
exit = sys.exit

schemadir = join(INSTALL, "schemaspy")

schemaspy = join(schemadir, "schemaSpy_5.0.0.jar")
sqlite_jdbc = join(schemadir, "sqlite.jar")

#postgres_jdbc = join(schemadir, "postgresql-8.0-312.jdbc3.jar")

postgres_jdbc = join(schemadir, "postgresql-9.1-902.jdbc4.jar")



options =  "-hq -norows"
# =============== COMMAND LINE PARSER =======================#

import argparse
import sys

desc = "Schemaspy Python Wrapper"
parser = argparse.ArgumentParser(prog='schemaspy.py', description=desc)

parser.add_argument("--database", "-d", help="Database Type")
parser.add_argument("--output", "-o", help="Output directory")
parser.add_argument("--path", "-p", help="Database path")
parser.add_argument("--supported", action="store_true", help="Print all supported databases")


args = parser.parse_args()

help = \
"""
Example:

./schemaspy.py -p [dbtype]://[user][:password]@hostname[:port]/database

SQLite Schema
./schemaspy.py -p sqlite:///home/tux/.zotserver/zotero.sqlite  -o zotero3

Postgres SQL Schema
./schemaspy.py -p postgresql://postgres:postgres@localhost/biblivre3 -o biblivre3
"""

if len(sys.argv) == 1:
    parser.print_help()
    print help
    exit(0)

if args.supported:
    print \
    """
    Type 	        Description
    ---------------------------------------------------------
    db2 	        IBM DB2 with 'app' Driver
    db2net 	        IBM DB2 with 'net' Driver
    udbt4 	        DB2 UDB Type 4 Driver
    db2zos 	        DB2 for z/OS
    derby 	        Derby (JavaDB) Embedded Server
    derbynet 	    Derby (JavaDB) Network Server
    firebird 	    Firebird
    hsqldb 	        HSQLDB Server
    informix 	    Informix
    maxdb 	        MaxDB
    mssql 	        Microsoft SQL Server
    mssql05 	    Microsoft SQL Server 2005
    mssql-jtds 	    Microsoft SQL Server with jTDS Driver
    mssql05-jtds 	Microsoft SQL Server 2005 with jTDS Driver
    mysql 	        MySQL
    ora 	        Oracle with OCI8 Driver
    orathin 	    Oracle with Thin Driver
    pgsql 	        PostgreSQL
    sqlite 	        SQLite
    sybase 	        Sybase Server with JDBC3 Driver
    sybase2 	    Sybase Server with JDBC2 Driver
    teradata 	    Teradata (requires -connprops)
    """


def get_database_uri(uri):

    dbtype, url = uri.split('://')

    if dbtype == "sqlite":
        return dict(
        dbtype=dbtype,
        user="",
        passw="",
        hostname="",
        port=-1,
        database=url
        )

    try:
        user, passw = url.split('@')[0].split(':')
    except:
        user = url.split('@')[0]
        passw = ""

    left = url.split('@')[1]

    try:
        hostname_port, database = left.split('/')
    except:
        hostname_port = left
        database = ""

    try:
        hostname, port = hostname_port.split(':')

    except:
        hostname = hostname_port
        port = ""

    return dict(
        dbtype=dbtype,
        user=user,
        passw=passw,
        hostname=hostname,
        port=port,
        database=database
    )


dbdata = get_database_uri(args.path)

print dbdata

dbtype = dbdata['dbtype']
user   = dbdata['user']
passw  = dbdata["passw"]
port   = dbdata["port"]
database = dbdata["database"]
hostname = dbdata["hostname"]

if dbtype == "sqlite":
    jdbc_driver = "-dp " + sqlite_jdbc
    sso = "-sso"

    cmd = ["java -jar", schemaspy, "-t sqlite -db", database, '-o', args.output, sso, jdbc_driver, options]
    cmd = " ".join(cmd)
    os.system(cmd)

if dbtype == "postgresql":

    #postgres_jdbc = sqlite_jdbc

    if port:
        hostname = hostname + ":" + port

    cmd = ["java -jar", schemaspy, "-t pgsql", "-host", hostname,
           "-db", database, "-s public", "-u", user, "-p", passw,
           "-dp", postgres_jdbc, "-o", args.output]
    cmd = " ".join(cmd)
    print cmd
    os.system(cmd)

