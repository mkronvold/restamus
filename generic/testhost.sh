#!/usr/bin/env bash

hr () { printf "%0$(tput cols)d" | tr 0 ${1:-=}; }

base=generic

hr
echo "Create new ${}base}.csv"
mv -v ${base}.csv ${base}.bak
touch ${base}.csv
./makeheader.sh
csvlook ${base}.csv

hr
echo "Create entry with missing column_a"
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"2401": {"column_b": "column_b data", "column_k": "column_k data", "column_e": "column_e data"}}'
curl http://127.0.0.1:5000/data/2401
csvlook ${base}.csv
echo

#hr
#echo "delete bad entry - TODO"
#curl http://127.0.0.1:5000/data/2401
#csvlook ${base}.csv
#echo

echo "Create entry with wrong column_a data"
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"2401": {"column_a": "bad data", "column_b": "column_b data", "column_c": "column_c data", "column_d": "column_d data"}}'
curl http://127.0.0.1:5000/data/2401
csvlook ${base}.csv
echo

hr
echo "update entry to correct data"
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"2401": {"column_a": "corrected column_a data"}}'
curl http://127.0.0.1:5000/data/2401
csvlook ${base}.csv
echo

hr
echo "update entry to add more fields"
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"2401": {"column_e": "additional column_e data", "column_f": "additional column_f data"}}'
curl http://127.0.0.1:5000/data/2401
csvlook ${base}.csv
echo

hr
echo "Returning ${base}.csv to original"
#mv -v ${base}.bak ${base}.csv
csvlook ${base}.csv
echo
echo "Test complete"
