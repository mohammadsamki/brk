

# Set the backup directory
BACKUP_DIR=/var/www/brian-cm  

# Set the PostgreSQL user and passwor
FILENAME=$BACKUP_DIR/all-databases-$(date +%Y-%m-%d-%H-%M-%S).sql

# Set the PostgreSQL user and password
PG_USER=postgres
PG_PASSWORD=zVI2u_8O86Pk

# Get a list of all databases
DATABASES=$(psql -U $PG_USER -h localhost -l -t | cut -d'|' -f1 | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e '/^$/d')

# Create the backup file
echo "-- Databases: $DATABASES" > $FILENAME
pg_dumpall -U $PG_USER -h localhost >> $FILENAME
