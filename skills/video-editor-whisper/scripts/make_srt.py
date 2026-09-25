#!/usr/bin/env python3
"""
make_srt.py
Converte um transcript.json (com timestamps por palavra) em um
arquivo de legendas .srt com poucas palavras por vez.

Uso:
    python make_srt.py transcript.json legendas.srt [palavras_por_legenda]
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
        print("Uso: python make_srt.py <transcript.json> <legendas.srt> [palavras_por_legenda]", file=sys.stderr)
        sys.exit(1)

    transcript_path = sys.argv[1]
    srt_path = sys.argv[2]
    words_per_caption = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    with open(transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_words = []
    for seg in data.get("segments", []):
        for w in seg.get("words", []):
            all_words.append(w)

    lines = []
    counter = 0
    for i in range(0, len(all_words), words_per_caption):
        chunk = all_words[i:i + words_per_caption]
        if not chunk:
            continue
        counter += 1
        start = format_timestamp(chunk[0]["start"])
        end = format_timestamp(chunk[-1]["end"])
        text = " ".join(w["word"] for w in chunk)
        lines.append(str(counter))
        lines.append(start + " --> " + end)
        lines.append(text)
        lines.append("")

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Legendas salvas em: " + srt_path + " (" + str(counter) + " legendas)")


if __name__ == "__main__":
    main()
