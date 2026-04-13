# MyMiniCloud Demo

Project for the mini cloud deployment lab.

## Run

```bash
cd "/Users/zitqan/Documents/Cloud Computing/Final/minicloud"
docker compose up -d --build
```

## Production run

Use this only on Ubuntu EC2. Build and push images first with `sh scripts/publish-images.sh`, then run the production helper on EC2.

```bash
sh deploy/run-prod-ec2.sh
```

## EC2 source-based run

If you only push a minimal set of images to Docker Hub and want EC2 to build the full stack from source, use:

```bash
sh deploy/run-ec2-source.sh
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
