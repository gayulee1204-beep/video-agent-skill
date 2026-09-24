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
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as f:
        list_path = f.name
        for path in segment_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")

    run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        output_path,
    ])

    os.remove(list_path)


def main():
    if len(sys.argv) < 4:
        print(
            "Uso: python edit_video.py <input.mp4> <cuts.json> <output.mp4>",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path, cuts_path, output_path = sys.argv[1:4]

    with open(cuts_path, "r", encoding="utf-8") as f:
        cuts = json.load(f)

    if not cuts:
        print("Nenhum corte informado em cuts.json", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp_dir:
        segment_paths = []
        for i, cut in enumerate(cuts):
            start = float(cut["start"])
            end = float(cut["end"])
            seg_path = os.path.join(tmp_dir, f"segment_{i:03d}.mp4")
            cut_segment(input_path, start, end, seg_path)
            segment_paths.append(seg_path)

        concat_segments(segment_paths, output_path)

    print(f"Vídeo final salvo em: {output_path}")


if __name__ == "__main__":
    main()
