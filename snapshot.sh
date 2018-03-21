#!/bin/bash


consul="localhost:8500"
dump_file="$2"

case "$1" in
	dump) curl -X GET http://${consul}/v1/snapshot -o $(date +%F).snap.tar.gz
		;;
	restore) curl -X PUT --data-binary @${dump_file} http://${consul}/v1/snapshot
		;;
esac	
