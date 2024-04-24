# pmlvsn

## Python
python3 -m venv venv
venv/bin/pip3 install opencv-python
venv/bin/python3.12 pmlvsn.py


## cli

### Combine multiple images
ffmpeg -framerate 1/0.5 -pattern_type glob -i "px/img/orig/*.jpg" -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4


### Combine multiple videos
cd px/mov
printf "file '%s'\n" * > files.txt
<edit files.txt>
ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp4


### Both?
cd px/mix
printf "file '%s'\n" * > files.txt
<edit files.txt>
ffmpeg -f concat -safe 0 -i files.txt -c:v libx264 -r 30 -pix_fmt yuv420p copy output.mp4

### Compress video
ffmpeg -i input.mp4 -vcodec libx265 -crf 28 output.mp4