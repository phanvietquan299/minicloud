#!/bin/sh
set -eu

export DOCKERHUB_NAMESPACE="phanvietquan"
export IMAGE_TAG="v3"

docker build --build-arg SERVER_LABEL=core -t "${DOCKERHUB_NAMESPACE}/myminicloud-web:${IMAGE_TAG}" ./web
docker build --build-arg SERVER_LABEL=lb1 -t "${DOCKERHUB_NAMESPACE}/myminicloud-web-lb1:${IMAGE_TAG}" ./web
docker build --build-arg SERVER_LABEL=lb2 -t "${DOCKERHUB_NAMESPACE}/myminicloud-web-lb2:${IMAGE_TAG}" ./web
docker build -t "${DOCKERHUB_NAMESPACE}/myminicloud-backend:${IMAGE_TAG}" ./app

docker push "${DOCKERHUB_NAMESPACE}/myminicloud-web:${IMAGE_TAG}"
docker push "${DOCKERHUB_NAMESPACE}/myminicloud-web-lb1:${IMAGE_TAG}"
docker push "${DOCKERHUB_NAMESPACE}/myminicloud-web-lb2:${IMAGE_TAG}"
docker push "${DOCKERHUB_NAMESPACE}/myminicloud-backend:${IMAGE_TAG}"