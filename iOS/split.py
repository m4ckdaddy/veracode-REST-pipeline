import os
import math
import subprocess

def get_file_size(file_path):
    """Returns the size of the file in bytes."""
    return os.path.getsize(file_path)

def split_file(file_path, segments):
    """Splits the file into the specified number of segments."""
    command = f"split -n {segments} {file_path}"
    subprocess.run(command, shell=True)

def main():
    # Ask the user for the file path
    file_path = input("Please enter the path to the binary file: ")

    # Check if the file exists
    if not os.path.exists(file_path):
        print("File does not exist. Please check the path and try again.")
        return

    # Get the file size
    size = get_file_size(file_path)

    # Calculate the number of segments
    segments = math.ceil(size / 2621440)

    # Split the file
    split_file(file_path, segments)
    print(f"The file has been split into {segments} segments.")

if __name__ == "__main__":
    main()

