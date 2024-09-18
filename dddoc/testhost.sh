#!/usr/bin/env bash

hr () { printf "%0$(tput cols)d" | tr 0 ${1:-=}; }


hr
echo "Create new dddoc.csv"
mv -v dddoc.csv dddoc.bak
touch dddoc.csv
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"docid": {"date": "date", "title": "title", "status": "status", "statement": "statement", "context": "context", "decision": "decision", "consequences": "consequences", "alternatives": "alternatives", "jira": "jira", "pr": "pr", "refdocs": "refdocs", "participants": "participants", "notes": "notes"}}'
csvlook dddoc.csv

hr
echo "Create doc with missing date"
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"dd2401": {"title": "Use AWS for SHA cluster metadata backups", "status": "Accepted", "statement": "SHA needs an S3 target for k8s cluster metadata backups Need a reliable and always available target for these backups"}}'
curl http://127.0.0.1:5000/data/dd2401
csvlook dddoc.csv
echo

#hr
#echo "delete bad docid - TODO"
#curl http://127.0.0.1:5000/data/dd2401
#csvlook dddoc.csv
#echo

echo "Create doc with wrong date"
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"dd2401": {"date": "2024-07-20", "title": "Use AWS for SHA cluster metadata backups", "status": "Accepted", "statement": "SHA needs an S3 target for k8s cluster metadata backups\rNeed a reliable and always available target for these backups"}}'
curl http://127.0.0.1:5000/data/dd2401
csvlook dddoc.csv
echo

hr
echo "update doc to correct date"
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"dd2401": {"date": "2024-08-20"}}'
curl http://127.0.0.1:5000/data/dd2401
csvlook dddoc.csv
echo

hr
echo "Returning dddoc.csv to original"
mv -v dddoc.bak dddoc.csv
csvlook dddoc.csv
echo
echo "Test complete"
