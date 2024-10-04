#!/usr/bin/env python3

# coding: utf8
# we must specify the encoding as utf-8 because python2.7 default encoding is
# ascii which causes many bugs
from __future__ import unicode_literals  # this allows to have all text
# unicode rather than str, it is a Python 3 feature
import argparse
from common import get_text_from_file
from common import sentTokenize
import glob
import nltk
from similaritymeasures import *
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim import models
import codecs
import pickle
import hashlib
import collections
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-A", "--inputA", type=str, default=None,
                    help="set A input source text files: all files in inputA")
parser.add_argument("-B", "--inputB", type=str, default=None,
                    help="set B input source text files: all files in inputB")
parser.add_argument("-e", "--embeddings", type=str,
                    default="GoogleNews-vectors-negative300.bin.gz",
                    help="path to embeddings file")
parser.add_argument("-b", "--binary", type=bool, default=True,
                    help="true if embeddings file is binary")
parser.add_argument("-m", "--minsim", type=float, default=0.7,
                    help="minimum similarity value under which similarity is"
                    "considered as null")
parser.add_argument("-o", "--output", type=str,
                    help="clusters output directory")

args = parser.parse_args()


def computeMD5hash(string):
    m = hashlib.md5()
    m.update(string)
    # m.update(string)
    return m.hexdigest()


def sent_similarity(s1, s2):
    content_words_1 = [w for w in word_tokenize(s1) if w not in stop]
    content_words_1_set = set(content_words_1)
    content_words_2 = [w for w in word_tokenize(s2) if w not in stop]
    content_words_2_set = set(content_words_2)
    sim = w2v(content_words_1_set, content_words_2_set, wordmodel)
    return sim


print(f"Loading embeddings {args.embeddings}", file=sys.stderr)
wordmodelfile = args.embeddings
# wordmodel = word2vec.Word2Vec.load_word2vec_format(wordmodelfile,
wordmodel = models.KeyedVectors.load_word2vec_format(
    wordmodelfile,
    binary=args.binary)
print(f"Loading embeddings DONE", file=sys.stderr)

stop = stopwords.words('english')
filesA = [os.path.join(args.inputA, o) for o in os.listdir(args.inputA)] if args.inputA else []
filesB = [os.path.join(args.inputB, o) for o in os.listdir(args.inputB)] if args.inputB else []

# files = glob.glob(path_pattern)
for afile in filesA:
    aname = os.path.basename(afile)
    absentences = collections.defaultdict(set)
    if args.inputA:
        asentences = []
        with open(afile, "r") as af:
            # sentences=sentences+f.read().splitlines()
            asentences = map(str.strip, af.readlines())
            for i, sent in enumerate(asentences):
                absentences[str(i)+"A"] = sent
    if args.inputB:
        bfile = os.path.join(args.inputB,
                            aname.split("-A")[0]+"-B"+aname.split("-A")[1])
        with open(bfile, "r") as bf:
            # sentences=sentences+f.read().splitlines()
            bsentences = map(str.strip, bf.readlines())
            for i, sent in enumerate(bsentences):
                absentences[str(i)+"B"] = sent

    try:
        outfile = os.path.join(args.output,
                            aname.split("-A")[0]+"-AB"+aname.split("-A")[1])
    except IndexError:
        outfile = os.path.join(args.output, aname+"-AB")
    # print "sentences number"
    # print len(sentences)
    # sys.exit(0)#########
    print(outfile)
    with codecs.open(outfile, "w") as out_f:
        for i1, item1 in enumerate(absentences.items()):
            for i2, item2 in enumerate(absentences.items()):
                if i1 < i2:
                    sim = sent_similarity(item1[1], item2[1])
                    # sim=w2v_words(item1[1],item2[1],wordmodel)
                    if sim > args.minsim:
                        out_f.write(
                            item1[0]+" "+item2[0]+" "+str(sim)+"\n")
                    else:
                        out_f.write(
                            item1[0]+" "+item2[0]+" "+str(0.0)+"\n")
