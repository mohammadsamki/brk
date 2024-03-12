# Set the backup directory
BACKUP_DIR=/var/www/mysitebrians  

# Set the PostgreSQL user and password
PG_USER=postgres
PG_PASSWORD=zVI2u_8O86Pk

# Set the filename of the backup file
BACKUP_FILE=$BACKUP_DIR/all-databases-2023-08-25-12-52-13.sql

# Check if the backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found!"
    exit 1
fi

# Restore the backup
psql -U $PG_USER -h localhost -f $BACKUP_FILE
