FROM python:3.11-alpine

WORKDIR /init

COPY init-keycloak.py /init/init-keycloak.py

CMD ["python", "/init/init-keycloak.py"]