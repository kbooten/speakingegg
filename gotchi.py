import random

from nltk import tokenize,ngrams,pos_tag
from nltk import NaiveBayesClassifier

from generator import Generator
gen = Generator()

from QuestionAsker import QuestionAsker
qa = QuestionAsker()

import re

from numpy import mean


from collections import defaultdict

# from scraper import Scraper
# scr = Scraper()

import itertools

from nltk.corpus import stopwords
from nltk import FreqDist
stops = stopwords.words('english')

import more_itertools

class Gotchi:
    

    def __init__(self):
        self.gen = gen
        self.qa = qa
        self.pos = []
        self.neg = []
        self.classifier = None
        self.good_sents = []


    def add_new_text_to_generator(self,text):
        tokenized_and_tagged = pos_tag(tokenize.casual_tokenize(text))
        print(tokenized_and_tagged)
        for token,tag in tokenized_and_tagged:
            self.gen.vocab[tag].append(token)
        print("vocablength:")
        print(len(list(itertools.chain(*self.gen.vocab.values()))))
        return len(list(set(self.gen.vocab)))



    def add_new_template(self,text):
        sent = random.choice(tokenize.sent_tokenize(text))
        print(sent)
        template = [tag for token,tag in pos_tag(tokenize.casual_tokenize(sent))]
        if template not in self.gen.templates:
            self.gen.templates.append(template)
        return template


        
    def get_templates(self):
        return [" ".join(t) for t in self.gen.templates]


    def get_top_words(self):
        vocab = list(itertools.chain(*self.gen.vocab.values()))
        vocab = [v for v in vocab if v not in stops]
        vocab = [v for v in vocab if len(v)>1]
        most_common = [k.lower() for k,v in FreqDist(vocab).most_common(50)]
        print (most_common)
        return most_common



    # def add_new_text_to_model(self,text):
    #     sents =  tokenize.sent_tokenize(text)
    #     self.pos+=sents

    def featurize(self,text):
        if type(text) == str:
            text = text.strip('"')
            text = text.strip('``')
            text = tokenize.word_tokenize(text)
        features = {}
        tokenized = [w.lower() for w in text]
        features.update({w:True for w in tokenized})
        tokenized = ["<START>"] + tokenized +["<END>"] 
        features.update({str(bigram):True for bigram in ngrams(tokenized,2)})

        # ## get words that appear together
        # not_stops = [t for t in tokenize if t not in stops]
        return features 
    

    def train(self):
        neg_features = [(self.featurize(example),'bad') for example in self.neg]
        pos_features = [(self.featurize(example),'good') for example in self.pos]
        classif = NaiveBayesClassifier.train(neg_features+pos_features)
        self.classifier = classif
   

    def try_to_get_good_utterance(self):
        number_of_attempts = random.randint(500,5000)
        template_limit = random.randint(0,len(self.gen.templates)-2)
        the_sample = [self.gen.generate(template_limit) for i in range(number_of_attempts)]
        the_sample = [s for s in the_sample if s!=None]
        featurized = [(self.featurize(s),s) for s in the_sample]
        classified = [(self.classifier.prob_classify(f).prob('good'),s) for (f,s) in featurized]
        ranked = sorted(classified, key=lambda x: x[0],reverse=True)
        ## add to good sents
        self.good_sents.append(self.format_utterance(ranked[0][1]))
        self.good_sents = self.good_sents[-5:]
        return ranked[0][0],self.format_utterance(ranked[0][1])
    

    def format_utterance(self,utterance):
        try:
            return " ".join(utterance)
        except:
            return None

    def get_random_non_optimized_utterance(self):
        return None,self.format_utterance(self.gen.generate())


    def get_most_informative_features(self, n=50):
        # Determine the most relevant features, and display them.
        cpdist = self.classifier._feature_probdist

        Feats = []

        for (fname, fval) in self.classifier.most_informative_features(n+5):

            def labelprob(l):
                return cpdist[l, fname].prob(fval)

            labels = sorted(
                [l for l in self.classifier._labels if fval in cpdist[l, fname].samples()],
                key=labelprob,
            )
            if len(labels) == 1:
                continue
            l0 = labels[0]
            l1 = labels[-1]

            Feats.append((fname, fval, l1, l0))
        #return Feats
            

        def format_double_feat(feature):
            if feature.startswith("("):
                feature = re.findall(r"\(u?[\"\'](.+)[\"\'], u?[\"\'](.+)[\"\']\)",feature)[0]
                if feature[0]=="<START>":
                    return "<span class='innerFeature'>%s</span> at the beginning" % feature[1]
                elif feature[1]=="<END>":
                    return "<span class='innerFeature'>%s</span> at the end" % feature[0]
                else:
                    feature = "<span class='innerFeature'>%s</span> followed by <span class='innerFeature'>%s</span>" % (feature[0],feature[1])
                    return str(feature)
            return "<span class='innerFeature'>%s</span>" % feature


        def format_feat(fname,fval,l1,l0):
            if l1=="good":
                if fval==None:
                    return "do not contain %s" % (format_double_feat(fname))
                else:
                    return "contain %s" % (format_double_feat(fname))

            elif l1=="bad":
                if fval==None:
                    return "contains %s" % (format_double_feat(fname))
                else:
                    return "do not contain %s" % (format_double_feat(fname))

        formatted_features = [format_feat(*f) for f in Feats]
        return list(more_itertools.unique_everseen(formatted_features))[:20]


    def retrain(self,evaluation,text):
        print(evaluation)
        print(text)
        if evaluation=='+':
            self.pos.append(text)
        elif evaluation=='-':
            self.neg.append(text)
        try:
            self.train()
        except ValueError:
            print ("not enough classes yet")
            return []
        return self.get_most_informative_features(n=20)

    def restart(self):
        self.gen.vocab = defaultdict(list)
        self.pos = []
        self.neg = []
        #self.classifier = None
        self.gen.template_limit=10 ##terrible...
        print(len(self.gen.templates[:10]))


