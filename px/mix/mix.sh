#!/bin/bash

# Create temporary files
video_list=$(mktemp)
image_list=$(mktemp)
filter_complex_file=$(mktemp)

# Find video and image files in the current directory
find . -maxdepth 1 -type f \( -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mov" \) > "$video_list"
find . -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) > "$image_list"

# Generate the filter_complex_file content
echo "$(cat "$image_list" | awk '{printf "[%d:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[img%d]; ", NR-1, NR-1}')" > "$filter_complex_file"
echo "$(cat "$video_list" | awk '{printf "[%d:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[vid%d]; ", NR-1, NR-1}')" >> "$filter_complex_file"

echo "$(cat "$image_list" | awk '{printf "[img%d]", NR-1}') $(cat "$video_list" | awk '{printf "[vid%d]", NR-1}') concat=n=$(($(wc -l < "$image_list") + $(wc -l < "$video_list"))):v=1:a=0,format=yuv420p[v]" >> "$filter_complex_file"

# Combine videos and images using FFmpeg
ffmpeg -f concat -safe 0 -i "$video_list" -f image2 -i "$(cat "$image_list" | tr '\n' '|')" -filter_complex_script "$filter_complex_file" -map "[v]" -c:v libx264 -preset fast -crf 18 -movflags +faststart output.mp4

# Clean up temporary files
rm "$video_list" "$image_list" "$filter_complex_file"