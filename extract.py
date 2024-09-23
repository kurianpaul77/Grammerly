import easyocr
from PIL import Image
from googletrans import Translator

# Function to translate text using Google Translate API
def translate_text(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

language = input("Enter the language: ").lower()

english = ['en']
hindi = ['hi']  # Hindi
arabic = ['ar']  # Arabic
spanish = ['es']  # Spanish
french = ['fr']  # French
italian = ['it']  # Italian
japanese = ['ja']  # Japanese
kannada = ['kn']  # Kannada
languages = {"english": english, "hindi": hindi, "arabic": arabic, "spanish": spanish, "french": french, "italian": italian, "japanese": japanese, "kannada": kannada}

if language in languages:
    reader = easyocr.Reader(languages[language])  # Pass a list of languages
    image_path = r"D:\Internship Luminar\Main Projects\scanner\static\download.png"
    image = Image.open(image_path)

    # Perform OCR to extract text from the image
    result = reader.readtext(image_path)

    # Extracted text from the result
    extracted_text = ' '.join([entry[1] for entry in result])

    # Translate the extracted text to English
    translated_text = translate_text(extracted_text, target_language='en')

    # Print the translated text
    print("Translated Text:", translated_text)
else:
    print("Language not supported. Please choose from:", list(languages.keys()))