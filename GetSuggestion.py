#-*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# Name:		  
# Purpose:
#
# Author:		wujc
#
# Created:	  05/12/2013
# Copyright:	(c) wujc 2013
# Licence:	  <your licence>
#-------------------------------------------------------------------------------

# import pickle
# from time import ctime
import json,pymongo
mc = pymongo.Connection('lost.nlpweb.org')
db = mc['writeahead']
wu = db.WUniDic
pu = db.PUniDic
wb = db.WBiDic
pb = db.PBiDic

def getWordSuggestion(q):
	##先根據Bigram概念來進行查詢
	words = q.split()

	if len(words) == 1: ##只有一個字(片段)
		prefix = words[0]
		try:
			return list(wu.find({'prefix':prefix}, {'_id':0, 'suggestion':1}))[0][u'suggestion']
		except:
			return []
	if len(words) > 1: ##有Ngram可以參考
		preword = words[-2]
		prefix = words[-1]
		try:
			return list(wb.find({'preword':preword, 'prefix':prefix}, {'_id':0, 'suggestion':1}))[0][u'suggestion']
		except: ##沒有 bigram可參考 改Unigram
			try:
				return list(wu.find({'prefix':prefix}, {'_id':0, 'suggestion':1}))[0][u'suggestion']
			except:
				return []


def getPhraseSuggestion(q):
	##先根據Bigram概念來進行查詢
	words = q.strip().split()

	if len(words) == 1: ##只有一個字(片段)
		preword = words[0]
		try:
			return list(pu.find({'preword':preword}, {'_id':0, 'suggestion':1}))[0][u'suggestion']
		except:
			return []
	if len(words) > 1: ##有Ngram可以參考
		preword = " ".join(words[-2:])
		try:
			return list(pb.find({'preword':preword}, {'_id':0, 'suggestion':1}))[0][u'suggestion']
			# return PBiDic[preword]
		except: ##沒有 bigram可參考 改Unigram
			try:
				return list(pu.find({'preword':preword}, {'_id':0, 'suggestion':1}))[0][u'suggestion']
			except:
				return []

# print 'loading dictionary',ctime()
# WUniDic = pickle.load(open("AANUni.pkl"))
# WBiDic = pickle.load(open("AANBi.pkl"))
# PUniDic = pickle.load(open("AAN_PhraseUni.pkl"))
# PBiDic = pickle.load(open("AAN_PhraseBi.pkl"))
# print 'Done',ctime()

# print getWordSuggestion("pro")
# print getWordSuggestion("we pro")
# print getPhraseSuggestion("propose")
# print getPhraseSuggestion("we propose")
# if __name__ == '__main__':
	 
# 	while True:
# 		q = raw_input("give me a string: ").strip()

# 		Wsuggestions = getWordSuggestion(q)
# 		Psuggestions = getPhraseSuggestion(q)
# 		print "word suggestion:"
# 		print " // ".join(Wsuggestions)
# 		print "phrase suggestion:"
# 		print " // ".join(Psuggestions)