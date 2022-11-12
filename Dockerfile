FROM alpine:3.12

ENV S3FS_VERSION=v1.86

RUN apk --update --no-cache add fuse alpine-sdk automake autoconf libxml2-dev fuse-dev curl-dev git bash python3 py3-pip; \
    pip3 install --upgrade setuptools pip validators; \
    git clone https://github.com/s3fs-fuse/s3fs-fuse.git; \
    cd s3fs-fuse; \
    git checkout tags/${S3FS_VERSION}; \
    ./autogen.sh; \
    ./configure --prefix=/usr; \
    make; \
    make install; \
    make clean; \
    rm -rf /var/cache/apk/*; \
    apk del git automake autoconf;

COPY run.py /run.py
CMD python3 /run.py && tail -f /dev/null
