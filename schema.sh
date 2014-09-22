#!/bin/bash
#
# This script creates the dabase schema of sqlite3 database
#
#
#----------------------------------------------
#
# Java JDK installation path to Oracle JAVA
export JAVA_HOME=/opt/java/
export JDK_HOME=/opt/java

export CLASSPATH=/opt/java/lib/:/opt/java/jre/lib
PATH=$PATH:$JAVA_HOME:$JAVA_HOME/jre/bin

driver=org.sqlite.JDBC
description=SQLite
connectionSpec=jdbc:sqlite:<db>
#description=SQLite-Xerial
driverPath=/opt/schemaspy/sqlite.jar

java -jar /opt/schemaspy/schemaSpy_5.0.0.jar -t sqlite -db "$1" -o schema -sso  -dp $driverPath

