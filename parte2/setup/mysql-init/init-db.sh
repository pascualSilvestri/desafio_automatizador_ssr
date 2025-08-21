#!/bin/bash
set -e

# This script will be run by the MySQL container on initialization.
# Place your SQL commands below, for example:
mysql -u root -p"$MYSQL_ROOT_PASSWORD" < ./repuestosDB_init.sql
