import json
import subprocess
import tempfile
import time

def main():
    # Path to the JSON output file
    json_output_file = 'firstout.json'

    # Read the JSON file
    with open(json_output_file, 'r') as file:
        data = json.load(file)

    # Extracting required values
    scan_id = data.get('scan_id')
    binary_segments_expected = data.get('binary_segments_expected')
    binary_segments_uploaded = data.get('binary_segments_uploaded')

    # Generate and execute HTTP PUT commands for binary segments
    for segment in range(binary_segments_uploaded, binary_segments_expected):
        file_segment = chr(97 + segment)  # Converts segment number to corresponding lowercase letter
        command = f"http --auth-type=veracode_hmac -f PUT \"https://api.veracode.com/pipeline_scan/v1/scans/{scan_id}/segments/{segment}\" file@xa{file_segment}"
        subprocess.run(command, shell=True)

    # After uploading all segments, start the scan
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        # Write the JSON payload to a temporary file
        json.dump({"scan_status": "STARTED"}, temp_file)
        temp_file_path = temp_file.name

    # Execute the HTTP PUT command to start the scan
    start_scan_command = f"http --auth-type=veracode_hmac PUT \"https://api.veracode.com/pipeline_scan/v1/scans/{scan_id}\" < {temp_file_path}"
    subprocess.run(start_scan_command, shell=True)

    # Poll the scan status every 30 seconds
    while True:
        time.sleep(30)  # Wait for 30 seconds
        status_command = f"http --auth-type=veracode_hmac GET \"https://api.veracode.com/pipeline_scan/v1/scans/{scan_id}\""
        result = subprocess.run(status_command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            scan_status = json.loads(result.stdout).get("scan_status", "")
            if scan_status == "SUCCESS":
                break

    # Fetch the findings
    findings_command = f"http --auth-type=veracode_hmac GET \"https://api.veracode.com/pipeline_scan/v1/scans/{scan_id}/findings\""
    subprocess.run(findings_command, shell=True)

if __name__ == "__main__":
    main()

