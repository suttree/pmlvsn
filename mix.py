import os
import subprocess
import tempfile

# Function to get the list of video and image files in the current directory
def get_media_files():
    video_extensions = (".mp4", ".avi", ".mov")
    image_extensions = (".jpg", ".jpeg", ".png")
    
    video_files = [f for f in os.listdir(".") if f.lower().endswith(video_extensions)]
    image_files = [f for f in os.listdir(".") if f.lower().endswith(image_extensions)]
    
    return video_files, image_files

# Function to generate the filter_complex_script
def generate_filter_complex_script(video_files, image_files):
    filter_complex_script = ""
    
    for i, image_file in enumerate(image_files):
        filter_complex_script += f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[img{i}];"
    
    for i, video_file in enumerate(video_files):
        filter_complex_script += f"[{len(image_files) + i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[vid{i}];"
    
    filter_complex_script += "".join(f"[img{i}]" for i in range(len(image_files))) + "".join(f"[vid{i}]" for i in range(len(video_files)))
    filter_complex_script += f"concat=n={len(image_files) + len(video_files)}:v=1:a=0,format=yuv420p[v]"
    
    return filter_complex_script

# Get the list of video and image files
video_files, image_files = get_media_files()

# Generate the filter_complex_script
filter_complex_script = generate_filter_complex_script(video_files, image_files)

# Create a temporary file for the filter_complex_script
with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
    temp_file.write(filter_complex_script)
    filter_complex_file = temp_file.name

# Combine videos and images using FFmpeg
input_files = image_files + video_files
input_args = []
for i, file in enumerate(input_files):
    input_args.extend(["-i", file])

ffmpeg_cmd = ["ffmpeg"] + input_args + [
    "-filter_complex_script", filter_complex_file,
    "-map", "[v]",
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "18",
    "-movflags", "+faststart",
    "output.mp4"
]

subprocess.run(ffmpeg_cmd, check=True)

# Clean up the temporary file
os.unlink(filter_complex_file)