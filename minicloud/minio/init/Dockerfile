FROM minio/mc:latest

WORKDIR /init

COPY init.sh /init/init.sh
COPY avatar.svg /init/avatar.svg
COPY report.pdf /init/report.pdf

ENTRYPOINT ["/bin/sh", "/init/init.sh"]