#!/bin/bash

# Set the backup directory
BACKUP_DIR=/var/www/brian-cm  

# Set the PostgreSQL user and password
PG_USER=postgres
PG_PASSWORD=zVI2u_8O86Pk

# Set the filename of the backup file
# Replace this with the actual filename of your backup file
BACKUP_FILE=$BACKUP_DIR/all-databases-2023-10-25-17-17-30.sql

# Export the PostgreSQL password so that pg_restore doesn't prompt for it
export PGPASSWORD=$PG_PASSWORD

# Restore the databases from the backup file
psql -U $PG_USER -h localhost -f $BACKUP_FILE

# Unset the PostgreSQL password
unset PGPASSWORD
