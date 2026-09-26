#!/usr/bin/env python3
"""
generate_narration.py
Gera um audio de narracao em ingles usando edge-tts (voz neural
gratuita da Microsoft). Tenta novamente automaticamente se o
servico falhar temporariamente.

Uso:
    python generate_narration.py narracao.txt narracao.mp3 [voz]
"""

import sys
import asyncio
import time

MAX_TENTATIVAS = 4
ESPERA_ENTRE_TENTATIVAS = 5  # segundos


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

    ultimo_erro = None
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            print("Tentativa " + str(tentativa) + " de " + str(MAX_TENTATIVAS) + "...", file=sys.stderr)
            asyncio.run(gerar())
            print("Narracao salva em: " + output_path)
            return
        except Exception as e:
            ultimo_erro = e
            print("Falhou nessa tentativa: " + str(e), file=sys.stderr)
            if tentativa < MAX_TENTATIVAS:
                print("Esperando " + str(ESPERA_ENTRE_TENTATIVAS) + "s antes de tentar de novo...", file=sys.stderr)
                time.sleep(ESPERA_ENTRE_TENTATIVAS)

    print("Erro: falhou apos " + str(MAX_TENTATIVAS) + " tentativas. Ultimo erro: " + str(ultimo_erro), file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
