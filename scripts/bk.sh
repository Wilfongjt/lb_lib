
#!/bin/sh
# open _bk.config and load variables
set -o allexport
source ../../../../_dev.config set
set +o allexport
# Backup Source to backup device
if [ ${DEV_BACKUP_FOLDER} == "TBD" ]; then
  echo "define DEV_BACKUP_FOLDER in _bk.config!"
  exit 1
fi;
mkdir -p "${DEV_BACKUP_FOLDER}"
rsync -av --update --delete --exclude={"._*",".git"} "${DEV_FOLDER}" "${DEV_BACKUP_FOLDER}"