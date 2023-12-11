import os
import math
import subprocess
import json
import hashlib
import subprocess

def get_file_size(file_path):
    """Returns the size of the file in bytes."""
    return os.path.getsize(file_path)

def get_file_hash(file_path):
    """Returns the SHA256 hash of the file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def split_file(file_path, segments):
    """Splits the file into the specified number of segments."""
    command = f"split -n {segments} {file_path}"
    subprocess.run(command, shell=True)

def save_to_json(binary_name, project_name, project_uri, dev_stage, segments, binary_size, binary_hash):
    """Saves details to input.json in JSON format."""
    data = {
        "binary_name": binary_name,
        "project_name": project_name,
        "project_uri": project_uri,
        "dev_stage": dev_stage,
        "segments": segments,
        "binary_size": binary_size,
        "binary_hash": binary_hash
    }
    with open("input.json", "w") as file:
        json.dump(data, file, indent=4)

#def send_post_request():
#    """Sends a POST request to the Veracode API."""
#    try:
#        subprocess.run(["http", "--auth-type=veracode_hmac", "POST", "https://api.veracode.com/pipeline_scan/v1/scans", "<", "input.json"], check=True)
#        print("POST request sent successfully.")
#    except subprocess.CalledProcessError as e:
#        print(f"An error occurred while sending the POST request: {e}")

def main():
    # Ask the user for the file path
    file_path = input("Please enter the path to the binary file: ")

    # Check if the file exists
    if not os.path.exists(file_path):
        print("File does not exist. Please check the path and try again.")
        return

    # Get the file size and hash
    binary_size = get_file_size(file_path)
    binary_hash = get_file_hash(file_path)

    # Calculate the number of segments
    segments = math.ceil(binary_size / 2621440)

    # Split the file
    split_file(file_path, segments)
    print(f"The file has been split into {segments} segments.")

    # Ask for additional details
    binary_name = input("Enter the binary name: ")
    project_name = input("Enter the project name: ")
    project_uri = input("Enter the project URI: ")
    dev_stage = "DEVELOPMENT"

    # Save details to JSON
    save_to_json(binary_name, project_name, project_uri, dev_stage, segments, binary_size, binary_hash)

    # Send the POST request
#    send_post_request()

if __name__ == "__main__":
    main()

