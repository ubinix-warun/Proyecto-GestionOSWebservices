#!/bin/bash
#docker build -t oswebservice:latest .
docker run -d -p 6060:5000 -v $(pwd):/app oswebservice
sleep 10
curl localhost:6060
