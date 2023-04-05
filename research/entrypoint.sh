#!/bin/sh

echo -n "Wait Mongo "
while ! nc -z $MONGO_HOST $MONGO_PORT; do
    echo -n "."
    sleep 0.1
done
echo " started"

echo -n "Wait Cassandra "
while ! nc -z $CASSANDRA_HOST $CASSANDRA_PORT; do
    echo -n "."
    sleep 0.1
done
echo " started"

python main.py

exec "$@"