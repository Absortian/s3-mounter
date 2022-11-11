mountJson = os.environ['MOUNT_JSON']
try:
    mountJson = json.loads(mountJson)
except ValueError:
    print('Invalid MOUNT_JSON env. Use the format: [{"bucket-one": "/mnt/1"}, {"bucket-two": "/mnt/2"}]')
    sys.exit(1)    
for eachMount in mountJson:
    try:
        bucket = list(eachMount.keys())[0]
        mountPath = list(eachMount.values())[0]
    except IndexError:
        print('Invalid MOUNT_JSON env. Use the format: [{"bucket-one": "/mnt/1"}, {"bucket-two": "/mnt/2"}]')
        sys.exit(1)
    # Print the bucket and mount path
    print('Bucket: %s, Mount Path: %s' % (bucket, mountPath))

