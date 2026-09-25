#!/usr/bin/env python3
"""
generate_narration.py
Gera um audio de narracao em ingles usando a API da ElevenLabs.

Uso:
    python generate_narration.py narracao.txt narracao.mp3

Variaveis de ambiente necessarias:
    ELEVENLABS_API_KEY  - sua chave de API da ElevenLabs
    ELEVENLABS_VOICE_ID - o ID da voz (opcional, tem um padrao: Rachel)
"""

import sys
import os


def main():
    if len(sys.argv) < 3:
        print("Uso: python generate_narration.py <texto.txt> <saida.mp3>", file=sys.stderr)
        sys.exit(1)

    text_path = sys.argv[1]
    output_path = sys.argv[2]

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("Erro: variavel de ambiente ELEVENLABS_API_KEY nao definida.", file=sys.stderr)
        sys.exit(1)

    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

    try:
        import requests
    except ImportError:
        print("Erro: biblioteca 'requests' nao instalada. Rode: pip install requests", file=sys.stderr)
        sys.exit(1)

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("Erro: o arquivo de texto esta vazio.", file=sys.stderr)
        sys.exit(1)

    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("Erro na API da ElevenLabs: " + str(response.status_code) + " " + response.text, file=sys.stderr)
        sys.exit(1)

    with open(output_path, "wb") as f:
        f.write(response.content)

    print("Narracao salva em: " + output_path)


if __name__ == "__main__":
    main()
