#!/bin/sh
set -e
# Password
echo "$AWS_KEY:$AWS_SECRET_KEY" > passwd && chmod 600 passwd
# -o url=https://url.to.s3/ -o use_path_request_style

mkdir -p "$MNT_POINT"
s3fs "$S3_BUCKET" "$MNT_POINT" -o passwd_file=passwd  && tail -f /dev/null
