#!/usr/bin/env python3
"""
generate_narration.py
Gera um audio de narracao usando Piper TTS (motor offline, sem
depender de nenhum servidor externo instavel).

Uso:
    python generate_narration.py narracao.txt narracao.wav modelo.onnx
"""

import sys
import subprocess


def main():
    if len(sys.argv) < 4:
        print("Uso: python generate_narration.py <texto.txt> <saida.wav> <modelo.onnx>", file=sys.stderr)
        sys.exit(1)

    text_path = sys.argv[1]
    output_path = sys.argv[2]
    model_path = sys.argv[3]

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("Erro: o arquivo de texto esta vazio.", file=sys.stderr)
        sys.exit(1)

    cmd = ["piper", "--model", model_path, "--output_file", output_path]
    print("Rodando:", " ".join(cmd), file=sys.stderr)
    subprocess.run(cmd, input=text, text=True, check=True)

    print("Narracao salva em: " + output_path)


if __name__ == "__main__":
    main()
