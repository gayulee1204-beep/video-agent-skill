#!/usr/bin/env python3
"""
transcribe.py
Transcreve um arquivo de audio usando Whisper e salva o resultado
diretamente em um arquivo JSON.

Uso:
    python transcribe.py audio.wav transcript.json
"""

import sys
import json


def main():
    if len(sys.argv) < 3:
        print("Uso: python transcribe.py <audio.wav> <saida.json>", file=sys.stderr)
        sys.exit(1)

    audio_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        import whisper
    except ImportError:
        print(
            "Erro: a biblioteca 'whisper' nao esta instalada. "
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

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Transcricao salva em: {output_path}")


if __name__ == "__main__":
    main()
