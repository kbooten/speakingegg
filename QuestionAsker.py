import spacy
nlp = spacy.load("en_core_web_sm")
import random




class QuestionAsker:
	'''
	Class to ask questions about sentences---basically to reverse them into questions.
	'''

	def __init__(self):
		#self.sents = []
		self.questions = []
		self.question_types = [self.getVerbQuestion,self.getAdjQuestion]


	def getQuestion(self,sent):
		# for s in sents:
		try:
			qs = self.metaQuestion(sent)
			qs_ok = [q for q in qs if q not in self.questions]
			q_choice = random.choice(qs_ok)
			self.questions.append(q_choice)
			return q_choice
		except:
		 	return None


	def metaQuestion(self,sent):
		qs = []
		for q in self.question_types:
			try:
				qs.append(q(sent))
			except:
				pass
		return qs



	def format_verb_question(self,noun,verb,number):
		auxverb = "does"
		if number=="NNS":
			auxverb = "do"
		return "Why %s the %s %s?" % (auxverb,noun,verb)



	def getVerbQuestion(self,sent):
		spacified = nlp(sent)
		noun_verb_number = []
		for token in spacified:
			if token.pos_ == "VERB":
				if token.lemma_ != 'be':
					nouns = [t for t in token.children if (t.pos_==u'NOUN' and t.dep_=="nsubj")]
					if nouns!=[]:
						noun = random.choice(nouns)
						noun_verb_number.append((noun.text,token.text,noun.tag_))
		return self.format_verb_question(*random.choice(noun_verb_number))		



	def format_adj_question(self,adj,noun,number):
		verb = "is"
		if number=="NNS":
			verb = "are"
		return "Why %s the %s %s?" % (verb,noun,adj)



	def getAdjQuestion(self,sent):
		spacified = nlp(sent)
		adj_n_number = []
		for token in spacified:
			if token.tag_ in ["NN","NNS"]:
				adjectives = [t.text for t in token.children if t.dep_==u'amod']
				if adjectives!=[]:
					adj_n_number.append((random.choice(adjectives),token.text,token.tag_))
		return self.format_adj_question(*random.choice(adj_n_number))



def main():
	qa = QuestionAsker()
	print(qa.getQuestion(u"The good men drink beer."))
	print(qa.getQuestion(u"The good men drink beer."))
	print(qa.getQuestion(u"The good men drink beer."))





if __name__ == '__main__':
	main()

