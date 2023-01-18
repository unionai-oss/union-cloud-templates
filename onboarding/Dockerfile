# 🐳📦 Docker containers unlock OS-level reproducibility 🔄
# docker buildx create --name bbb --driver docker-container --driver-opt image=moby/buildkit:master \
#   --buildkitd-flags '--allow-insecure-entitlement security.insecure' --platform linux/arm64,linux/amd64
# docker buildx build --builder bbb --allow security.insecure --platform linux/arm64,linux/amd64 \
#   --push -t ghcr.io/unionai-oss/union-cloud-templates:yt-v0.2 .
# Can also use -t localhost:30000/cloud-templates:v0.1 if you want to use the registry that comes with flytectl demo
#   You'll need to push to localhost:30000 after building.
FROM python:3.9-slim-buster

WORKDIR /root
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV GIT_PYTHON_REFRESH quiet

RUN apt-get update && apt-get install -y build-essential vim git
RUN pip3 install awscli

# Install Python dependencies
COPY ./requirements.txt /root
RUN pip install -r /root/requirements.txt

# Copy the actual code
COPY . /root
RUN pip install -e /root
