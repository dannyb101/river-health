#!/bin/bash
# remove old docker version if exists
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine            

# add required package repo
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo

# install docker
sudo dnf install docker-ce --nobest -y
sudo systemctl enable --now docker

# add permission to user
sudo usermod -aG docker jenkins
sudo usermod -aG docker $USER
echo "id jenkins: $(id jenkins)"
echo "id user: $(id $USER)"
