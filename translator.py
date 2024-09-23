from gtts import gTTS
import os
from googletrans import Translator
import speech_recognition as sr

dict = {'English': 'en','Spanish': 'es','French': 'fr','German': 'de','Italian': 'it','Portuguese': 'pt','Russian': 'ru','Dutch': 'nl',
        'Chinese': 'zh-CN','Japanese': 'ja','Korean': 'ko','Vietnamese': 'vi','Thai': 'th',
        'Hindi': 'hi','Arabic': 'ar', 'Turkish': 'tr', 'Bengali': 'bn', 'Punjabi': 'pa','Tamil': 'ta', 'Telugu': 'te','Marathi': 'mr',
        'Gujarati': 'gu', 'Kannada':'kn','Hebrew': 'he','Persian': 'fa', 'Kurdish': 'ku'
}

lan=input("enter the language: ")

if lan.title() in dict:
    value = dict[lan.title()]
    # print(f"The value for key '{lan}' is: {value}")
else:
    print(f"The key '{lan}' is not present in the dictionary.")


# Speech Recognition
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something in language:")
    audio = recognizer.listen(source)

# Recognize and translate
try:
    text = recognizer.recognize_google(audio, language=value)
    print("You said '{lan}':", text)

    # Translation using googletrans
    translator = Translator()
    translation = translator.translate(text, dest="en")

    if translation.text:
        english_translation = translation.text
        print("Translated to English:", english_translation)

        # Text-to-Speech (English)
        tts_english = gTTS(english_translation, lang='en')
        tts_english.save("output_english.mp3")

        # Play the generated English audio file
        os.system("start output_english.mp3")

    else:
        print("Translation to English failed.")

except sr.UnknownValueError:
    print("Sorry, could not understand audio.")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")