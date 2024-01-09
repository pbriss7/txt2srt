from pydub import AudioSegment
import re

def milliseconds_to_srt_time(milliseconds):
    """Conversion des millisecondes en format srt"""
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def sentence_tokenize_with_periods(text):
    """Séparation des phrases"""
    sentences = re.split(r'(?<=\.)\s', text)
    return [sentence.strip() for sentence in sentences if sentence]

def generate_srt(sentences, duration_per_group):
    """Génère des sous-titres srt toutes les 10 phrases (ajuster au besoin)."""
    srt_content = []
    group_size = 10
    start_time = 0

    for i in range(0, len(sentences), group_size):
        end_time = start_time + duration_per_group
        group_text = ' '.join(sentences[i:i+group_size])
        srt_entry = f"{i//group_size+1}\n{milliseconds_to_srt_time(start_time)} --> {milliseconds_to_srt_time(end_time)}\n{group_text}\n\n"
        srt_content.append(srt_entry)
        start_time = end_time + 1

    return "".join(srt_content)

# Chargement du texte (remplacer *** par le chemin)
text_file_path = '***.txt'
with open(text_file_path, 'r') as file:
    text = file.read()

# Chargement du fichier mp3 et calcul de sa durée (remplacer *** par le chemin)
audio_file_path = '***.mp3'
audio = AudioSegment.from_mp3(audio_file_path)
audio_duration_milliseconds = len(audio)

# Segmentation du texte
sentences = sentence_tokenize_with_periods(text)

# Calcul du temps moyen toutes les 10 phrases (ajuster au besoin)
duration_per_group = audio_duration_milliseconds // (len(sentences) // 10)

# Création du contenu srt
srt_content = generate_srt(sentences, duration_per_group)

# Sauvegarde du fichier .srt (ajuster le chemin au besoin)
srt_file_path = 'subtitles.srt'
with open(srt_file_path, 'w') as file:
    file.write(srt_content)
