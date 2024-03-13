# Set the backup directory
BACKUP_DIR=/Users/macbookair/Desktop/

# Set the PostgreSQL user and password
PG_USER=postgres
PG_PASSWORD=zVI2u_8O86Pk

# Set the filename of the backup file
BACKUP_FILE=$BACKUP_DIR/all-databases-2024-03-12-01-29-11.sql

# Check if the backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found!"
    exit 1
fi

# Restore the backup
psql -U $PG_USER -h localhost -f $BACKUP_FILE
