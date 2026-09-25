#!/usr/bin/env python3
"""
make_srt.py
Converte um transcript.json (gerado pelo transcribe.py) em um arquivo
de legendas no formato .srt.

Uso:
    python make_srt.py transcript.json legendas.srt
"""

import sys
import json


def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return "%02d:%02d:%02d,%03d" % (hours, minutes, secs, millis)


def main():
    if len(sys.argv) < 3:
        print("Uso: python make_srt.py <transcript.json> <legendas.srt>", file=sys.stderr)
        sys.exit(1)

    transcript_path = sys.argv[1]
    srt_path = sys.argv[2]

    with open(transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])

    lines = []
    for i, seg in enumerate(segments, start=1):
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        text = seg["text"].strip()
        lines.append(str(i))
        lines.append(start + " --> " + end)
        lines.append(text)
        lines.append("")

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Legendas salvas em: " + srt_path)


if __name__ == "__main__":
    main()
