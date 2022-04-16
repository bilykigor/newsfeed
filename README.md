#!/bin/bash
yum update -y
yum install docker -y
yum install git -y
systemctl enable docker.service
systemctl start docker.service

git clone https://github.com/bilykigor/newsfeed.git
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

cd newsfeed
wget "https://drive.google.com/uc?export=download&id=1Mhva8BN8zXxH2nToZhH5qXOj9SVwkz65" -O variables.env

