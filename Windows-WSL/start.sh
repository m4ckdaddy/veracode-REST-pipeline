#!/bin/bash
echo "Usage: Please enter the path to the binary for Veracode Pipeline Scannner via REST API" 
# SANITY CHECK 
touch input.json
http --auth-type=veracode_hmac POST "https://api.veracode.com/pipeline_scan/v1/scans" < input.json > firstout.json
echo "Python Execute"
python3 pipelined.py
echo "pipeline-scan initialializing"
python3 fetch.py
echo "pipeline-scan Successful, please check findings file for results"
