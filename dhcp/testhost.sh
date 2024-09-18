#!/usr/bin/env bash

hr () { printf "%0$(tput cols)d" | tr 0 ${1:-=}; }


hr
echo "Create new dhcp-reservation.csv"
mv -v dhcp-reservation.csv dhcp-reservation.bak
touch dhcp-reservation.csv
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"mac": {"ipaddr": "ipaddr", "hostname": "hostname", "bootimage": "bootimage"}}'
csvlook dhcp-reservation.csv

hr
echo "Create test host with wrong mac"
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"00:1A:2B:3C:4D:5E": {"ipaddr": "192.168.1.3", "hostname": "mike-proart.10g", "bootimage": "disk"}}'
curl http://127.0.0.1:5000/data/00:1A:2B:3C:4D:5E
csvlook dhcp-reservation.csv
echo

hr
echo "delete bad mac - TODO"
curl http://127.0.0.1:5000/data/00:1A:2B:3C:4D:5E
csvlook dhcp-reservation.csv
echo

echo "Create mike-proart with wrong ipaddr"
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"10:7c:61:62:b6:0a": {"ipaddr": "192.168.1.3", "hostname": "mike-proart.10g", "bootimage": "disk"}}'
curl http://127.0.0.1:5000/data/10:7c:61:62:b6:0a
csvlook dhcp-reservation.csv
echo

hr
echo "update mike-proart to correct ipaddr"
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"10:7c:61:62:b6:0a": {"ipaddr": "10.0.0.2"}}'
curl http://127.0.0.1:5000/data/10:7c:61:62:b6:0a
csvlook dhcp-reservation.csv
echo

hr
echo "Returning dhcp-reservation.csv to original"
mv -v dhcp-reservation.bak dhcp-reservation.csv
csvlook dhcp-reservation.csv
echo
echo "Test complete"
