from __future__ import unicode_literals, print_function
from grammarbot import GrammarBotClient
from spacy.lang.en import English
from enum import Enum
import spam

client = GrammarBotClient()

url = 'https://www.grammarbot.io/'
text = spam.scrape_text(url)
# print(text)
# res = client.check(text)

# print(res)

class PhishCategory(Enum):
    claim_prize = 1 # Tells user they've won a prize
    request_auth = 2 # Tricks user into entering log in credentials
    payment_auth = 3 # Tricks user into entering payment info

class PhishCategorizer:
    # Categorizes a set of text into different phish categories
    # Searches text for keywords and matches to most likely PhishCategory

    def __init__(self, text):
        self.text = text
        self.category = None


class GrammarCheck:

    def __init__(self, text, max_char_count = 15):
        # Initialize checker with text and preprocess text by removing unwanted sentences
        self.text = text
        self.max_char_count = max_char_count
        self.client = GrammarBotClient()
        self.sentences = self.get_sentences()
        self.preprocess_text()

    def get_sentences(self):
        nlp = English()
        nlp.add_pipe(nlp.create_pipe('sentencizer')) # updated
        doc = nlp(self.text)
        sentences = [sent.string.strip() for sent in doc.sents]
        return sentences

    def preprocess_text(self):
        # Remove sentences with words greater than max_char_count
        for sent in self.sentences:
            for word in sent.split():
                if len(word) > self.max_char_count:
                    self.sentences.remove(sent)
        self.text = ' '.join(sent for sent in self.sentences)

    def check_grammar(self):
        res = self.client.check(self.text)
        print(res)

if __name__ == '__main__':
    grammar_checker = GrammarCheck('hellomynameisjoshuaramkissoon. My nickname is josh. I have appreciated verymuchyour help. Pleasestopmessagingmeplease.')
    grammar_checker.check_grammar()
    grammar_checker.category = PhishCategory.request_auth
    print(grammar_checker.category)
