#!/usr/bin/env python2

import os
import sys
import time
import shutil

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
isdir = os.path.isdir
isfile = os.path.isfile
exists  = os.path.exists
copy  = shutil.copy

sleep = time.sleep

exit = sys.exit

INSTALL="/opt"
schemadir = join(INSTALL, "schemaspy")

chdir(INSTALL)


if not isdir(schemadir):
        
    print "Clonning repository"

    os.system("git clone  https://github.com/wolfprogrammer/schemaspybin")
    os.system("mv schemaspybin schemaspy")


# Compile Source Code
chdir(schemadir)

print os.getcwd()
print os.listdir(".")

os.system("tar -xvf javasqlite.tar")


chdir("javasqlite-20140624")

os.system("./configure")
os.system("make")
os.system("sudo make install")

copy("sqlite.jar", schemadir)

print "Installed"
