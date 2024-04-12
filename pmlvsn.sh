#ffmpeg -framerate 1/0.5 -pattern_type glob -i "px/img/orig/*.jpg" -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4
ffmpeg -framerate 1/0.5 -pattern_type -pattern_type glob -i "px/mov/*.mov" -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" -c:v libx264 -r 30 -movflags +faststart output.mp4
