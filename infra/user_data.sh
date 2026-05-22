#!/bin/bash
set -eux

# --- Install Docker ---
apt-get update -y
apt-get install -y ca-certificates curl git

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Resolve arch and codename into plain variables — avoids $(...) inside the echo
ARCH=$(dpkg --print-architecture)
. /etc/os-release

echo "deb [arch=$ARCH signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $VERSION_CODENAME stable" \
  | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# --- Pull pre-built image from GHCR ---
GHCR_IMAGE="ghcr.io/poloziuk/uptime-monitor/uptime-monitor:${image_tag}"
docker pull "$GHCR_IMAGE"

# Tag for docker compose (project=uptime-monitor, services=app+worker)
docker tag "$GHCR_IMAGE" uptime-monitor-app:latest
docker tag "$GHCR_IMAGE" uptime-monitor-worker:latest

# --- Clone repo for docker-compose.yml ---
git clone https://github.com/poloziuk/uptime-monitor.git /app
cd /app

# --- Start the stack (no rebuild — images already loaded above) ---
docker compose -p uptime-monitor up -d --no-build
