from annotated_text import annotated_text
from bs4 import BeautifulSoup
from gramformer import Gramformer
from spellchecker import SpellChecker
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
import pandas as pd
import torch
import math
import re

def set_seed(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(1212)

class GramformerCorrector:

    def __init__(self):
        self.model_map = {
            'Corrector': 1
        }

    def load_gf(self, model: int):
        """
        Load Gramformer model
        """
        gf = Gramformer(models=model, use_gpu=False)
        return gf

    def show_highlights(self, gf: object, input_text: str, corrected_sentence: str):
        """
        To show highlights
        """
        try:
            strikeout = lambda x: '\u0336'.join(x) + '\u0336'
            highlight_text = gf.highlight(input_text, corrected_sentence)
            color_map = {'d': '#faa', 'a': '#afa', 'c': '#fea'}
            tokens = re.split(r'(<[dac]\s.*?<\/[dac]>)', highlight_text)
            annotations = []
            for token in tokens:
                soup = BeautifulSoup(token, 'html.parser')
                tags = soup.findAll()
                if tags:
                    _tag = tags[0].name
                    _type = tags[0]['type']
                    _text = tags[0]['edit']
                    _color = color_map[_tag]

                    if _tag == 'd':
                        _text = strikeout(tags[0].text)

                    annotations.append((_text, _type, _color))
                else:
                    annotations.append(token)
            args = {
                'height': 45 * (math.ceil(len(highlight_text) / 100)),
                'scrolling': True
            }
            annotated_text(*annotations, **args)
        except Exception as e:
            print('Some error occurred!')

    def show_edits(self, gf: object, input_text: str, corrected_sentence: str):
        """
        To show edits
        """
        try:
            edits = gf.get_edits(input_text, corrected_sentence)
            df = pd.DataFrame(edits, columns=['type', 'original word', 'original start', 'original end',
                                              'correct word', 'correct start', 'correct end'])
            df = df.set_index('type')
            print(df)
        except Exception as e:
            print('Some error occurred!')

    def suggest_paraphrases(self, input_text: str, num_suggestions=3):
        """
        Suggest paraphrases for the input sentence using LangChain.
        """
        openai_api_key = ''
        prompt_template = PromptTemplate(input_variables=['text'], template='Paraphrase the following text: {text}')
        llm = OpenAI(openai_api_key=openai_api_key, temperature=0.8)
        chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)

        try:
            for i in range(num_suggestions):
                paraphrased_text = chain.run(input_text)
                print(f"Suggestion {i + 1}: {paraphrased_text}")
                return paraphrased_text
        except Exception as e:
            print('Some error occurred!')

    def correct_text(self, input_text):
        # Correct spelling mistakes first
        spell = SpellChecker()
        corrected_sentence = ' '.join(spell.correction(word) for word in input_text.split())

        # Correct grammar mistakes
        gf = self.load_gf(self.model_map['Corrector'])
        results = gf.correct(corrected_sentence)
        corrected_sentence = list(results)[0]

        print(f'Corrected Sentence: {corrected_sentence}')
        # self.show_highlights(gf, input_text, corrected_sentence)
        # self.show_edits(gf, input_text, corrected_sentence)
        return corrected_sentence
        # Suggest paraphrases
        # self.suggest_paraphrases(corrected_sentence)

if __name__ == "__main__":
    obj = GramformerCorrector()
    user_input = input("Enter the text: ")
    obj.correct_text(user_input)