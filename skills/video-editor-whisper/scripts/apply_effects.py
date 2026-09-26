#!/usr/bin/env python3
"""
apply_effects.py
Mistura um overlay de brilho/particulas no INICIO do video (uma unica
vez, depois desaparece), usando "blend screen" (funciona com overlays
de fundo preto, como os baixados gratuitamente do Pixabay/Mixkit).
Nao altera a cor original do video.

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

    if overlay_path == "nenhuma" or not os.path.exists(overlay_path):
        # Sem brilho: so copia o video sem mexer em nada.
        run([
            "ffmpeg", "-y",
            "-i", input_path,
            "-c:v", "copy",
            "-an",
            output_path,
        ])
        print("Video salvo sem alteracoes em: " + output_path)
        return

    base_duration = get_duration(input_path)
    overlay_duration = get_duration(overlay_path)
    pad_duration = max(0.0, base_duration - overlay_duration)

    # tpad completa o overlay com quadros PRETOS depois que ele termina,
    # entao ele toca uma unica vez no comeco e some (preto = invisivel
    # no modo de mistura "screen").
    filter_complex = (
        "[1:v]tpad=stop_mode=add:stop_duration=" + str(round(pad_duration, 2)) + ":color=black[ov_pad];"
        "[ov_pad][0:v]scale2ref=w=iw:h=ih[ov2][base2];"
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
    print("Video com brilho (uma vez no inicio) salvo em: " + output_path)


if __name__ == "__main__":
    main()
