#!/usr/bin/env python3
"""
transcribe.py
Transcreve um arquivo de áudio usando Whisper e imprime o resultado em JSON.

Uso:
    python transcribe.py audio.wav > transcript.json
"""

import sys
import json

def main():
    if len(sys.argv) < 2:
        print("Uso: python transcribe.py <arquivo_audio.wav>", file=sys.stderr)
        sys.exit(1)

    audio_path = sys.argv[1]

    try:
        import whisper
    except ImportError:
        print(
            "Erro: a biblioteca 'whisper' não está instalada. "
            "Rode: pip install openai-whisper",
            file=sys.stderr,
        )
        sys.exit(1)

    model = whisper.load_model("base")
    result = model.transcribe(audio_path, verbose=False)

    output = {
        "text": result.get("text", ""),
        "segments": [
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip(),
            }
            for seg in result.get("segments", [])
        ],
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
