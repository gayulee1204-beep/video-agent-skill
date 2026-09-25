#!/usr/bin/env python3
"""
generate_narration.py
Gera um arquivo de audio (mp3) com narracao a partir de um texto,
usando Google Text-to-Speech (gTTS), que e gratuito.

Uso:
    python generate_narration.py narracao.txt narracao.mp3
"""

import sys


def main():
    if len(sys.argv) < 3:
        print("Uso: python generate_narration.py <texto.txt> <saida.mp3>", file=sys.stderr)
        sys.exit(1)

    text_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        from gtts import gTTS
    except ImportError:
        print("Erro: biblioteca 'gtts' nao instalada. Rode: pip install gTTS", file=sys.stderr)
        sys.exit(1)

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("Erro: o arquivo de texto esta vazio.", file=sys.stderr)
        sys.exit(1)

    tts = gTTS(text=text, lang="pt")
    tts.save(output_path)

    print("Narracao salva em: " + output_path)


if __name__ == "__main__":
    main()
