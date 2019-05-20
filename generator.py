import random
import json

# with open('smallvocab.json','r') as f:
#     vocab = json.load(f)

with open('sent_templates_small.json','r') as f:
    templates = json.load(f)

templates.sort(key=len)

from collections import defaultdict

from nltk import tokenize,pos_tag


class Generator:    
    
    def __init__(self,n=10):
        """
        """
        self.templates = templates
        self.vocab = defaultdict(list) ## empty vocab
        
    def fill_in_pos(self,pos):
        """
        fill in the words here
        """
        return random.choice(self.vocab[pos])
        
    def generate(self,template_limit=None):
        """
        pick a template and fill it in 
        """
        try:
            if template_limit==None:
                temp = random.choice(self.templates)
            else:
                temp = random.choice(self.templates[template_limit:])
            generated = [self.fill_in_pos(pos) for pos in temp]
            return generated
        except:
            return None



def main():
    gen = Generator()
    print(gen.generate())


if __name__ == '__main__':
    main()