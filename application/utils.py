import easyocr
from googletrans import Translator

def perform_ocr(image, language):
    translator = Translator()
    reader = easyocr.Reader([language])
    image_data = image.read()
    result = reader.readtext(image_data)
    extracted_text = ' '.join([entry[1] for entry in result])
    translated_text = translator.translate(extracted_text, dest='en').text
    return translated_text
