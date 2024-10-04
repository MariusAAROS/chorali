# coding: utf8
#we must specify the encoding as utf-8 because python2.7 default encoding is ascii which causes many bugs
from __future__ import unicode_literals #this allows to have all text in unicode rather than str, it is a Python 3 feature

import re , os
#from nltk.corpus import wordnet as wn
import nltk , time
import codecs

"""
returns a list of lists called 'sentences'. Each list in sentences contains the token of a single sentence.
units are either "words" or "tokens" , this is detemined by the 3rd parameter of the function
"""
_currentdir = os.path.dirname(os.path.realpath(__file__))

def sentTokenize(text):
    """
    Basic sentence tokenizer using nltk punkt
    """
    sentTokenizer = nltk.data.load('file:' +
                                   _currentdir +
                                   '/data/english.pickle')
    return sentTokenizer.tokenize(text)


def get_one_file_units(tokenizedFile,sourceFile,unit_type, pos_filter):

	new_sentence = True
	n_sentence= -1
	text=""
	sent_positions = []
	dataset = []
	sentences = []
	count = True
	with open(tokenizedFile, 'r') as tokens_file, open(sourceFile, 'r') as source_file, open("./output.txt", 'w') as output_file:
		sentences_units=[]
		units={'noun':[],'verb':[],'adj':[],'adv':[]}
		for s_ligne in source_file:
			text = text + s_ligne
		n_sentence+= 1
		sentence = ""
		for ligne in tokens_file:
			if (new_sentence == True):
				start = int(ligne.split(' ')[0]) - 1
				new_sentence = False
			if len(ligne.split(' ')) > 2 :
				ch = ligne.split(' ')[2]
				if (not re.match('(\w)*_(\w)*',ch)) :
					find = re.search('(?<=#)\w+', ligne)
					if find :
						ch = find.group(0)
						if ch == 'QUOT':
							count = False
						elif ch == 'SENT':
								end = int(ligne.split(' ')[0])
								if (end - start) > 3:
									pos = [start,end]
									if count :
										sent_positions.append(pos)
										sentence = text[start:end]
										if len(sentence) < 5 :
											print(sentence , "  ", end - start)
										sentences.append(sentence)
										dataset.append(n_sentence)
										sentences_units.append(units)
										n_sentence+=1
								count = True
								new_sentence = True

								"""
								output_file.write("\n sentence "+str(n_sentence)+"\n"+"nouns:\n")
								for noun in units['noun']:
									output_file.write(noun+ "\t")
								output_file.write("\n verbs: \n")
								for verb in units['verb']:
									output_file.write(verb+ "\t")
								output_file.write("\n adverbs: \n")
								for adverb in units['adv']:
									output_file.write(adverb+ "\t")
								output_file.write("\n adjectives: \n")
								for adj in units['adj']:
									output_file.write(adj+ "\t")
								"""
								units={'noun':[],'verb':[],'adj':[],'adv':[]}

						elif ch in pos_filter:
							if count :
								if unit_type == "tokens":
									unit = get_token_from_lima_output(ligne)
								elif unit_type == "words":
									unit = get_word_from_lima_output(ligne)
								if ch in {'NN','NNP','NNS'}:
									units['noun'].append(unit)
								elif ch == 'JJ':
									units['adj'].append(unit)
								elif ch == 'RB' :
									units['adv'].append(unit)
								elif ch in {'VB','VBG','VBN','VBD','VBZ'} :
									units['verb'].append(unit)
	return sentences_units , sentences, sent_positions, dataset

def getSentenceUnits(sent):
	units={'noun':[],'verb':[],'adj':[],'adv':[]}
	tok = nltk.tokenize.word_tokenize(sent)
	pos=nltk.pos_tag(tok)
	for couple in pos :
		category = couple[1]
		word = couple[0]
		if category in {'NN','NNP','NNS'}:
			units['noun'].append(word)
		elif category in {'VB','VBG','VBN','VBD','VBZ'} :
			units['verb'].append(word)
		elif category == "JJ" :
			units['adj'].append(word)
		elif category == "RB" :
			units['adv'].append(word)
	return units

"""returns 3 output variables
sentences : list of raw text sentences | exp : l = {sentence1,sentence2}
sent_positions : list of corresponding sentences positions in the source text file | exp : sentp = {(start_pos_sent1,end_pos_sent1),(start_pos_sent2,end_pos_sent2)}
dataset : list of sentences numbers in order | exp : dset = {1,2}
"""
def getOneFileSentences(tokenizedFile,sourceFile):
	new_sentence = True
	n_sentence= -1
	text=""
	sent_positions = []
	dataset = []
	sentences = []
	count = True
	with open(tokenizedFile, 'r') as tokens_file, open(sourceFile, 'r') as source_file:
		for s_ligne in source_file:
			text = text + s_ligne
		sentence = ""
		for ligne in tokens_file:
			if (new_sentence == True):
				start = int(ligne.split(' ')[0]) - 1
				new_sentence = False
			if len(ligne.split(' ')) > 2 :
				ch = ligne.split(' ')[2]
				find = re.search('(?<=#)\w+', ligne)
				if find :
					ch = find.group(0)
					if ch == 'QUOT':
						count = False
					elif ch == 'SENT':
						end = int(ligne.split(' ')[0])
						pos = [start,end]
						new_sentence = True
						if count :
							n_sentence+=1
							sent_positions.append(pos)
							sentences.append(text[start:end])
							dataset.append(n_sentence)
						count = True
	return sentences,sent_positions,dataset

def get_src_file_from_tkn_file_name(tokenizedFile,sourceDir):
	file_name = os.path.splitext(tokenizedFile)[0]
	sourceFile = os.path.join(sourceDir,file_name)
	return sourceFile , file_name

def get_token_from_lima_output(line):
	lastWord ="" #last column in the output text file of lima
	token=""
	line_array = line.split(' ')
	fieldsNumber = len(line_array)
	lastWord = line_array[fieldsNumber-1] ;
	k=0
	stop = False
	while (k < len(lastWord)) and (not stop) :
		if lastWord[k]=="#" :
			stop = "true"
		else :
			token = token + lastWord[k]
			k = k +1
	return token

def get_word_from_lima_output(ligne):

	word = ""
	word = ligne.split()[2]
	return word

"""
takes as input a word (string) and his category (string in {noun,verb,adj,adv} and returns it wordnet synsets
with that part of speech)
"""
def get_synsets_by_category(word,category):
	if category == "noun":
		word_synsets = wn.synsets(word, pos = wn.NOUN)
	elif category == "verb":
		word_synsets = wn.synsets(word, pos=wn.VERB)
	elif category == "adj":
		word_synsets = wn.synsets(word, pos=wn.ADJ)
	if category == "adv":
		word_synsets = wn.synsets(word, pos=wn.ADV)
	return word_synsets
"""
category in {"noun","verb","adj","adv"}
"""
def insert_unit_and_unit_synsets_into_db(rdb,unit,category)	:
	key = category+"_synsets"
	if not rdb.sismember(category,unit):
		synsets = get_synsets_by_category(unit,category)
		for syn in synsets :
			syn_name = syn.name
			rdb.sadd(key, syn_name)
			rdb.sadd(category, unit)

#this function exists also in sim_matrix.py
def load_idf_from_rdb(rdb):
	idf = {}
	for k in rdb.keys() :
		idf_value = rdb.get(k)
		if idf_value :
			idf_value= float(idf_value)
		idf[k] = idf_value
	return idf

#this function exists also in sim_matrix.py
def load_syn_sim_from_rdb(rdb):
	syn_sim = {}
	for s in ( rdb.smembers("noun_synsets") | rdb.smembers("verb_synsets") ):
		sim_dict = rdb.hgetall(s)
		if sim_dict :
			syn_sim[s]= sim_dict
	return syn_sim

def get_text_from_file(path_to_file):
	with codecs.open(path_to_file,"r","utf-8") as _file:
		lignes = _file.read().splitlines()
		#lignes  = _file.readlines()
		non_empty_lines = [l for l in lignes if l != "\n"]
		spaced_sentences = [l.replace(".",". ") for l in non_empty_lines]
		sentences = [l.replace("\n"," ") for l in non_empty_lines]
		text = ' '.join(sentences)
		text=unicode(text)
	return text
