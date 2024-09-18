#!/bin/bash

mac=$1
ip=$2
hostname=$3
bootimage=$4

#postdata='{"'${mac}'": {"ipaddr": "'${ip}'", "hostname": "'${hostname}'", "bootimage": "'${bootimage}'"}}'
postdata='{"'${mac}'": {"ipaddr": "'${ip}'"}}'
echo $postdata
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d $postdata

curl http://127.0.0.1:5000/data/$mac


curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"00:1A:2B:3C:4D:5E": {"ipaddr": "192.168.1.3"}}'