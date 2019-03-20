#coding:utf-8
from __future__ import division
import globals
import random
from file import *
from relation import *

class User(object):
	#id = 0 		
	#type = 0	
	# 0 means good, 1 means independent malicious, 2 means collective malicious, 3 means camouflage malicious, 4 means spies malicious
	#r_honest = 1
	# the probability of rating honestly
	#p_honest = 1
	# the probability of honestly providing good file
	#s_valid = 0
	# the probability of storing a valid file
	#s_invalid = 0
	#filelist = []
	# the list of files owned by a user
	def __init__(self, id, type, camouflage=0.5, spy = 0.5, pre_trust = 0):
		self.id = id
		self.type = type
		self.filelist = {}
		self.rel_vec = []
		for i in xrange(0,globals.NUM_USERS): 
		#initial the local rating
			rel = Relation()
			self.rel_vec.append(rel)
		
		if type == globals.GOOD:
			self.r_honest = 1
			self.p_honest = 0.95
			self.s_valid = 1
			self.s_invalid = 0
			self.bandwidth = globals.BAND_WIDTH		 # the current handwidth
			self.total_bandwidth = globals.BAND_WIDTH # the total bandwidth
			self.pre_trust = pre_trust
		if type == globals.MALICIOUS_INDEPENDENT:
			self.r_honest = 1
			self.p_honest = 0
			self.s_valid = 0
			self.s_invalid = 1
			self.bandwidth = globals.BAND_WIDTH
			self.total_bandwidth = globals.BAND_WIDTH
			self.pre_trust = 0
		if type == globals.MALICIOUS_COLLECTIVE:
			#print "user " + str(self.id) + "is a malicious collective user"
			self.r_honest = 0
			self.p_honest = 0
			self.s_valid = 0
			self.s_invalid = 1
			self.bandwidth = globals.BAND_WIDTH
			self.total_bandwidth = globals.BAND_WIDTH
			self.pre_trust = 0
		if type == globals.MALICIOUS_CAMOUFLAGE:
			self.r_honest = 0
			self.p_honest = camouflage
			self.s_valid = 1
			self.s_invalid = 1
			self.bandwidth = globals.BAND_WIDTH
			self.total_bandwidth = globals.BAND_WIDTH
			self.pre_trust = 0
			self.camouflage = 0.5
			print "user " + str(self.id) + "is a malicious camouflage user with " + str(self.camouflage) + "% prbability to provide valid file"
		if type == globals.MALICIOUS_SPIES:
			if random.random() < spy:	#the probability of being a spy
				self.r_honest = 1
				self.p_honest = 0.95
				self.s_valid = 1
				self.s_invalid = 0
				self.bandwidth = globals.BAND_WIDTH
				self.total_bandwidth = globals.BAND_WIDTH
				self.pre_trust = 0
			else:
				self.r_honest = 0
				self.p_honest = 0
				self.s_valid = 0
				self.s_invalid = 1
				self.bandwidth = globals.BAND_WIDTH
				self.total_bandwidth = globals.BAND_WIDTH
				self.pre_trust = 0
	def add_file(self, file):	# the user add a file into the file list
		file = File(file.id, file.is_valid)
		if not self.has_a_file(file.id):
			self.filelist[file.id] = file
			#print "user " + str(self.id) + " add a file (" + str(file.id) + "," + str(file.is_valid) + ")" 
	
	def receive_a_file(self, file, provider):	#user接受一个文件
		file = File(file.id, file.is_valid)
		# print "user %d receives an file from %d" % (self.id, provider)
		if not self.has_a_file(file.id):
			# print "user (%d, %d) plans to add a file (%d, %d)" % (self.id, self.type, file.id, file.is_valid)
			if file.is_valid == 1:	# 如果是有效文件
				if random.random() < self.s_valid:
					self.filelist[file.id] = file
					#print "user " + str(self.id) + " receives a file (" + str(file.id) + "," + str(file.is_valid) + ")" 
			else:
				if random.random() < self.s_invalid:
					self.filelist[file.id] = file
					#print "user " + str(self.id) + " receives a file (" + str(file.id) + "," + str(file.is_valid) + ")" 
					
	def has_a_file(self, file_id): 	# check whether the user has a file with the id number
		return self.filelist.has_key(file_id) 
	
	def bwidth_avail(self):
		if self.bandwidth > 0:
			return True
		else:
			return False
				
	def send_a_file(self, file_id):
		if self.has_a_file(file_id):
			self.bandwidth = self.bandwidth - 1 
			# the handwidth will decrease by 1 for sending a file
			if self.type == globals.MALICIOUS_CAMOUFLAGE:
				if random.random() < self.camouflage:	# provide honestly
					return File(file_id, globals.VALID)
				else:
					return File(file_id, globals.INVALID)
			#print "%d user sends a %d file" %(self.id, file_id)
			return self.filelist[file_id]
		else:
			#print "%d user sends a %d file" %(self.id, file_id)
			pass
	
	def clean(self):	#重新设置一些参数
		self.bandwidth = self.total_bandwidth
		
	def feedback(self, provider, file):
		provider_id = provider.id
		if self.type == globals.MALICIOUS_CAMOUFLAGE:
			if provider.type == globals.MALICIOUS_CAMOUFLAGE:
				self.rel_vec[provider_id].global_pos += 1
			else:
				self.rel_vec[provider_id].global_neg += 1	
		elif self.type == globals.GOOD or self.type == globals.MALICIOUS_INDEPENDENT or self.type == globals.MALICIOUS_COLLECTIVE:	
			r = random.random()
			if file.is_valid == globals.VALID:
				if r < self.r_honest:
					self.rel_vec[provider_id].global_pos += 1
				else:
					self.rel_vec[provider_id].global_neg += 1
			else:	#如果是无效文件
				if r < self.r_honest:	#进行诚实反馈
					self.rel_vec[provider_id].global_neg += 1
				else:	#进行不诚实反馈
					self.rel_vec[provider_id].global_pos += 1
			#print "%d:(%d, %d)" % (provider, self.rel_vec[provider].global_pos, self.rel_vec[provider].global_neg)
	def fback_int(self, provider):
		fback = self.rel_vec[provider].global_pos -	self.rel_vec[provider].global_neg
		if fback < 0:
			fback = 0
		return fback
		
		#print "user " + str(self.id)
		#for provider in xrange(globals.NUM_USERS):
		#	if self.rel_vec[provider].global_pos > 0 or self.rel_vec[provider].global_neg > 0:
		#		print "user " + str(provider) + ": " + str(self.rel_vec[provider].global_pos) + ", " + str(self.rel_vec[provider].global_neg)
		#print "(global_pos, global_neg) of %d provider for %d user is (%d, %d)" % (provider, self.id, self.rel_vec[provider].global_pos, self.rel_vec[provider].global_neg)
		
	def show_files(self):
		print "user " + str(self.id)
		print "total " + str(len(self.filelist)) + " files."
		for file in self.filelist:
			print "("+str(self.filelist[file].id)+","+str(self.filelist[file].is_valid)+") ",
		print ""	
			