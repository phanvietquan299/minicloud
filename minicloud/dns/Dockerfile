FROM internetsystemsconsortium/bind9:9.18

COPY named.conf /etc/bind/named.conf
COPY named.conf.options /etc/bind/named.conf.options
COPY named.conf.local /etc/bind/named.conf.local
COPY db.cloud.local /etc/bind/db.cloud.local

EXPOSE 53/udp