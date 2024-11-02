#!/usr/bin/env bash

csvcmd='jq'
lookcmd='cat'

[ -z $1 ] && echo "usage: $0 <index> [csv|look]" && exit 1

[ -n $2 ] && [ "$2" == "csv" ] && csvcmd='in2csv -f json -k data'
[ -n $2 ] && [ "$2" == "look" ] && csvcmd='in2csv -f json -k data' && lookcmd='csvlook -I'


curl -s http://127.0.0.1:5000/data/$1 | jq 'reduce to_entries[] as {$key, $value} ({"data": []}; .data += [{"index": $key} + $value])' | $csvcmd | $lookcmd
