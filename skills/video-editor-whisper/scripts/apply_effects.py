#!/usr/bin/env python3
"""
apply_effects.py
Mistura um overlay de brilho/particulas SOMENTE nos primeiros 3
segundos do video, usando chroma key (fundo escuro transparente).
O overlay e redimensionado mantendo a proporcao original (cortando
as bordas em vez de esticar), para nao ficar distorcido quando o
video de brilho tem uma proporcao diferente do video base (ex: um
overlay horizontal 16:9 usado num video vertical 9:16).

Uso:
    python apply_effects.py input.mp4 output.mp4 [overlay.mp4|nenhuma]
"""

import sys
import os
import subprocess
import json

EFFECT_SECONDS = 3


def run(cmd):
    print("Rodando:", " ".join(cmd), file=sys.stderr)
    subprocess.run(cmd, check=True)


def get_dimensions(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-of", "json", path],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(result.stdout)
    stream = data["streams"][0]
    return int(stream["width"]), int(stream["height"])


def main():
    if len(sys.argv) < 3:
        print("Uso: python apply_effects.py <input.mp4> <output.mp4> [overlay.mp4|nenhuma]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    overlay_path = sys.argv[3] if len(sys.argv) > 3 else "nenhuma"

    if overlay_path == "nenhuma" or not os.path.exists(overlay_path):
        run([
            "ffmpeg", "-y",
            "-i", input_path,
            "-c:v", "copy",
            "-an",
            output_path,
        ])
        print("Video salvo sem alteracoes em: " + output_path)
        return

    width, height = get_dimensions(input_path)

    filter_complex = (
        "[1:v]trim=duration=" + str(EFFECT_SECONDS) + ",setpts=PTS-STARTPTS,"
        "scale=w=" + str(width) + ":h=" + str(height) + ":force_original_aspect_ratio=increase,"
        "crop=" + str(width) + ":" + str(height) + ","
        "colorkey=0x000000:0.25:0.15[ov_key];"
        "[0:v][ov_key]overlay=eof_action=pass,format=yuv420p[outv]"
    )

    run([
        "ffmpeg", "-y",
        "-i", input_path,
        "-i", overlay_path,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-c:v", "libx264",
        "-an",
        output_path,
    ])

    print("Video com brilho nos primeiros " + str(EFFECT_SECONDS) + "s salvo em: " + output_path)


if __name__ == "__main__":
    main()
