#!/bin/bash
echo "Deploying cosmic-themes, prepare for liff off..."
cd /home/austin/docker/cosmic-themes-py/build
docker build -t cosmic-themes-py .
cd ../
docker-compose up -d
