# MyMiniCloud Deployment Notes

## Docker Hub

Set the namespace and image tag, then run:

```bash
export DOCKERHUB_NAMESPACE=<your-dockerhub-user>
export IMAGE_TAG=v1
sh scripts/publish-images.sh
```

## AWS EC2 Ubuntu

Run the bootstrap script on a fresh Ubuntu EC2 instance:

```bash
sh deploy/aws-ec2-ubuntu.sh
```

After relogin:

```bash
cd minicloud
docker compose up -d --build
```

## Notes

- Keep `cloud-net` as the single Docker network.
- Open ports `80, 8080, 8081, 8082, 8083, 8085, 9000, 9001, 9090, 3000, 3306, 1053/udp` in the EC2 security group.
- Use `docker compose ps` and `docker logs <container>` for verification.