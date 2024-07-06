#!/bin/bash

# Load configuration from external file
CONFIG_FILE="/home/e.guluzade/backup.conf"
if [ -f "$CONFIG_FILE" ]; then
	source "$CONFIG_FILE"
else
	echo "Configuration file not found!"
	exit 1
fi

# Defining variables

BACKUP_DATE=$(date +%Y%m%dH%M%S)
BACKUP_FILENAME="backup_$BACKUP_DATE.tar.gz"
LOG_FILE="$BACKUP_DST/backup_$BACKUP_DATE.log"
mkdir -p "$BACKUP_DST/backup_$BACKUP_DATE"

# Start logging
exec >> >(tee -a "$LOG_FILE") 2>&1
tar -czf "$BACKUP_DST/backup_$BACKUP_DATE/$BACKUP_FILENAME" -C "$BACKUP_SRC" .

# Verify the backup was created successfully
if [ $? -eq 0 ]; then
	echo "backup successful: $BACKUP_FILENAME"
else
	echo "Backup failed"
	ssmtp bugx.academy@gmail.com < failure_email.txt
	exit 1
fi

# Implement backup rotation to keep last 5 backups
NUM_BACKUPS_TO_KEEP=5
cd "$BACKUP_DST"
find . -maxdepth 1 -name "backup_*" -type d | sort -r | sed -e "1,${NUM_BACKUPS_TO_KEEP}d" | xargs rm -rf
find . -maxdepth 1 -name "backup_*.log" | sort -r | sed -e "1,${NUM_BACKUPS_TO_KEEP}d" | xargs rm -rf

echo "Backup script completed successfully"
exit 0
