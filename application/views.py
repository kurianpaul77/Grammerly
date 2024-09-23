from django.shortcuts import render,redirect
from application.forms import ImageUploadForm,PdfUploadForm,TextUploadForm
from application.models import ImageUpload,ExtractedData,TextUpload,PdfUpload
from django.http import JsonResponse
from pytesseract import pytesseract
from PIL import Image
from application.serializers import ExtractedSerializer
import pdfplumber
from googletrans import LANGUAGES
from .translator import translate_text
import os

from django.http import HttpResponse
from gtts import gTTS
from googletrans import Translator
import speech_recognition as sr

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
from django.views.generic import TemplateView

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from bs4 import BeautifulSoup
from application.gramformer import Gramformer
from .gramformer import Gramformer
from spellchecker import SpellChecker
import pandas as pd
import torch
import math
import re
import openai
from annotated_text import annotated_text
from .new2 import GramformerCorrector

def base(request):
    return render(request,'home.html')

from django.shortcuts import render
from django.http import JsonResponse
from .utils import perform_ocr

def home(request):
    return render(request, 'imageupload.html')


def translate_textt(request):
    if request.method == 'POST' and request.FILES['image']:
        language = request.POST.get('language')
        image = request.FILES['image']
        translated_text = perform_ocr(image, language)
        data = ExtractedData.objects.create(text= translated_text)
        data.save()
        return render(request,'extracted.html',{'extracted_text': translated_text})
    return render(request,'imageupload.html')


# def image_upload(request):
#     if(request.method=="POST"):
#         i=request.FILES.get('i')
#         img=ImageUpload.objects.create(files=i)
#         img.save()
#         return imageextract(request)

#     return render(request,'imageupload.html')

def text_upload(request):
    if(request.method=="POST"):
        t=request.POST.get('t')
        text=TextUpload.objects.create(text=t)
        text.save()
        return get_text(request)
    return render(request,'textupload.html')

def pdf_upload(request):
    if request.method == "POST":
        p = request.FILES.get('p')
        pdf = PdfUpload.objects.create(files=p)
        pdf.save()
        return pdf_extract(request)

    return render(request, 'pdfupload.html')


# def imageextract(request):
#     if request.method == 'POST':
#         # Get the uploaded image
#         img = ImageUpload.objects.latest('uploaded_at') # You might want to filter or select the image in a specific way

#         if img:
#             image = Image.open(img.files.path)
#             pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

#             # Perform OCR to extract text from the image
#             extracted_text = pytesseract.image_to_string(image)

#             # Create a new ExtractedData object and save the extracted text
#             data = ExtractedData.objects.create(text=extracted_text)
#             data.save()

#             # Return the extracted text as JSON
#             return render(request, 'extracted.html', {'extracted_text': extracted_text})
#         else:
#             return render(request, 'errorpage.html', {'error': 'No image uploaded'})

#     return render(request, 'imgextract.html')

def pdf_extract(request):
    if request.method == "POST":
        try:
            pdf = PdfUpload.objects.latest("uploaded_at")
            if pdf and pdf.files:
                # Check if the 'files' attribute is not None
                with pdfplumber.open(pdf.files.path) as pdf_doc:
                    extracted_text = ""
                    for page in pdf_doc.pages:
                        extracted_text += page.extract_text()
                        data = ExtractedData.objects.create(text=extracted_text)
                        data.save()


                # You can now use 'extracted_text' in your template or perform further processing
                return render(request, 'extracted.html', {'extracted_text': extracted_text})
            else:
                # Handle the case where 'pdf' or 'pdf.files' is None
                return render(request, 'errorpage.html', {'error_message': 'No PDF file found.'})
        except PdfUpload.DoesNotExist:
            # Handle the case where no PdfUpload objects are found
            return render(request, 'errorpage.html', {'error_message': 'No PDF uploaded yet.'})

    return render(request, 'pdfextract.html')

def getdata(request):
    data=ExtractedData.objects.latest('uploaded_at')
    data_str=data.text
    print(data_str)
    print(type(data_str))
    return render(request, 'home.html')

def translation(request):
    if request.method == "POST":
        lang_code = request.POST.get('lang_code')

        data = ExtractedData.objects.latest('uploaded_at')
        print(data)
        data_str = data.text
        print(data_str)

        translated_text = translate_text(data_str, "en", lang_code)
        print(translated_text)
        return render(request, 'translated.html', {'translated_text': translated_text})
    return render(request, 'translate.html')

# def text_extract(request):
#     if request.method=="POST":
#         data=TextUpload.objects.latest('uploaded_at')
#         if data:                              
#             obj=ExtractedData()
#             obj.text=data.text
#             obj.save()
#         else:
#             pass
#         return translation(request)

def get_text(request):
    text=TextUpload.objects.latest('uploaded_at')
    return render(request,'text.html',{'text':text})

def text_translation(request):
    if request.method == "POST":
        lang_code = request.POST.get('lang_code')
        if not lang_code:
            return render(request, 'translate.html')
        data = TextUpload.objects.latest('uploaded_at')
        data_str = data.text

        translated_text = translate_text(data_str, "en", lang_code)
        return render(request, 'translated.html', {'translated_text': translated_text})
    return render(request, 'translate.html')





openai.api_key = ''

def set_seed(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(1212)



def GramformerCorrectorView(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        obj = GramformerCorrector()
        corrected_text = obj.correct_text(user_input)
        return render(request,"gramformer_corrector.html" , {'corrected_text': corrected_text})
    else:
        return render(request,"gramformer_corrector.html" )


import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
from django.views.generic import TemplateView

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        openai_api_key = ''
        llm = OpenAI(openai_api_key=openai_api_key, temperature=0.8)

        input_text = request.POST.get('input_text', '')

        if input_text.lower() == 'exit':
            return JsonResponse({'response': 'Thank you for using Chatbot. Have a great day ahead'})

        if input_text.lower() in ['hi', 'hai', 'hello', 'hy']:
            return JsonResponse({'response': 'Hai, Welcome to Chatbot'})

        if input_text.lower() in ['bye', 'by', 'goodbye', 'thank you', 'thanks']:
            return JsonResponse({'response': 'Thank you for using Chatbot. Have a great day ahead.'})

        input_prompt = PromptTemplate(input_variables=['query'], template='IT related {query}')
        chain = LLMChain(llm=llm, prompt=input_prompt, verbose=True)
        
        return JsonResponse({'response': chain.run(input_text)})
    else:
        return JsonResponse({'response': 'Invalid request'}, status=400)

class ChatBotView(TemplateView):
    template_name="chatbot.html"



from django.shortcuts import render
from gtts import gTTS
from googletrans import Translator
import speech_recognition as sr
import os

def audio_translation(request):
    if request.method == 'POST':
        dict_languages = {'English': 'en','Spanish': 'es','French': 'fr','German': 'de','Italian': 'it','Portuguese': 'pt','Russian': 'ru','Dutch': 'nl',
        'Chinese': 'zh-CN','Japanese': 'ja','Korean': 'ko','Vietnamese': 'vi','Thai': 'th',
        'Hindi': 'hi','Arabic': 'ar', 'Turkish': 'tr', 'Bengali': 'bn', 'Punjabi': 'pa','Tamil': 'ta', 'Telugu': 'te','Marathi': 'mr',
        'Gujarati': 'gu', 'Kannada':'kn','Hebrew': 'he','Persian': 'fa', 'Kurdish': 'ku','Malayalam':'ml'
}
        
        lan = request.POST.get('language')
        if lan.title() in dict_languages:
            value = dict_languages[lan.title()]
        else:
            return render(request, 'translation_audio.html', {'error': f"The language '{lan}' is not available."})

        translator = Translator()

        # Provide the instruction to the user
        instruction_translation = translator.translate("Say something in " + lan.title(), src='en', dest=value)
        instruction_text = instruction_translation.text
        tts_instruction = gTTS(instruction_text, lang=value)
        tts_instruction.save("static/instruction.mp3")
        # os.system("start instruction.mp3")

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print(instruction_text)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language=value)
            translation = translator.translate(text, dest="en")

            if translation.text:
                english_translation = translation.text
                tts_english = gTTS(english_translation, lang='en')
                tts_english.save("static/output_english.mp3")
                # os.system("start output_english.mp3")
                
                return render(request, 'translation_audio.html', {'translated_text': english_translation})
            else:
                return render(request, 'translation_audio.html', {'error': "Translation to English failed."})

        except sr.UnknownValueError:
            return render(request, 'translation_audio.html', {'error': "Sorry, could not understand audio."})
        except sr.RequestError as e:
            return render(request, 'translation_audio.html', {'error': f"Could not request results from Google Speech Recognition service; {e}"})

    return render(request, 'translation_audio.html') 

