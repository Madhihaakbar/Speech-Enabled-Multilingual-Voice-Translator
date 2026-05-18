from tkinter import *
from tkinter import ttk, messagebox
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()

root = Tk()
root.title("AI Multilingual Voice Translator")
root.geometry("750x600")

Label(
    root,
    text="AI Multilingual Voice Translator",
    font=("Arial",20,"bold")
).pack(pady=10)

languages = GoogleTranslator().get_supported_languages(
    as_dict=True
)

language_names = sorted(
    [x.title() for x in languages.keys()]
)

# Input
Label(
    root,
    text="Input Language"
).pack()

input_lang = StringVar(value="English")

ttk.Combobox(
    root,
    textvariable=input_lang,
    values=language_names,
    width=35,
    state="readonly"
).pack(pady=5)

# Output
Label(
    root,
    text="Output Language"
).pack()

output_lang = StringVar(value="Tamil")

ttk.Combobox(
    root,
    textvariable=output_lang,
    values=language_names,
    width=35,
    state="readonly"
).pack(pady=5)

output = Text(
    root,
    width=75,
    height=15
)

output.pack(pady=15)

pygame.mixer.init()


def speak_translation(text, lang):

    try:

        tts = gTTS(
            text=text,
            lang=lang
        )

        file = "voice.mp3"

        tts.save(file)

        pygame.mixer.music.load(file)

        pygame.mixer.music.play()

    except:
        pass


def translate_voice():

    try:

        output.delete(
            "1.0",
            END
        )

        output.insert(
            END,
            "Listening...\n\n"
        )

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(
                source
            )

            audio = recognizer.listen(
                source,
                timeout=5
            )

        source_lang = input_lang.get().lower()

        target_lang = output_lang.get().lower()

        source_code = languages[source_lang]

        target_code = languages[target_lang]

        text = recognizer.recognize_google(
            audio,
            language=source_code
        )

        output.insert(
            END,
            "You Said:\n"+text+"\n\n"
        )

        translated = GoogleTranslator(
            source=source_code,
            target=target_code
        ).translate(text)

        output.insert(
            END,
            "Translated:\n"+translated
        )

        # Speak translated language
        speak_translation(
            translated,
            target_code
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


Button(
    root,
    text="Start Speaking",
    width=20,
    command=translate_voice
).pack(pady=20)

root.mainloop()