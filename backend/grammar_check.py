from __future__ import unicode_literals, print_function
from grammarbot import GrammarBotClient
from spacy.lang.en import English
# import spam
import math

class GrammarChecker:

    def __init__(self, text, max_char_count = 17, sensitivity = 1):
        # Initialize checker with text and preprocess text by removing unwanted sentences
        # Sensitivity (0, 1): how strict you are with typos
        # Sensitivity of 1 is strictest, 0 is most lenient

        self.text = text
        self.max_char_count = max_char_count
        self.sensitivity = sensitivity
        self.client = GrammarBotClient()
        self.sentences = self.get_sentences()
        self.num_words = 0
        self.preprocess_text()

    def get_sentences(self):
        # Returns sentences from text
        nlp = English()
        nlp.add_pipe(nlp.create_pipe('sentencizer')) # updated
        doc = nlp(self.text)
        sentences = [sent.string.strip() for sent in doc.sents]
        return sentences

    def preprocess_text(self):
        # Remove sentences with words greater than max_char_count
        count = 0
        for sent in self.sentences:
            for word in sent.split():
                if len(word) > self.max_char_count:
                    if sent in self.sentences:
                        self.sentences.remove(sent)
                count += 1
        self.num_words = count
        self.text = ' '.join(sent for sent in self.sentences)

    def measure_grammar(self, sensitivity = 1, ignore_doublespace = True, ignore_punctuation = True):
        # Return a measure of typo appearance in text
        res = self.client.check(self.text)
        matches = res.matches
        results = []
        num_typos = 0
        if ignore_doublespace and ignore_punctuation:
            for match in matches:
                if match.category != 'TYPOGRAPHY' and match.category != 'PUNCTUATION':
                    results.append(match)
            num_typos = len(results)
        elif ignore_doublespace:
            for match in matches:
                if match.category != 'TYPOGRAPHY':
                    results.append(match)
            num_typos = len(results)
        elif ignore_punctuation:
            for match in matches:
                if match.category != 'PUNCTUATION':
                    results.append(match)
            num_typos = len(results)
        num_sentences = len(self.sentences)
        measure = num_typos**1.5*math.exp(num_typos-(0.25*(num_sentences)))*sensitivity/self.num_words
        return measure
