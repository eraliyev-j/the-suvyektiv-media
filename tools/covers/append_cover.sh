#!/bin/bash
# append_cover.sh in.mp4 cover.jpg out.mp4 : adds a 0.5 s cover frame at the end (for IG thumbnailOffset)
in=$1; cov=$2; out=$3
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
has_a=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$in" | head -1)
if [ -n "$has_a" ]; then
ffmpeg -v error -y -i "$in" -loop 1 -t 0.5 -i "$cov" -f lavfi -t 0.5 -i anullsrc=r=48000:cl=stereo -filter_complex \
"[0:v]fps=30,scale=1080:1920,setsar=1,format=yuv420p[a];[1:v]fps=30,scale=1080:1920,setsar=1,format=yuv420p[b];[0:a]aresample=48000,aformat=channel_layouts=stereo[x];[2:a]aformat=channel_layouts=stereo[y];[a][x][b][y]concat=n=2:v=1:a=1[v][au]" \
-map "[v]" -map "[au]" -c:v libx264 -crf 21 -preset fast -c:a aac -b:a 192k -movflags +faststart "$out"
else
ffmpeg -v error -y -i "$in" -loop 1 -t 0.5 -i "$cov" -filter_complex "[0:v]fps=30,scale=1080:1920,setsar=1,format=yuv420p[a];[1:v]fps=30,scale=1080:1920,setsar=1,format=yuv420p[b];[a][b]concat=n=2:v=1:a=0[v]" -map "[v]" -c:v libx264 -crf 21 -preset fast -movflags +faststart "$out"
fi
echo "$out $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out") (was $d)"
