#!/bin/sh

# Check if config is mounted
if [ -f /config/.config/rclone/rclone.conf ]; then
    echo "Using mounted rclone config"
    export RCLONE_CONFIG=/config/.config/rclone/rclone.conf
else
    echo "No rclone config found!"
    exit 1
fi

# Run rclone sync
rclone sync "/data" --progress --webdav-url=BASEURL --webdav-user=PROJECTURL --webdav-pass=PASSWORD --webdav-vendor=nextcloud --webdav-nextcloud-chunk-size=0 :webdav: