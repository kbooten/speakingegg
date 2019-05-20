
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
from nltk import tokenize,pos_tag


class Scraper:
    
    def __init__(self):
        all_sents = []

    def _tag_visible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def _text_from_html(self,body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = list(filter(self._tag_visible, texts))  
        return visible_texts
    
    def _visiblefilter(self,text):
        if text[0].isalpha():
            if any(c in text for c in [u'©',u"™"])==False:
                if text[0] == text[0].upper():
                    if text[-1] in ".!?":
                        if text[-2]!=".":
                            return True
        return False
    
    def _sent_tokenization(self,texts):    
        gathered_sents = []
        for sents in [tokenize.sent_tokenize(f) for f in texts]:
            for s in sents:
                gathered_sents.append(s)
        return gathered_sents
    
    
    def _meta_sentence_gathering(self,body):
        visible = self._text_from_html(body)
        filtered = [v for v in visible if self._visiblefilter(v)]
        sents = self._sent_tokenization(filtered)
        return sents
    

    def additional_filter(self,text):
        tokenized = tokenize.word_tokenize(text.lower())
        if tokenized[-1]!=".":
            return False
        pos_tags_first_letters = [tag[0] for token,tag in pos_tag(tokenized)]
        if "N" not in pos_tags_first_letters:
            return False
        if "V" not in pos_tags_first_letters:
            return False
        return True



    def read(self,url,apply_additional_filter=True):
        body = requests.get(url).text
        sents = self._meta_sentence_gathering(body)
        if apply_additional_filter==True:
            sents = [s for s in sents if self.additional_filter(s)]
        return sents


if __name__ == "__main__":
    s = Scraper()
    print(s.read('https://slate.com/'))
        