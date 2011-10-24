#!/bin/sh
CLASSPATH=`echo /usr/share/couchdb-lucene/jars/*.jar | sed "s/ /:/g"`
CLASS=com.github.rnewson.couchdb.lucene.Main
JAVA_OPTS="-server -Xmx1g"
LOGDIR=/var/log/couchdb-lucene
cd /usr/share/couchdb-lucene
java ${JAVA_OPTS} -classpath "${CLASSPATH}" "${CLASS}" 2>$LOGDIR/stderr.log >$LOGDIR/stdout.log & disown
