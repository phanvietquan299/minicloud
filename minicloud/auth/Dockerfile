FROM quay.io/keycloak/keycloak:25.0.5

COPY realm-export.json /opt/keycloak/data/import/realm-export.json

EXPOSE 8080

CMD ["start-dev", "--import-realm"]