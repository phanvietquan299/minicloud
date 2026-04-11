#!/bin/sh
set -eu

: "${DOCKERHUB_NAMESPACE:?Set DOCKERHUB_NAMESPACE, for example myname}"
: "${IMAGE_TAG:?Set IMAGE_TAG, for example v1}"

docker login

docker build -t "${DOCKERHUB_NAMESPACE}/myminicloud-web:${IMAGE_TAG}" ./web
docker build -t "${DOCKERHUB_NAMESPACE}/myminicloud-web-lb1:${IMAGE_TAG}" ./web
docker build -t "${DOCKERHUB_NAMESPACE}/myminicloud-web-lb2:${IMAGE_TAG}" ./web
docker build -t "${DOCKERHUB_NAMESPACE}/myminicloud-backend:${IMAGE_TAG}" ./app

docker push "${DOCKERHUB_NAMESPACE}/myminicloud-web:${IMAGE_TAG}"
docker push "${DOCKERHUB_NAMESPACE}/myminicloud-web-lb1:${IMAGE_TAG}"
docker push "${DOCKERHUB_NAMESPACE}/myminicloud-web-lb2:${IMAGE_TAG}"
docker push "${DOCKERHUB_NAMESPACE}/myminicloud-backend:${IMAGE_TAG}"