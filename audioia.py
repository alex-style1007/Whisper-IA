from moviepy.editor import VideoFileClip
import whisper
import pandas as pd

# Ruta al archivo de audio MP4 que deseas convertir
input_mp4_file = "Audio.mp4"

# Ruta al archivo de salida en formato WAV
output_wav_file = "Audio.wav"

# Carga el archivo MP4 y extrae el audio
video_clip = VideoFileClip(input_mp4_file)
audio = video_clip.audio

# Exporta el audio a un archivo WAV
audio.write_audiofile(output_wav_file, codec="pcm_s16le")

print(f"El archivo MP4 se ha convertido a {output_wav_file}")




model = whisper.load_model("medium")
result = model.transcribe("Audio.mp4")
print(result["text"])

result['segments']

pausas = []
segmentos = result['segments']
for i in range(1, len(segmentos)):
    duracion_pausa = segmentos[i]['start'] - segmentos[i - 1]['end']
    if duracion_pausa > 0.3:  # Consideramos una pausa de más de 1 segundo
        pausas.append(i)

# Agrupar segmentos de texto por hablante
hablantes = []
inicio_segmento = 0
for pausa in pausas:
    hablantes.append(segmentos[inicio_segmento:pausa])
    inicio_segmento = pausa
hablantes.append(segmentos[inicio_segmento:])


etiqueta_actual = "Persona 1"
etiquetas = []
texto = []
for hablante in hablantes:
    for segmento in hablante:
        etiquetas.append(etiqueta_actual)
        texto.append(segmento['text'])
        etiqueta_actual = "Persona 1" if etiqueta_actual == "Persona 2" else "Persona 2"

# Crear un DataFrame de Pandas
df = pd.DataFrame({'Hablante': etiquetas, 'Texto': texto})
print(df)
