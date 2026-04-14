# MyMiniCloud Demo

Project for the mini cloud deployment lab.

## Run

```bash
cd "/Users/zitqan/Documents/Cloud Computing/Final/minicloud"
docker compose up -d --build
```

## Production run

Use the manual workflow described in [DEPLOYMENT_PLAYBOOK.md](DEPLOYMENT_PLAYBOOK.md) for the cleanest deployment path.

```bash
sh deploy/aws-ec2-ubuntu.sh
git clone <YOUR_GITHUB_REPO_URL>
cd <YOUR_REPO_FOLDER>
docker compose up -d --build
```

## EC2 source-based run

If you want EC2 to build the full stack from source after cloning the repo, use:

```bash
sh deploy/run-ec2-source.sh
```

## EC2 hybrid run

If you want EC2 to pull 4 custom images from Docker Hub and use official images for the rest, use:

```bash
docker compose -f docker-compose.aws.yml --env-file .env up -d
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
