#!/usr/bin/env python3
"""
analyze_transcript.py
Lê a transcrição gerada pelo Whisper (transcript.json) e decide
automaticamente quais trechos do vídeo devem ser mantidos, usando
regras simples (sem inteligência artificial):

- Remove silêncios maiores que um limite (padrão: 1.5 segundos)
- Junta trechos de fala próximos
- Gera o arquivo cuts.json pronto para o edit_video.py

Uso:
    python analyze_transcript.py transcript.json cuts.json
    python analyze_transcript.py transcript.json cuts.json --min-gap 2.0 --padding 0.3
"""

import sys
import json
import argparse


def build_cuts(segments, min_gap=1.5, padding=0.2):
    if not segments:
        return []

    cuts = []
    current_start = max(0.0, segments[0]["start"] - padding)
    current_end = segments[0]["end"] + padding

    for seg in segments[1:]:
        gap = seg["start"] - current_end
        if gap > min_gap:
            # Silêncio grande encontrado: fecha o trecho atual e começa um novo
            cuts.append({
                "start": round(current_start, 2),
                "end": round(current_end, 2),
            })
            current_start = max(0.0, seg["start"] - padding)
            current_end = seg["end"] + padding
        else:
            # Silêncio pequeno: continua o mesmo trecho
            current_end = seg["end"] + padding

    cuts.append({
        "start": round(current_start, 2),
        "end": round(current_end, 2),
    })
    return cuts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript_path")
    parser.add_argument("cuts_path")
    parser.add_argument(
        "--min-gap", type=float, default=1.5,
        help="Silêncio mínimo (em segundos) para considerar um corte"
    )
    parser.add_argument(
        "--padding", type=float, default=0.2,
        help="Margem (em segundos) deixada antes/depois de cada trecho de fala"
    )
    args = parser.parse_args()

    with open(args.transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    cuts = build_cuts(segments, min_gap=args.min_gap, padding=args.padding)

    with open(args.cuts_path, "w", encoding="utf-8") as f:
        json.dump(cuts, f, ensure_ascii=False, indent=2)

    print(f"{len(cuts)} trecho(s) de fala encontrados. Cortes salvos em {args.cuts_path}")


if __name__ == "__main__":
    main()
