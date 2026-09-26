#!/usr/bin/env python3
"""
apply_effects.py
Aplica cor mais viva no video e (opcional) mistura um overlay de
brilho/particulas usando "blend screen" (funciona com overlays de
fundo preto, como os baixados gratuitamente do Pixabay/Mixkit).

Uso:
    python apply_effects.py input.mp4 output.mp4 [overlay.mp4|nenhuma]
"""

import sys
import os
import subprocess


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

    base_filter = "eq=saturation=1.25:contrast=1.08"

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
