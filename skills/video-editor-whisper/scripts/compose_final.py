#!/usr/bin/env python3
"""
compose_final.py
Junta tudo: substitui o audio do video pela narracao (misturada com
musica de fundo, se houver) e queima as legendas no video.

Uso:
    python compose_final.py video.mp4 narracao.mp3 musica.mp3 legendas.srt final.mp4

Se nao tiver musica, passe a palavra "nenhuma" no lugar do caminho da musica.
"""

import sys
import subprocess
import os


def run(cmd):
    print("Rodando:", " ".join(cmd), file=sys.stderr)
    subprocess.run(cmd, check=True)


def main():
    if len(sys.argv) < 6:
        print("Uso: python compose_final.py <video.mp4> <narracao.mp3> <musica.mp3|nenhuma> <legendas.srt> <final.mp4>", file=sys.stderr)
        sys.exit(1)

    video_path = sys.argv[1]
    narration_path = sys.argv[2]
    music_path = sys.argv[3]
    srt_path = sys.argv[4]
    final_path = sys.argv[5]

    mixed_audio_path = "mixed_audio.mp3"

    if music_path != "nenhuma" and os.path.exists(music_path):
        run([
            "ffmpeg", "-y",
            "-i", narration_path,
            "-i", music_path,
            "-filter_complex",
            "[1:a]volume=0.15[music];[0:a][music]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "[aout]",
            mixed_audio_path,
        ])
    else:
        mixed_audio_path = narration_path

    run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", mixed_audio_path,
        "-vf", "subtitles=" + srt_path,
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        final_path,
    ])

    print("Video final salvo em: " + final_path)


if __name__ == "__main__":
    main()
