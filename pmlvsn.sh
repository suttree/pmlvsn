ffmpeg -framerate 1/0.5 -pattern_type glob -i "px/img/orig/*.jpg" -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4
