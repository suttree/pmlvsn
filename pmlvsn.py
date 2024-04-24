import os
import subprocess

# Set the directory containing the .MOV files
directory = "./"

# Get a list of all .MOV files in the directory
mov_files = [file for file in os.listdir(directory) if file.endswith(".MOV")]

# Sort the files alphabetically (assuming they are named in the desired order)
mov_files.sort()

# Create a temporary file to store the file list
temp_file = "temp_file_list.txt"

# Write the file paths to the temporary file
with open(temp_file, "w") as file:
    for mov_file in mov_files:
        file_path = os.path.join(directory, mov_file)
        file.write(f"file '{file_path}'\n")

# Set the output file name and path
output_file = "combined_video.MOV"
output_path = os.path.join(directory, output_file)

# Use FFmpeg to concatenate the videos
subprocess.call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', temp_file, '-c', 'copy', output_path])

# Remove the temporary file
os.remove(temp_file)
