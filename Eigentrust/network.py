#coding:utf-8
from __future__ import division
from globals import *
import random
import numpy as np
import math
class Network(object):
	def __init__(self, input, Users):
		#print input
		self.filename = input
		self.file = open(self.filename, 'r')
		self.trust = np.mat(np.zeros((NUM_USERS,NUM_USERS)))
		self.size = len(self.trust)
		self.Users = Users
		#print self.trust
		print "trss"
		print len(self.trust)
		for line in self.file.readlines():
			line = line.split()
			requester = int(line[0])
			provider = int(line[1])
			#根据dataset初始化用户的localtrust
			Users[requester].rel_vec[provider].global_pos = 1
			Users[provider].rel_vec[requester].global_pos = 1
			self.trust[requester, provider] = 1
			self.trust[provider, requester] = 1
			#print "mat: (%d, %d) set to be 1" % (requester, provider)
		self.pre_trust()
		self.initialize()
	
	def initialize(self):
		col_sum = []
		for col in xrange(NUM_USERS):
			sum = 0
			for row in xrange(NUM_USERS):
				sum += self.trust[row, col]
			col_sum.append(sum)
		
		for col in xrange(NUM_USERS):
			for row in xrange(NUM_USERS):
				self.trust[row, col] = self.trust[row, col] / col_sum[col]
	
	#对单独的列进行更新
	def normalize(self, UsersSet, requester):	#如果requester > 0, 则对指定的列进行更新, 否则对所有的用户都进行更新
		col_sum = 0
		for provider in xrange(0, NUM_USERS):
			fback_int = UsersSet[requester].fback_int(provider)
			col_sum += fback_int
			self.trust[provider,requester] = fback_int
		
		if col_sum == 0:
			for provider in xrange(0, NUM_USERS):
				self.trust[provider, requester] = self.pretrust_vec[provider]
		else:
			for provider in xrange(0, NUM_USERS):
				self.trust[provider, requester] = self.trust[provider, requester] / col_sum
				#if self.trust[provider, requester] / col_sum > 0:
				#	print "(%d, %d) = %f" % (provider, requester,self.trust[provider, requester] / col_sum)
				
	def pre_trust(self):	#创建pre_trust向量
		self.pretrust_vec = [0]*self.size
		for i in xrange(0, self.size):
			if self.Users[i].pre_trust == 1:
				self.pretrust_vec[i] = 1 / PRE_TRUST
			#self.pretrust_vec[i] = 1 / NUM_USERS
		print self.pretrust_vec
	def CalcG(self,matrix,cols,rows):
		H = []
		K = math.log(rows)
		fs = []
		print("K = %f "%(K))
		for i in xrange(0,cols):
			temp = 0.00
			for j in xrange(0,rows):
				tr = np.transpose(matrix) 
				f = matrix[j,i] / np.sum(tr[i])
				if f > 0:
					temp = temp + f * math.log(f)
			H.append((-K)*temp)

		sum_E = np.sum(H) 

		W = []
		for x in xrange(0,cols):
			w = (1.0 - H[x]) / (cols - sum_E)
			W.append(w)
		DW = np.zeros((rows, cols))
		for i in xrange(0,rows):
			for j in xrange(0,cols):
				DW[i][j] = matrix[i,j] * W[j]
		Fbk = []
		for x in xrange(0,cols):
			Fbk.append(np.sum(np.transpose(DW)[x]))

		Gdi = self.G(cols,rows,matrix,Fbk)
		return Gdi
	def G(self,cols,rows,Dset,Fbk):
		Gdi = []
		for row in xrange(0,rows):
			for col in xrange(0,cols):
				Gdi.append(0.5 * Dset[row,col] + (1 - 0.5)*Fbk[col])
		print(len(Gdi))
		return Gdi
	def matrix_mult(self):
		# self.Eigenvec = np.mat(self.pretrust_vec).T
		# print(self.trust)
		# max_iters = 8
		# print len(self.pretrust_vec)
		# for i in xrange(0, max_iters):
			
		# 	self.Eigenvec = self.trust * self.Eigenvec
		# 	# print type(self.trust)
		
		self.Eigenvec = self.CalcG(self.trust,NUM_USERS,NUM_USERS)
		sum = 0
		self.Eigenvec = np.mat(self.Eigenvec)
		print(len(self.Eigenvec))
		return self.Eigenvec



				
				