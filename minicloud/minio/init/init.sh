#!/bin/sh
set -eu

until mc alias set myminio http://object-storage-server:9000 minioadmin minioadmin >/dev/null 2>&1; do
  sleep 2
done

mc mb --ignore-existing myminio/profile-pics
mc mb --ignore-existing myminio/documents
mc anonymous set download myminio/profile-pics
mc anonymous set download myminio/documents
mc cp /init/avatar.svg myminio/profile-pics/avatar.svg
mc cp /init/report.pdf myminio/documents/report.pdf