---
name: video-montaj
description: Edit (montaj) raw videos with ffmpeg following the user's guidance-book.md — hook, cuts, subtitles, color, music. Use when the user says "montaj qil", "guidance book bo'yicha", or asks to edit/cut videos in a folder that has a guidance-book.md.
---

# Video montaj (ffmpeg + guidance book)

The user's style rules live in `guidance-book.md` in the current folder. That file is the source of truth: every decision (hook length, cut pace, subtitle look, color, music level, output format) comes from it. If a rule is missing or still a `[placeholder]`, use the default noted here and tell the user which defaults you used.

## 0. Setup checks

- Read `guidance-book.md` fully before touching any video. If it doesn't exist, stop and ask for it.
- Check ffmpeg with `ffmpeg -version`. If it's not on PATH (new installs only show up after a shell restart), look under `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\*\bin\` and use the full path.
- Folders: source clips go in `raw footage/`, style examples in `references/`, finished files in `exports/`. If the clips are somewhere else, work with them where they are. Never overwrite or delete a source clip.
- Put intermediate files in a `_work/` folder (or your scratchpad), not next to the sources.

## 1. Inspect

For each clip, run `ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of json "<clip>"`.
Write a short inventory: name, duration, resolution, fps, audio yes/no. If the clips have different resolutions or fps, normalize them to the target from the guidance book (default 1080x1920, 30 fps for vertical).

## 2. Plan before rendering

Write an edit plan and show it to the user before the final render:
- **Hook (first 1–3 s)**: which moment opens the video and why, per the guidance book's hook rules.
- **Cuts**: find dead air with `ffmpeg -i clip -af silencedetect=noise=-30dB:d=0.5 -f null -`, using the threshold and minimum pause from the guidance book. List the keep segments as timestamps.
- **Order** of segments, **subtitles**, **color**, **music**, **output**.

If the guidance book says to proceed without approval, skip the wait.

## 3. Build

1. **Trim** each keep segment and re-encode it to a uniform intermediate (`-c:v libx264 -crf 18 -preset fast -c:a aac -ar 48000`). Frame-accurate cuts need a re-encode; don't use `-c copy` for cuts.
2. **Reframe** to the target aspect: `scale=...:force_original_aspect_ratio=increase,crop=W:H` (crop to fill), or pad it if the guidance book says so.
3. **Concatenate** with the concat demuxer (`-f concat -safe 0 -i list.txt`). For transitions, use `xfade`/`acrossfade` only if the guidance book asks for them; the default is hard cuts.
4. **Color**: apply the guidance book's look with `eq=contrast=..:saturation=..:brightness=..`, `colorbalance`, or `lut3d=file.cube` if it gives a LUT in `references/`.
5. **Audio**: `loudnorm=I=-14:TP=-1:LRA=11` on the voice. If there's music, mix it under the voice with `sidechaincompress` or a fixed volume (default music at -20 dB relative to the voice), and fade it out over the last 1–2 s.
6. **Subtitles**:
   - Transcribe with ffmpeg's `whisper` filter if this build has it (`ffmpeg -filters | grep whisper`) and a model file is available; otherwise ask the user for an `.srt`, or use a Whisper CLI if one is installed.
   - Check the transcript for mistakes in names and terms before burning it in.
   - Style it per the guidance book with `subtitles=subs.srt:force_style='FontName=..,FontSize=..,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Alignment=2,MarginV=..'`. For word-by-word or highlighted captions, generate an `.ass` file.
   - On Windows, escape the path inside the filter: `subtitles='C\:/path/subs.srt'`.
7. **Export** to `exports/<name>_v1.mp4` (bump the version on each re-render, never overwrite): `-c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart`, unless the guidance book says otherwise.

## 4. Verify and report

- Run `ffprobe` on the export: check duration, resolution, fps and that it has audio.
- Grab a few frames (`-ss <t> -frames:v 1 check_<t>.png`), at least from the hook, the middle and the end, and look at them to check the framing, subtitles and color.
- Tell the user: output path, final duration, which guidance-book rules you applied, which defaults you filled in, and anything you couldn't do.

## Rules

- Never modify or delete the source footage.
- Prefer one clear ffmpeg command per step over one giant filtergraph, so a failed step can be rerun on its own.
- Long renders: run them in the background and report when they finish.
- Keep the commands you used in `_work/commands.txt` so the edit can be reproduced.
