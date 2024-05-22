# Whisper-IA
Para iniciar sera importante ejecutar los siguientes instaladores:
```python
!pip install moviepy
```

```python
!pip install -U openai-whisper
```

```python
!sudo apt update && sudo apt install ffmpeg
```

## Contexto General del Proyecto
El objetivo de este proyecto es desarrollar una herramienta que permite la extracción y transcripción de audio desde archivos de video en formato MP4. Utilizando técnicas avanzadas de procesamiento de audio y lenguaje natural, el proyecto se centra en convertir el contenido de audio en texto, identificar y segmentar las pausas en la conversación, y agrupar los segmentos transcritos por hablante. Finalmente, se organiza toda la información en un formato estructurado utilizando un DataFrame de Pandas, lo cual facilita su análisis y visualización.

Este proyecto tiene múltiples aplicaciones en diversas áreas, incluyendo:

1. Análisis de Conversaciones: Útil para estudiar patrones de diálogo, identificar pausas y turnos de habla, y analizar la dinámica de las conversaciones.
2. Transcripción Automática: Beneficioso para generar transcripciones automáticas de videos educativos, entrevistas, conferencias, y otros contenidos audiovisuales.
3. Mejora de Accesibilidad: Ayuda a crear contenido más accesible para personas con discapacidades auditivas mediante la generación de subtítulos precisos.
## Flujo de Trabajo del Proyecto
1. Importación de Bibliotecas:Se importan las bibliotecas necesarias para la manipulación de video, transcripción de audio y manejo de datos.
2. Extracción de Audio de un Video MP4: Se carga el archivo MP4, se extrae el audio y se convierte a formato WAV.
3. Transcripción del Audio con Whisper: Se utiliza el modelo Whisper para transcribir el contenido del audio, generando un texto transcrito y segmentado.
4. Identificación de Pausas entre Segmentos: Se identifican las pausas significativas entre los segmentos de habla para agrupar los fragmentos de conversación.
5. Agrupación de Segmentos por Hablante:Se agrupan los segmentos de texto por hablante, alternando entre "Persona 1" y "Persona 2".
6. Creación de un DataFrame de Pandas:Se organiza la información en un DataFrame con las etiquetas de hablante y los textos transcritos para facilitar el análisis y la visualización.

### Importación de Bibliotecas
Primero, importamos las bibliotecas necesarias para la manipulación de video, transcripción de audio y manejo de datos.

```python
from moviepy.editor import VideoFileClip
import whisper
import pandas as pd
```

### Extracción de Audio de un Video MP4
Definimos las rutas de los archivos de entrada y salida, cargamos el archivo MP4 y extraemos el audio. Luego, exportamos el audio a un archivo WAV.
```python
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
```
### Transcripción del Audio con Whisper
Cargamos el modelo de Whisper y transcribimos el contenido del archivo MP4. El resultado contiene el texto transcrito y los segmentos de audio. https://openai.com/index/whisper/
```python
model = whisper.load_model("medium")
result = model.transcribe("Audio.mp4")
print(result["text"])
result['segments']
```

### Identificación de Pausas entre Segmentos
Identificamos las pausas significativas entre los segmentos de habla, que se consideran como pausas de más de 0.3 segundos.
```python
pausas = []
segmentos = result['segments']
for i in range(1, len(segmentos)):
    duracion_pausa = segmentos[i]['start'] - segmentos[i - 1]['end']
    if duracion_pausa > 0.3:  # Consideramos una pausa de más de 1 segundo
        pausas.append(i)
```
### Agrupación de Segmentos por Hablante
Agrupamos los segmentos de texto por hablante, alternando entre "Persona 1" y "Persona 2".
```python
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
```

### Creación de un DataFrame de Pandas
Creamos un DataFrame de Pandas con las etiquetas de hablante y los textos transcritos, y lo imprimimos.
```python
# Crear un DataFrame de Pandas
df = pd.DataFrame({'Hablante': etiquetas, 'Texto': texto})
print(df)
```
