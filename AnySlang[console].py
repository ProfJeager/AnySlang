from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
import os

# Функция для извлечения аудио из видео
def extract_audio_from_video(video_file, audio_file):
    video = VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)

# Функция для преобразования аудио в текст
def transcribe_audio(audio_file, language_code):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file)
    audio.export("temp.wav", format="wav")
    
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language=language_code)
        except sr.UnknownValueError:
            text = "Не удалось распознать речь"
        except sr.RequestError as e:
            text = f"Ошибка сервиса распознавания речи; {e}"
    
    os.remove("temp.wav")
    return text

# Основной код
video_file = "C://Users/User/Downloads/IMG_6267.MOV"  # Укажите путь к вашему видеофайлу
audio_file = "extracted_audio.wav"

# Список поддерживаемых языков и их кодов
supported_languages = {
    "Английский": "en-US",
    "Русский": "ru-RU",
    "Испанский": "es-ES",
    "Французский": "fr-FR",
    "Немецкий": "de-DE",
    "Узбекский": "uz-UZ",
    # Добавьте другие языки по мере необходимости
}

# Запрос языка у пользователя
print("Выберите язык видео из списка:")
for i, (language, code) in enumerate(supported_languages.items(), start=1):
    print(f"{i}. {language}")
choice = int(input("Введите номер выбранного языка: ")) - 1

if 0 <= choice < len(supported_languages):
    selected_language = list(supported_languages.values())[choice]
else:
    print("Неверный выбор. Использование языка по умолчанию (английский).")
    selected_language = "en-US"

extract_audio_from_video(video_file, audio_file)
text = transcribe_audio(audio_file, selected_language)

print("Текст из видео:\n", text)
