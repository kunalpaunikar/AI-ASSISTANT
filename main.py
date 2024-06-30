import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from gtts import gTTS
import pygame
import os
from pytube import Search

# Initialization
recognizer = sr.Recognizer()
engine = pyttsx3.init()
pygame.mixer.init()
newsapi = "959e23c7725a412ba357b476954e6239"
music = {}

def speak(text):
    tts = gTTS(text)
    tts.save('speech.mp3')
    pygame.mixer.music.load('speech.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("speech.mp3")

def open_url(url):
    webbrowser.open(url)

def play_music_from_youtube(song):
    try:
        query = f"{song} official audio"
        video = Search(query).results[0]
        open_url(video.watch_url)
    except Exception as e:
        print(f"Error playing music from YouTube: {e}")
        speak("Failed to play the music from YouTube.")

def process_command(command):
    if "open" in command:
        open_url(f"https://{command.replace('open', '').strip()}.com")
    elif command.startswith("play"):
        song = command.split(" ", 1)[1]
        if song in music:
            open_url(music[song])
        else:
            play_music_from_youtube(song)
    elif "news" in command:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            r.raise_for_status()
            articles = r.json().get('articles', [])
            for article in articles:
                speak(article['title'])
        except requests.RequestException:
            speak("Failed to retrieve news.")
    elif "play music" in command:
        play_music_from_youtube(command.replace("play music ", "").strip())

if __name__ == "__main__":
    speak("Initializing alexa...")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for the wake word...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
                word = recognizer.recognize_google(audio)
                if word.lower() == "alexa":
                    speak("Yes?")
                    print("Listening for command...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio).lower()
                    process_command(command)
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error: {e}")
