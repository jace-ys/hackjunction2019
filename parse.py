from urllib.request import urlopen
from bs4 import BeautifulSoup
from spacy_langdetect import LanguageDetector
import json
import spacy

class Parser:

    def scrape_text(self, url):
        # URL of website to be scraped
        try:
            html = urlopen(url).read()
            soup = BeautifulSoup(html, features = 'html.parser')

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            return text
        except:
            return None

    def get_language(self, text):
        # Returns language code eg 'en' for english
        nlp = spacy.load('en')
        nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
        return nlp(text)._.language['language']
