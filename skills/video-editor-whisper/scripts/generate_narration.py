#!/usr/bin/env python3
"""
generate_narration.py
Gera um audio de narracao em ingles usando edge-tts (voz neural
gratuita da Microsoft, sem precisar de chave de API).

Uso:
    python generate_narration.py narracao.txt narracao.mp3 [voz]

Vozes populares em ingles (para testar outras, rode: edge-tts --list-voices):
    en-US-AriaNeural    (feminina, EUA)
    en-US-GuyNeural     (masculina, EUA)
    en-GB-SoniaNeural   (feminina, Reino Unido)
    en-GB-RyanNeural    (masculina, Reino Unido)
"""

import sys
import asyncio


def main():
    if len(sys.argv) < 3:
        print("Uso: python generate_narration.py <texto.txt> <saida.mp3> [voz]", file=sys.stderr)
        sys.exit(1)

    text_path = sys.argv[1]
    output_path = sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else "en-US-AriaNeural"

    try:
        import edge_tts
    except ImportError:
        print("Erro: biblioteca 'edge-tts' nao instalada. Rode: pip install edge-tts", file=sys.stderr)
        sys.exit(1)

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("Erro: o arquivo de texto esta vazio.", file=sys.stderr)
        sys.exit(1)

    async def gerar():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)

    asyncio.run(gerar())

    print("Narracao salva em: " + output_path)


if __name__ == "__main__":
    main()
