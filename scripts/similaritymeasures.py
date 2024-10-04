# coding: utf8
#we must specify the encoding as utf-8 because python2.7 default encoding is ascii which causes many bugs
from __future__ import unicode_literals #this allows to have all text in unicode rather than str, it is a Python 3 feature

import nltk
from nltk import WordPunctTokenizer
from nltk.tokenize import word_tokenize
import redis
from common import *
from requests import get
import sys
import os

from contextlib import contextmanager


@contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)

#sys.path.insert(0, os.path.join(os.environ['ICSISUMM'],
                                #'monolingual-word-aligner'))
#with pushd(os.path.join(os.environ['ICSISUMM'],
                                #'monolingual-word-aligner')) as ctxt:
    #from aligner import align

from nltk.corpus import stopwords
stop = stopwords.words('english')
sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"
alphanum="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
from operator import itemgetter
import numpy as np

"""
def wordnetTextToTextSimilarity(text_1,text_2):
    if text_1 == text_2:
        return 1
    tokens_1 = WordPunctTokenizer().tokenize(text1)
    tokens_2 = WordPunctTokenizer().tokenize(text2)

    intersection = set(tokens_1) & set(tokens_2)
    commonwords = len(intersection)
    if commonwords == 0:
        return 0
    tokens_1 = WordPunctTokenizer().tokenize(text1)
    tokens_2 = WordPunctTokenizer().tokenize(text2)
    pos_tagged_text_1 = nltk.pos_tag(tokens_1)
    pos_tagged_text_2 = nltk.pos_tag(tokens_2)
    verbs_1 = [x[0] for x in pos_tagged_text_1 if x[1] in ['VBD','VBG','VB','VBN','VBP','VBZ'] ]
    nouns_1 = [x[0] for x in pos_tagged_text_1 if x[1] in ['NN','NNP','NNPS','NNS'] ]
    verbs_2 = [x[0] for x in pos_tagged_text_2 if x[1] in ['VBD','VBG','VB','VBN','VBP','VBZ'] ]
    nouns_2 = [x[0] for x in pos_tagged_text_2 if x[1] in ['NN','NNP','NNPS','NNS'] ]
"""
def sss(s1, s2, type='relation', corpus='webbase'):

    try:
        response = get(sss_url,
                 params={'operation':'api',
                         'phrase1':s1,
                         'phrase2':s2,
                         'type':type,
                         'corpus':corpus})
        #print "sim = ",float(response.text.strip())
        return float(response.text.strip())
    except:
        """
        print(s1)
        print("______________")
        print(s2)
        print("******************************")
        #print('Error in getting similarity for %s: %s' % ((s1,s2), response))
        """
        print("sss error    ")
        return 0.0

#def alignement_sim(s1,s2,ad,port): #,content_words_1,content_words_2)#,s1_parse_result,s2_parse_result):
    #print(len(s1.split()))
    #print(len(s2.split()))
    #similarity = 0
    #content_words_1 = set([w for w in word_tokenize(s1) if w not in stop])
    #content_words_2 = set([w for w in word_tokenize(s2) if w not in stop])
    #inter=len(content_words_1 & content_words_2)
    #if inter==0:
        #return 0.0
    #nc1 = len(content_words_1) #number of content words in sentence 1
    #nc2 = len(content_words_2) #number of content words in sentence 2
    #nac1 =0 #number of aligned content words in sentence 1
    #nac2 =0 #number of aligned content words in sentence 2
    #"""
    #try:
        #alignments = align(s1, s2)
    #except:
        #return 0.33
    #"""
    #print('alignement_sim: Before align')
    #"""try:
        #alignments = align(s1, s2)
    #except:
        #print("ERROR!")
        #return 0"""
    #alignments = align(s1, s2, "127.0.0.1",8083) # , s1_parse_result,s2_parse_result)
    #print('alignement_sim: After align')
    #word_alignements = alignments[1]
    #for a in word_alignements:
        #if a[0] in content_words_1:
                #nac1 += 1
        #if a[1] in content_words_2:
                #nac2 += 1
    #numerator = nac1 + nac2
    #denumerator = nc1 + nc2
    #similarity = numerator / float(denumerator)
    #print(inter , similarity)
    ##semeval_sim = similarity * 5
    ##semeval_sim = "%.2f" % semeval_sim
    #return similarity

def sentence_vector(words_set,wordmodel):
#sentence representation as the centroid of its words vectors
    firstelement=True
    for w in words_set:
        if (w in wordmodel.vocab) and (w != ''):
            if firstelement:
                firstelement=False
                vec=wordmodel[w]
                mat=[vec]
                print("shape and type of word vec")
                print(vec.shape)
                print(type(vec))
            else:
                vec=wordmodel[w]
                mat=np.append(mat,[vec], axis=0)
    print("shape of mat")
    print(mat.shape)
    print("mat")
    print(mat)
    sentvec= np.mean(mat, axis=0)
    print(sentvec)
    return sentvec



def w2v(ws1, ws2, wordmodel):
    if ws1 == ws2:
        return 1.0
    if type(ws1)!= 'set':
        ws1=set(ws1)
    for v in ws1.copy():
        if (v not in wordmodel.vocab) or (v == ''):
            #print "%s not in vocab" %(v)
            ws1.remove(v)
    if type(ws2) != 'set':
        ws2=set(ws2)
    for v in ws2.copy():
        if (v not in wordmodel.vocab) or (v == ''):
            #print "%s not in vocab" %(v)
            ws2.remove(v)
    #print ws1
    #print ws2

    intersection = ws1 & ws2

    commonwords = len(intersection)

    if commonwords == 0:
        return 0

    similarity = wordmodel.n_similarity(ws1, ws2)
    #print "sim: ", similarity
    return similarity


def bigramSim(b1,b2,wordmodel):
    if b1 ==b2:
        return 1.0
    b1=set(b1)
    for v in b1.copy():
        if (v not in wordmodel.vocab) or (v == ''):
            #print "%s not in vocab" %(v)
            b1.remove(v)
    b2=set(b2)
    for v in b2.copy():
        if (v not in wordmodel.vocab) or (v == ''):
            #print "%s not in vocab" %(v)
            b2.remove(v)

    similarity = wordmodel.n_similarity(b1, b2)
    return similarity
def w2v_words(s1, s2, wordmodel):
    if s1 == s2:
        return 1.0
    cw1 = [w for w in word_tokenize(s1) if w not in stop]
    cw2 = [w for w in word_tokenize(s2) if w not in stop]
    intersection = set(cw1) & set(cw2)

    commonwords = len(intersection)

    if commonwords == 0:
        return 0

    l1 = [word for word in cw1 if word not in intersection]
    l2 = [word for word in cw2 if word not in intersection]

    if len(l1) > len(l2):
        l1, l2 = l2, l1

    totalscore = 0

    for t1 in l1:
        sublist = []
        hasitem = False
        for i, t2 in enumerate(l2):
            # check if POS are here
            #if len(t1.split('/')) > 1:
            if True:
                # compare same POS words
                #if t1.split('/')[1][:2] == t2.split('/')[1][:2]:
                if True:
                    if t1 in wordmodel.vocab and t2 in wordmodel.vocab:
                        sublist.append((i, wordmodel.similarity(t1, t2)))
                        hasitem = True
                    # if we don't know one of the words
                    # consider them as dissimilar
                    else:
                        sublist.append((i, 0))
                else:
                    sublist.append((i, 0))
        if hasitem:
            maxitem, subscore = max(sublist, key=itemgetter(1))
            l2.pop(maxitem)
            totalscore += subscore

    num = float(commonwords + totalscore)
    denum = min(len(s1.split()), len(s2.split()))
    score = num / denum


    return score

#calculate similarity between two bigrams
#compositional similarity of distributional similarities

def w2v_bg(bg1, bg2, wordmodel):
    if bg1 == bg2:
        return 1.0
    intersection = bg1 & bg2
    commonwords=len(intersection)
    l1 = [word for word in bg1 if word not in intersection]
    l2 = [word for word in bg2 if word not in intersection]

    if len(l1) > len(l2):
        l1, l2 = l2, l1

    totalscore = 0

    for t1 in l1:
        sublist = []
        hasitem = False
        for i, t2 in enumerate(l2):
            if t1 in wordmodel.vocab and t2 in wordmodel.vocab:
                sublist.append((i, wordmodel.similarity(t1, t2)))
                hasitem = True
        if hasitem:
            maxitem, subscore = max(sublist, key=itemgetter(1))
            l2.pop(maxitem)
            totalscore += subscore

    num = float(commonwords + totalscore)
    denum = 2
    score = num / denum
    return score



def w2v_bigrams(ws1, ws2, wordmodel):
        if ws1 == ws2:
                return 1.0
        if type(ws1)!= 'set':
                ws1=set(ws1)
        for v in ws1.copy():
                if (v not in wordmodel.vocab) or (v == ''):
                        #print "%s not in vocab" %(v)
                        ws1.remove(v)
        if type(ws2) != 'set':
                ws2=set(ws2)
        for v in ws2.copy():
                if (v not in wordmodel.vocab) or (v == ''):
                        #print "%s not in vocab" %(v)
                        ws2.remove(v)
        #print ws1
        #print ws2

        intersection = ws1 & ws2

        commonwords = len(intersection)

        if commonwords == 0:
                return 0
        sent1 = np.array([wordmodel[list(ws1)[0]]])
        sent2 = np.array([wordmodel[list(ws2)[0]]])
        l1=list(ws1)
        l2=list(ws2)
        for a,b in zip(l1, l1[1:]):
                bigram=a+"_"+b
                if bigram in wordmodel.vocab:
                        sent1=np.append(sent1,[wordmodel[bigram]],0)
        for i,w in enumerate(l1) :
                if i !=0:
                        sent1=np.append(sent1,[wordmodel[w]],0)


        for a,b in zip(l2, l2[1:]):
                bigram=a+"_"+b
                if bigram in wordmodel.vocab:
                        sent2=np.append(sent2,[wordmodel[bigram]],0)
        for i,w in enumerate(l2) :
                if i !=0:
                        sent2=np.append(sent2,[wordmodel[w]],0)

        sent1=np.mean(sent1,axis=0)
        sent2=np.mean(sent2,axis=0)

        similarity = spatial.distance.cosine(sent1,sent2)
        #print "sim: ", similarity

        return similarity


