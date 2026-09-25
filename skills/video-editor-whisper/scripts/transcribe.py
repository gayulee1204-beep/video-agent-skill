#!/usr/bin/env python3
"""
transcribe.py
Transcreve um arquivo de audio usando Whisper e salva o resultado
(com timestamps por palavra) diretamente em um arquivo JSON.

Uso:
    python transcribe.py audio.wav transcript.json [idioma]
"""

import sys
import json


def main():
    if len(sys.argv) < 3:
        print("Uso: python transcribe.py <audio.wav> <saida.json> [idioma]", file=sys.stderr)
        sys.exit(1)

    audio_path = sys.argv[1]
    output_path = sys.argv[2]
    language = sys.argv[3] if len(sys.argv) > 3 else None

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

    kwargs = {"verbose": False, "word_timestamps": True}
    if language:
        kwargs["language"] = language

    result = model.transcribe(audio_path, **kwargs)

    segments_out = []
    for seg in result.get("segments", []):
        words_out = []
        for w in seg.get("words", []):
            word_text = (w.get("word") or "").strip()
            if word_text:
                words_out.append({
                    "start": w["start"],
                    "end": w["end"],
                    "word": word_text,
                })
        segments_out.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
            "words": words_out,
        })

    output = {
        "text": result.get("text", ""),
        "segments": segments_out,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("Transcricao salva em: " + output_path)


if __name__ == "__main__":
    main()
