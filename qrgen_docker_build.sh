#!/bin/bash
docker build -t qrgen-app .
docker run -d -p 5050:5050 --name qrgen qrgen-app
