---
name: video-editor-whisper
description: Transcreve o áudio de vídeos usando Whisper e edita o vídeo automaticamente (corta silêncios, remove erros de fala, gera legendas). Use esta skill sempre que o usuário pedir para editar, cortar, legendar ou produzir um vídeo a partir de um arquivo de vídeo bruto.
---

# Video Editor com Whisper

Esta skill transforma um vídeo bruto em um vídeo editado, usando transcrição de áudio para decidir os cortes.

## Quando usar

Use esta skill quando o usuário:
- Enviar um arquivo de vídeo e pedir para "editar", "cortar", "legendar" ou "produzir" o vídeo
- Pedir para remover silêncios, gaguejos ou partes erradas de uma gravação
- Pedir para gerar legendas a partir de um vídeo

## Como funciona (passo a passo)

1. **Extrair o áudio do vídeo**
   Rode o comando ffmpeg para extrair o áudio em formato wav:

ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav


2. **Transcrever o áudio com Whisper**
   Rode o script `scripts/transcribe.py` passando o arquivo de áudio.
   Ele retorna um JSON com o texto falado e os timestamps de cada trecho.

python scripts/transcribe.py audio.wav > transcript.json


3. **Analisar a transcrição**
   Leia o `transcript.json` e identifique:
   - Trechos de silêncio longos (sem fala)
   - Repetições, gaguejos ou "ãhh", "tipo assim" em excesso
   - Pausas maiores que 1.5 segundos entre frases

4. **Gerar a lista de cortes**
   Monte uma lista de intervalos de tempo (início/fim) que devem ficar no vídeo final, excluindo os trechos identificados no passo 3.

5. **Editar o vídeo**
   Rode o script `scripts/edit_video.py` passando o vídeo original e a lista de cortes.
   Ele usa ffmpeg internamente para gerar o vídeo final:

python scripts/edit_video.py input.mp4 cuts.json output.mp4


6. **(Opcional) Gerar legendas**
   Converta o `transcript.json` para o formato `.srt` e informe ao usuário como incorporar as legendas com ffmpeg:

ffmpeg -i output.mp4 -vf subtitles=legendas.srt final_com_legenda.mp4


## Observações importantes

- Sempre confirme com o usuário antes de sobrescrever o vídeo original.
- Se o vídeo for muito longo, processe em partes para evitar arquivos temporários gigantes.
- Nunca invente falas na transcrição — use exatamente o que o Whisper retornou.
