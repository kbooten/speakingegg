from flask import Flask
from flask import render_template,jsonify,request
app = Flask(__name__)
import os

from gotchi import Gotchi 
from QuestionAsker import QuestionAsker
qa = QuestionAsker()

class metabot:
	def __init__(self):
		self.bot = Gotchi()

mb = metabot()

import random

@app.route('/')
def main_page():
	print("RESTARTING BOT>>>>>>>>")
	mb.bot.restart()
	#hashkey = random.getrandbits(128)
	#bots[hashkey]=bot
	return render_template('index.html')#,hashkey=hashkey)


@app.route("/read", methods=["GET"])
def read():
	text = request.args.get('text')
	#url = request.args.get('newurl')
	mb.bot.add_new_text_to_generator(text)
	template=None
	if request.args.get('newTemplate')=='true':
		template = mb.bot.add_new_template(text)
	else:
		template = None

	# mb.bot.add_new_text_to_model(text)
	return jsonify({'aNewTemplate':template,"templates":mb.bot.get_templates(),"vocab":mb.bot.get_top_words()})


@app.route('/retrain', methods=['GET'])
def retrain():
	evaluation = request.args.get('evaluation')
	text = request.args.get('text')
	print (evaluation,text)

	top_features = mb.bot.retrain(evaluation,text)
	return jsonify({'topFeatures':top_features})


@app.route('/speak', methods=['GET'])
def speak():
	try:
		prediction,utterance = mb.bot.try_to_get_good_utterance()
	except:
		prediction,utterance = mb.bot.get_random_non_optimized_utterance()
	return jsonify({"prediction":prediction, "utterance":utterance})


@app.route('/askQuestion', methods=['GET'])
def ask_question():
	text = request.args.get('text')
	question = qa.getQuestion(text)
	return jsonify({"question":question})



if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

