#!/usr/bin/env python3
"""
apply_effects.py
Mistura um overlay de brilho/particulas SOMENTE nos primeiros 3
segundos do video, usando chroma key (torna o fundo escuro do
overlay transparente de verdade, em vez de misturar cor).
Nao altera a cor original do video base.

Uso:
    python apply_effects.py input.mp4 output.mp4 [overlay.mp4|nenhuma]
"""

import sys
import os
import subprocess

EFFECT_SECONDS = 3


def run(cmd):
    print("Rodando:", " ".join(cmd), file=sys.stderr)
    subprocess.run(cmd, check=True)


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

    filter_complex = (
        "[1:v]trim=duration=" + str(EFFECT_SECONDS) + ",setpts=PTS-STARTPTS,"
        "colorkey=0x000000:0.25:0.15[ov_key];"
        "[ov_key][0:v]scale2ref=w=iw:h=ih[ov2][base2];"
        "[base2][ov2]overlay=eof_action=pass,format=yuv420p[outv]"
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
