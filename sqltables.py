#!/usr/bin/env python2

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.sql import select
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, backref

from utils import joinstr
from sqlalchemy import inspect

from pprint import pprint
import sys


DEBUG_SQL = False

# create the pydot graph object by autoloading all tables via a bound metadata object
def create_schema(dbpath):
    from sqlalchemy_schemadisplay import create_schema_graph

    graph = create_schema_graph(metadata=MetaData(dbpath),
                                show_datatypes=False,  # The image would get nasty big if we'd show the datatypes
                                show_indexes=False,  # ditto for indexes
                                rankdir='LR',  # From left to right (instead of top to bottom)
                                concentrate=False  # Don't try to join the relation lines together
    )
    graph.write_png('dbschema.png')  # write out the file


def get_version():
    return sqlalchemy.__version__


def verbose():
    db.echo = True


def silent():
    db.echo = False


def get_tables():
    return meta.tables.keys()


# Get table
def get_table(tablename):
    return meta.tables[tablename]


def create_table_code():
    code = ""

    for table in get_tables():
        table_code = "{tablename} = get_table('{tablename}')".format(tablename=table)
        code = joinstr([code, table_code, '\n'], "")

    return code


def colls(table):
    """ Return table columns """
    print table.columns.keys()


# Primary key
def pmkey(table):
    """ Return all primary keys """
    return table.primary_key.columns.keys()


# Foreign keys
def fnkey(table):
    """ Return all table foreign keys """
    return table.foreign_keys


def findcoll(collname):
    """
    Find all tables that has the column collname
    """
    tablelst = []

    for tablename in get_tables():

        table = get_table(tablename)

        if collname in table.columns.keys():
            tablelst.append(tablename)

    return tablelst


# pprint( inspector.get_table_names())
# pprint( inspector.get_columns('items'))
#pprint( inspector.get_foreign_keys('items'))

"""
product_table = Table(
'product', metadata,
Column('brand_id', Integer, ForeignKey('brand.id')),
Column('sku', Unicode(80)),
PrimaryKeyConstraint('brand_id', 'sku', name='prikey'))


Table('items', MetaData(bind=None), 
    Column('itemID', INTEGER(), table=<items>, primary_key=True, nullable=False), 
    Column('itemTypeID', INTEGER(), table=<items>, nullable=False),
    Column('dateAdded', TIMESTAMP(), table=<items>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0xb3b682cc>, for_update=False)), 
    Column('dateModified', TIMESTAMP(), table=<items>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0xb3b6838c>, for_update=False)), 
    Column('clientDateModified', TIMESTAMP(), table=<items>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0xb3b68dac>, for_update=False)), 
    Column('libraryID', INTEGER(), ForeignKey(u'libraries.libraryID'), table=<items>), 
    Column('key', TEXT(), table=<items>, nullable=False), 
    schema=None)

"""

table_tpl = \
    r"""
{TableName} = Table("{table}", metadata,
{columns}
)
"""

column_tpl = \
    r"""
    Column({data}),
""".strip('\n')

header = \
    """
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import *
{dbtypes}
metadata=MetaData()
"""

postgres_types = \
    """
from sqlalchemy.dialects.postgresql import \
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
    INTERVAL, MACADDR, NUMERIC, REAL, SMALLINT, TEXT, TIME, \
    TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
    DATERANGE, TSRANGE, TSTZRANGE
"""

sqlitetypes = ""

sqldbtypes = dict(sqlite=sqlitetypes, postgresql=postgres_types)

foreign_keys = None


def foreign_keys_map(table):
    foreign_keys = inspector.get_foreign_keys(table)

    keys = {}

    for cell in foreign_keys:
        #print "cell =", cell
        fnkey = cell['constrained_columns'][0]
        table = cell['referred_table']
        rcol = cell['referred_columns'][0]
        keys[fnkey] = (table, rcol)

    return keys


def create_column_code(col, table):
    fnkey_map = foreign_keys_map(table)

    ##print "fnkey_map = ", fnkey_map

    ##print "col = ", col

    bols = ["False", "True"]

    name = col['name']
    nullable = col['nullable']
    try:
        primary_key = col['primary_key']
    except:
        primary_key = 0

    default = col['default']

    #import IPython ; IPython.embed()

    if type(col['type']) == sqlalchemy.sql.sqltypes.NullType:
        _type = "NullType()"
    else:
        _type = str(col['type'])

    if _type == "TIMESTAMP WITHOUT TIME ZONE":
        _type = "DATETIME()"

    if not _type.endswith(')'):
        _type += '()'

    if name in fnkey_map.keys():
        ftable, fcolumn = fnkey_map[name]
        _foreign_keys = "ForeignKey(\"%s.%s\")" % (ftable, fcolumn)
        #print "_foreign_keys = ", _foreign_keys
    else:
        _foreign_keys = None

    code = [
        '\"%s\"' % name,
        _type,
        _foreign_keys,
        "primary_key=%s" % str(primary_key),
        "nullable=%s" % nullable,
        #"default=%s" % str(default),
    ]

    _code = joinstr(code, ", ")

    return column_tpl.format(colname=name, data=_code)


def table_code(table):
    ##print "------table = ", table

    columns = inspector.get_columns(table)


    ##print "columns = ", columns
    ##print "--------------"
    #create_column_code(columns[0])   
    columns_code = [create_column_code(col, table) for col in columns]
    columns_code_ = joinstr(columns_code, '\n')
    ##print columns_code_
    return table_tpl.format(TableName=table, table=table, columns=columns_code_)


def create_code(dbtype):
    codes = [table_code(table) for table in inspector.get_table_names()]
    code = joinstr(codes, "")

    try:
        _dbtypes = sqldbtypes[dbtype]
    except:
        _dbtypes = ""

    #print "_dbtypes ", _dbtypes

    return header.format(dbtypes=_dbtypes) + code


#=============== COMMAND LINE PARSER =======================#

import argparse
import sys

desc = "SlQL Table constructor"
parser = argparse.ArgumentParser(prog=sys.argv[0], description=desc)

parser.add_argument("--database", "-d", help="Database type")
parser.add_argument("--path", "-p", help="Database URL")
parser.add_argument("--tables", "-ts", action="store_true", help="Print database tables")
parser.add_argument("--table", "-t", help="Print table columns")
parser.add_argument("--explore", "-e", action="store_true", help="Interactively explore the database")
parser.add_argument("--schema", "-s", action="store_true", help="Create schema ")

args = parser.parse_args()

description = \
    """
Create python SQL Alchemy tables of SQL databases

Example:

./sqltables.py -d sqlite -p /home/tux/.zotserver/zotero.sqlite  > tables.py
./sqltables.py  -d postgresql -p postgres:postgres@localhost/biblivre3 > tables.py
"""

if len(sys.argv) == 1:
    parser.print_help()
    print description
    sys.exit(0)

if args.database:
    if args.database == 'sqlite':
        uri = 'sqlite:///'
    else:
        uri = args.database + r'://'

else:
    print "No datbase informed"
    sys.exit(1)

if not args.path:
    sys.exit(1)

dbpath = uri + args.path

#print "dbpath = ", dbpath


# db = engine
# db name is for lazy programmers


db = create_engine(dbpath, echo=DEBUG_SQL)
meta = MetaData()
meta.reflect(bind=db)
inspector = inspect(db)

Session = sessionmaker(bind=db)
s = Session()

if args.tables:
    pprint(inspector.get_table_names())
    sys.exit(0)

if args.table:
    print 30 * "-"
    print "COLUMNS "
    pprint(inspector.get_columns(args.table))
    print "\n"
    print "FOREIGN KEYS"

    pprint(inspector.get_foreign_keys(args.table))
    sys.exit(0)

if args.explore:
    print "Session object:\ts"
    print "Inspector object:\tinspector"
    print "Database engine object:\tdb"
    import IPython

    IPython.embed()

    sys.exit(0)

if args.schema:
    create_schema(dbpath)
    sys.exit(0)

print create_code(args.database)


