# Module/SubtitleClipper.py

import pysrt
import ffmpeg
import json
from pathlib import Path

def extract_subtitles_by_time(srt_path, time_range, output_srt_path):
    subs = pysrt.open(srt_path)
    selected = []

    start_sec, end_sec = time_range
    for sub in subs:
        sub_start = sub.start.ordinal / 1000
        sub_end = sub.end.ordinal / 1000
        if sub_end >= start_sec and sub_start <= end_sec:
            sub.shift(seconds=-start_sec)
            selected.append(sub)

    for i, sub in enumerate(selected, 1):
        sub.index = i
    pysrt.SubRipFile(items=selected).save(output_srt_path, encoding='utf-8')


def burn_srt_to_video(input_video, input_srt, output_video):
    srt_posix = Path(input_srt).resolve().as_posix()
    ffmpeg.input(input_video).output(
        output_video,
        vf=f"subtitles={srt_posix}",
        vcodec='libx264',
        acodec='copy'
    ).run()



def process_clip_with_subtitles(full_srt_path, clip_video_path, time_json_path, output_srt_path, output_video_path):
    with open(time_json_path, 'r') as f:
        time_range = json.load(f)[0]
    start = float(time_range["start"])
    end = float(time_range["end"])

    extract_subtitles_by_time(full_srt_path, (start, end), output_srt_path)
    burn_srt_to_video(clip_video_path, output_srt_path, output_video_path)
