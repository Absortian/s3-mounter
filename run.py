# Imports
import os
import json
import sys
import validators
# Imports END

# ENV Variables
mountJson = os.environ['MOUNT_JSON']
try:
    mountJson = json.loads(mountJson)
except ValueError:
    print('Invalid MOUNT_JSON env. Use the format: [{"bucket-one": "/mnt/1"}, {"bucket-two": "/mnt/2"}]')
    sys.exit(1)  
try:
    s3Key = str(os.environ['S3_KEY'])
    s3Secret = str(os.environ['S3_SECRET'])
except:
    print("S3_KEY or S3_SECRET not set")
    sys.exit(1)
try:
    with open(".secretFile", "w") as f:
        f.write(s3Key + ":" + s3Secret)
    os.chmod(".secretFile", 0o600)
except:
    print("Could not create .secretFile")
    sys.exit(1)
try:
    s3Url = str(os.environ['S3_URL'])
except:
    s3Url = None
if s3Url is not None:
    if not validators.url(s3Url):
        print("S3_URL is not a valid URL")
        sys.exit(1)
try:
    s3UsePathRequestStyle = os.environ['S3_USE_PATH_REQUEST_STYLE']
    if s3UsePathRequestStyle.lower() != 'true' and s3UsePathRequestStyle != '1':
        s3UsePathRequestStyle = False
    else:
        s3UsePathRequestStyle = True
except:
    s3UsePathRequestStyle = False
# ENV Variables END

# Logic
for eachMount in mountJson:
    try:
        bucket = str(list(eachMount.keys())[0])
        mountPath = str(list(eachMount.values())[0])
    except IndexError:
        print('Invalid MOUNT_JSON env. Use the format: [{"bucket-one": "/mnt/1"}, {"bucket-two": "/mnt/2"}]')
        sys.exit(1)
    if not bucket or not isinstance(bucket, str):
        print('Detected empty bucket name in MOUNT_JSON env. Use the format: [{"bucket-one": "/mnt/1"}, {"bucket-two": "/mnt/2"}]')
        sys.exit(1)
    if not mountPath or not isinstance(mountPath, str):
        print('Detected empty mount path in MOUNT_JSON env. Use the format: [{"bucket-one": "/mnt/1"}, {"bucket-two": "/mnt/2"}]')
        sys.exit(1)
    if not os.path.exists(mountPath):
        os.makedirs(mountPath)
        print('Created mount path: {}'.format(mountPath))
    # Create string for s3fs command
    s3fsCommand = 's3fs {} {} -o passwd_file=.secretFile'.format(bucket, mountPath)
    if s3Url and isinstance(s3Url, str):
        s3fsCommand += ' -o url={}'.format(s3Url)
    if s3UsePathRequestStyle:
        s3fsCommand += ' -o use_path_request_style'
    print('Running s3fs command: {}'.format(s3fsCommand))
    # Check if s3fs command is successful
    os.system(s3fsCommand)
    if os.path.ismount(mountPath):
        print('Successfully mounted {} to {}'.format(bucket, mountPath))
    else:
        print('Failed to mount {} to {} check if the bucket exists and have the right permissions'.format(bucket, mountPath))
        sys.exit(1)
# Logic END
