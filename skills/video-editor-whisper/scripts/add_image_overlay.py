#!/usr/bin/env python3
"""
add_image_overlay.py
Sobrepoe uma imagem na METADE DE BAIXO da tela, aparecendo apenas
nos ultimos N segundos do video.

Uso:
    python add_image_overlay.py video.mp4 imagem.png saida.mp4 [segundos]
"""

import sys
import os
import subprocess
import json

DEFAULT_SECONDS = 5


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
    if len(sys.argv) < 4:
        print("Uso: python add_image_overlay.py <video.mp4> <imagem.png> <saida.mp4> [segundos]", file=sys.stderr)
        sys.exit(1)

    video_path = sys.argv[1]
    image_path = sys.argv[2]
    output_path = sys.argv[3]
    seconds = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_SECONDS

    if image_path == "nenhuma" or not os.path.exists(image_path):
        run(["ffmpeg", "-y", "-i", video_path, "-c", "copy", output_path])
        print("Sem imagem: video copiado sem alteracoes para " + output_path)
        return

    duration = get_duration(video_path)
    width, height = get_dimensions(video_path)
    img_w, img_h = get_dimensions(image_path)

    half_height = height // 2
    start_time = max(0.0, duration - seconds)

    # Calcula o tamanho da imagem para caber na metade de baixo,
    # mantendo a proporcao (sem usar o filtro pad).
    factor = min(width / img_w, half_height / img_h)
    new_w = max(2, int(img_w * factor) // 2 * 2)
    new_h = max(2, int(img_h * factor) // 2 * 2)
    new_w = min(new_w, width)
    new_h = min(new_h, half_height)

    # Centraliza a imagem dentro da metade de baixo
    pos_x = (width - new_w) // 2
    pos_y = half_height + (half_height - new_h) // 2

    filter_complex = (
        "[1:v]setsar=1,format=rgba,"
        "scale=" + str(new_w) + ":" + str(new_h) + "[img];"
        "[0:v][img]overlay=x=" + str(pos_x) + ":y=" + str(pos_y) +
        ":enable='gte(t\\," + str(round(start_time, 2)) + ")'[outv]"
    )

    run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", image_path,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_path,
    ])

    print("Video com imagem sobreposta salvo em: " + output_path)


if __name__ == "__main__":
    main()
