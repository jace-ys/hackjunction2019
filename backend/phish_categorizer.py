from grammar_check import GrammarChecker
from enum import Enum
import spacy
import numpy as np
from nltk.stem import PorterStemmer
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from parse import Parser

class PhishCategory(Enum):
    set_win = 1 # Tells user they've won a prize
    set_bank = 2 # Tricks user into entering log in credentials
    set_personal = 3 # Tricks user into entering payment info
    non_specific = 4 # Not identified as any other category

class PhishCategorizer:
    # Categorizes a set of text into different phish categories
    # Searches text for keywords and matches to most likely PhishCategory

    keywords = {
        'set_win': [
            'congrat', 'win', 'free', 'click', 'link', 'proceed', 'phone', 'ipad', 'laptop', 'computer', 'dollar', 'claim'
        ],
        'set_bank': [
            'bank', 'login', 'account', 'password', 'secur', 'sign', 'card', 'credit', 'forget', 'pin'
        ],
        'set_personal': [
            'mail', 'address', 'first', 'last', 'name', 'inform', 'verif', 'number', 'forget', 'personal', 'detail'
        ]
    }

    def __init__(self, text):
        self.text = text
        self.category = None
        self.grammar_measure = None

        self.gc = GrammarChecker(self.text) # Initialize grammar checker
        self.sentences = self.gc.get_sentences() # Get sentences from text

    def check_grammar(self, sensitivity = 1):
        # Checks grammar found in website's HTML content
        # gc = GrammarChecker(self.text, sensitivity = sensitivity)

        measure = self.gc.measure_grammar(sensitivity)
        self.grammar_measure = measure
        return measure

    def get_stemmed_text(self):
        # Returns lemmatized text

        lemmatizer = WordNetLemmatizer()
        lemmas = []
        for sent in self.sentences:
            for word, tag in pos_tag(word_tokenize(sent)):
                wntag = tag[0].lower()
                wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
                if not wntag:
                    lemma = word
                else:
                    lemma = lemmatizer.lemmatize(word, wntag)
                lemmas.append(lemma)
        return ' '.join(l for l in lemmas)

    def categorize(self, appearance_threshold = 3):
        # Scans website HTML content and looks for keywords to categorize it

        # Get stemmed text
        self.text = self.get_stemmed_text().lower()
        # Get occurences of keywords in text
        win_occurences = []
        bank_occurences = []
        personal_occurences = []
        set_win, set_bank, set_personal = self.keywords['set_win'], self.keywords['set_bank'], self.keywords['set_personal']
        for word in set_win:
            win_occurences.append(self.text.count(word))
        for bank in set_bank:
            bank_occurences.append(self.text.count(bank))
        for pers in set_personal:
            personal_occurences.append(self.text.count(pers))
        win_c, bank_c, personal_c = sum(win_occurences), sum(bank_occurences), sum(personal_occurences) # Number of appearances

        if win_c > appearance_threshold:
            return PhishCategory.set_win
        elif bank_c > appearance_threshold:
            return PhishCategory.set_bank
        elif personal_c > appearance_threshold:
            return PhishCategory.set_personal
        else:
            # Not categorized
            return PhishCategory.non_specific

if __name__ == '__main__':
    url = 'https://christojati.com'

    p = Parser()

    # Test text
    url_text = p.scrape_text(url)

    non_specific_text = 'An ipad paragraph is a group of words put together to form a group that is usually longer than a sentence. Paragraphs are often made up of several sentences. There are usually between three and eight sentences. Paragraphs can begin with an indentation (about five spaces), or by missing a line out, and then starting again. This makes it easier to see when one paragraph ends and another begins. In most organized forms of writing, such as essays, paragraphs contain a topic sentence . This topic sentence of the paragraph tells the reader what the paragraph will be about. Essays usually have multiple paragraphs that make claims to support a thesis statement, which is the central idea of the essay. Paragraphs may signal when the writer changes topics. Each paragraph may have a number of sentences, depending on the topic.'

    win_text = 'Congratulations! You are winning a free ipad!! Click here to claim your prize. '

    bank_text = 'You have been   locked out of your bank acount! Pls enter your credit card number and security pin. Youre home insurrance has been compromised and you need to renew now! Enter youre personal details to continue'

    personal_text = 'Your home insurance has been compromised and you need to renew now! Enter your personal details to continue'

    pc = PhishCategorizer(bank_text) # Initialize Categorizer with text we want to categorize
    r = pc.categorize()
    print(r)
    res = pc.check_grammar()
    print(res)
