#!/usr/bin/env python3
"""
apply_effects.py
Aplica efeitos visuais automaticos: cores mais vivas, vinheta,
fade de entrada/saida, e (opcional) um overlay de brilho/particulas
misturado com "blend screen" (funciona com overlays de fundo preto,
como os baixados gratuitamente do Pixabay/Mixkit).

Uso:
    python apply_effects.py input.mp4 output.mp4 [overlay.mp4|nenhuma]
"""

import sys
import os
import subprocess


def run(cmd):
    print("Rodando:", " ".join(cmd), file=sys.stderr)
    subprocess.run(cmd, check=True)


def get_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def main():
    if len(sys.argv) < 3:
        print("Uso: python apply_effects.py <input.mp4> <output.mp4> [overlay.mp4|nenhuma]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    overlay_path = sys.argv[3] if len(sys.argv) > 3 else "nenhuma"

    duration = get_duration(input_path)
    fade_duration = 0.5
    fade_out_start = max(0.0, duration - fade_duration)

    base_filter = (
        "eq=saturation=1.25:contrast=1.08,"
        "vignette,"
        "fade=t=in:st=0:d=" + str(fade_duration) + ","
        "fade=t=out:st=" + str(round(fade_out_start, 2)) + ":d=" + str(fade_duration)
    )

    if overlay_path != "nenhuma" and os.path.exists(overlay_path):
        filter_complex = (
            "[0:v]" + base_filter + "[base];"
            "[1:v]loop=loop=-1:size=9999[ov1];"
            "[ov1][base]scale2ref=w=iw:h=ih[ov2][base2];"
            "[base2][ov2]blend=all_mode=screen:shortest=1,format=yuv420p[outv]"
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
        print("Video com efeitos e brilho salvo em: " + output_path)
        return

    run([
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", base_filter,
        "-c:v", "libx264",
        "-an",
        output_path,
    ])
    print("Video com efeitos salvo em: " + output_path)


if __name__ == "__main__":
    main()
