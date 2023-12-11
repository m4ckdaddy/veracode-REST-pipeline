#!/bin/bash
# CLEAR INPUT.JSON for SANITY CHECK
touch input.json
#echo ' ' > input.json
http --auth-type=veracode_hmac POST "https://api.veracode.com/pipeline_scan/v1/scans" < input.json > firstout.json
python3 pipeline.py
echo "Fetching Scan Results"
python3 fetch.py 
#> veracode-pipeline-scan_results.json
echo "Veracode Pipeline Scan Completed, please check 'veracode-pipeline-scan_results.json' for Scan Results"
