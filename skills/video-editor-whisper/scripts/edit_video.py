#!/usr/bin/env python3
"""
edit_video.py
Corta um vídeo mantendo apenas os intervalos de tempo indicados,
usando ffmpeg por baixo dos panos.

Uso:
    python edit_video.py input.mp4 cuts.json output.mp4

Formato esperado do cuts.json:
[
  {"start": 0.0, "end": 5.2},
  {"start": 8.1, "end": 20.0}
]
Cada item representa um trecho (em segundos) que deve
ser MANTIDO no vídeo final.
"""

import sys
import json
import subprocess
import os
import tempfile


def run(cmd):
    print("Rodando:", " ".join(cmd), file=sys.stderr)
    subprocess.run(cmd, check=True)


def cut_segment(input_path, start, end, out_path):
    duration = end - start
    run([
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", input_path,
        "-t", str(duration),
        "-c", "copy",
        out_path,
    ])


def concat_segments(segment_paths, output_path):
    with
