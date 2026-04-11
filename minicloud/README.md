# MyMiniCloud Demo

Project for the mini cloud deployment lab.

## Run

```bash
cd "/Users/zitqan/Documents/Cloud Computing/Final/minicloud"
docker compose up -d --build
```

## Production run

```bash
cp .env.example .env
# fill DOCKERHUB_NAMESPACE and IMAGE_TAG
docker compose -f docker-compose.prod.yml --env-file .env up -d
```

## Test

- Web: http://localhost:8080/
- App: http://localhost:8085/hello
- Student API: http://localhost/api/student
- Proxy: http://localhost/api/hello
- Keycloak: http://localhost:8081/auth
- Database-backed API: http://localhost:8085/students-db
- MinIO: http://localhost:9001
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Naming convention

- web
- app
- db
- auth
- minio
- dns
- prometheus
- grafana
- proxy

## Deployment

See [deploy/DEPLOYMENT.md](deploy/DEPLOYMENT.md) for Docker Hub and AWS EC2 steps.
