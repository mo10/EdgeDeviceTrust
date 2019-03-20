#coding:utf-8

from __future__ import division
import random
import sys
import globals
import numpy as np
from file import *
from user import *
from network import *

malicious_users = []
good_users = []
pre_trust = []
NUM_USERS = 0
NUM_FILES = 0
NUM_TRANS = 0
FILES_PER_USER = 0
USER_GOOD = 0
USER_PURE = 0
USER_COLLECTIVE = 0
USER_CAMOUFLAGE = 0 
Users = {}
Trust_network = 0
Transactions = 0
Eigenvals = 0
SIGMA = 0.00001
Total_transactions = 0
Valid_transactions = 0

#python sim.py -input ModelA10%.txt -output result.txt -dataset "D:\E\我的酷盘\实验代码\MF based Eigentrust\dataset\sub-graph.txt"
#python sim.py -input trace.txt -output result.txt -dataset "C:\Users\Xing\Desktop\MF based Eigentrust\dataset\sub-graph.txt"

def get_pre_trust():
	global pre_trust
	pre_trust = random.sample(good_users, globals.PRE_TRUST)

def parse_and_print_globals(infile):
	global NUM_USERS
	global NUM_FILES
	global NUM_TRANS
	global FILES_PER_USER
	global USER_GOOD
	global USER_PURE
	global USER_COLLECTIVE
	global USER_CAMOUFLAGE
	num = 0
	line = infile.readline()
	while line:
		if num == 0:
			NUM_USERS = int(line.split()[0])
		if num == 1:
			NUM_FILES = int(line.split()[0])
		if num == 2:
			NUM_TRANS = int(line.split()[0])
		if num == 3:
			FILES_PER_USER = int(line.split()[0])
		if num == 4:
			USER_GOOD = int(line.split()[0])
		if num == 5:
			USER_PURE = int(line.split()[0])
		if num == 6:
			USER_COLLECTIVE = int(line.split()[0])
		if num == 7:
			USER_CAMOUFLAGE = int(line.split()[0])
			break
		line = infile.readline()
		num += 1
	print "%d users" % NUM_USERS
	print "%d files" % NUM_FILES
	print "%d transactions" % NUM_TRANS
	print "%d files per user" % FILES_PER_USER
	print "%d good users" % USER_GOOD
	print "%d indepent users" % USER_PURE
	print "%d collective users" % USER_COLLECTIVE
	print "%d camouflage users" % USER_CAMOUFLAGE

def parse_users(infile):	
	global Users
	global pre_trust
	global USER_GOOD
	global USER_PURE
	global USER_COLLECTIVE
	global USER_CAMOUFLAGE
	
	#读取malicious user and good user
	if USER_PURE > 0:
		malicious_num = USER_PURE
		user_type = globals.MALICIOUS_INDEPENDENT
	elif USER_COLLECTIVE > 0:
		malicious_num = USER_COLLECTIVE
		user_type = globals.MALICIOUS_COLLECTIVE
	elif USER_CAMOUFLAGE > 0:
		malicious_num = USER_CAMOUFLAGE
		user_type = globals.MALICIOUS_CAMOUFLAGE
	
	infile.readline()
	line = infile.readline()
	num = 0	
	while num < malicious_num:
		#print line
		malicious_users.append(int(line))
		node = User(id = int(line), type = user_type)
		if not Users.has_key(int(line)):
			Users[int(line)] = node 
			num += 1
		line = infile.readline()
	print len(Users)	
	infile.next
	line = infile.readline()
	num = 0
	while num < USER_GOOD:
		# print line
		good_users.append(int(line))
		node = User(id = int(line), type = globals.GOOD)
		if not Users.has_key(int(line)):
			Users[int(line)] = node
		num += 1
		line = infile.readline()
	print len(Users)
	get_pre_trust()
	print "pre_trust"
	print pre_trust
	for id in pre_trust:	#设置pretrust
		Users[id].pre_trust = 1
	# print malicious_users
	# print len(malicious_users)
	# print good_users
	# print len(good_users)

def parse_files(infile):
	infile.next
	line = infile.readline().split()
	while True:
		if line[0] == "transactions:":
			break
		user_id = int(line[0])
		file_id = int(line[1])
		file_is_valid = int(line[2])
		f = File(file_id, file_is_valid)
		#print str(user_id) + ", " + str(file_id) + ", " + str(file_is_valid)
		line = infile.readline().split()
		Users[user_id].add_file(f)
	print line
	
def parse_network(dataset):
	global Trust_network
	Trust_network = Network(dataset, Users)
	
def parse_transactions(infile):
	global Transactions
	Transactions = []
	line = infile.readline()
	while line:
		line = line.split()
		requester = int(line[0])
		fileid = int(line[1])
		trans = [requester, fileid]
		Transactions.append(trans)
		line = infile.readline()

def source_best_user(requester, file_id):		
	global Users
	global Eigenvals
	candicates = []
	RESPONSE_NODES = [0] * globals.NUM_USERS
	for key in Users:	#对每一个user进行循环
		cond1 = Users[key].has_a_file(file_id)
		cond2 = Users[key].bwidth_avail()
		if cond1 and cond2: # user has the file and can send the file
			if Eigenvals[key,0] > SIGMA:
				if not key == requester:
					candicates.append(key)
					#print str(key) + " trust value:" + str(Eigenvals[key,0])
	#print candicates
	random.shuffle(candicates)
	
	if len(candicates) == 0:
		#print "no resource avaliable!!"
		return -1
	else:
		trust_sum = 0
		provider = 0
		for candicate in candicates:
			trust_sum += Eigenvals[candicate,0]
		#print "trust_sum: " + str(trust_sum)
		normalize = []
		sum = 0
		for candicate in candicates:
			normalize.append(Eigenvals[candicate,0]/trust_sum)
			sum+=Eigenvals[candicate,0]/trust_sum
		
		if random.random < 0.1: #10%的概率随机选取一个节点
			provider = random.sample(candicates, 1)
			#print "with 0.1 probality, select " + str(provider)
		else:
			#print candicates
			#print "normalize"
			#print normalize
			probability = random.random()
			#print "probability:" + str(probability)
			sum = 0
			for i in xrange(len(candicates)):
				sum += normalize[i]
				#print "sum: " + str(sum)
				if probability < sum:
					provider = candicates[i]
					break
			#print "with 0.9 probality, select " + str(provider)
		return provider
		
def source_rand_user(requester, file_id):
	global Users
	candicates = []
	for key in Users:	#对每一个user进行循环
		if Users[key].has_a_file(file_id):
			candicates.append(key)
	if len(candicates) == 0:
		#print "no resource avaliable!!"
		return -1
	else:
		provider = random.sample(candicates, 1)
		return provider[0]
def GenEi():
	H = []
	K = math.log(rows)
	fs = []
	print("K = %f "%(K))
	for i in xrange(0,cols):
		temp = 0.00
		for j in xrange(0,rows):
			tr = np.transpose(matrix) #转置数组
			f = matrix[j][i] / np.sum(tr[i])
			if f > 0:
				temp = temp + f * math.log(f)
		H.append((-K)*temp)

	sum_E = np.sum(H) # 计算熵
def perform_a_trans(trans):
	global Users
	global Trust_network
	global Eigenvals
	requester = int(trans[0])
	file_id = int(trans[1])
	type = Users[requester].type # the type of user with id "requester"
	if type == globals.GOOD or type == globals.MALICIOUS_INDEPENDENT or type == globals.MALICIOUS_COLLECTIVE or type == globals.MALICIOUS_CAMOUFLAGE:
		if globals.TSYS == globals.EIGEN:
			Eigenvals = Trust_network.matrix_mult()
			sum = 0
			for i in xrange(globals.NUM_USERS):
				sum += Eigenvals[i,0]
			print "sum = %f"%(sum)
			provider = source_best_user(requester, file_id)
			if provider == -1:
				return [0,0]
			else:
				Trans_happen = 1
				trans_file = Users[provider].send_a_file(file_id)	#provider发送一个file
				Users[requester].receive_a_file(trans_file, provider)
				Users[requester].feedback(Users[provider],trans_file) 
				#requester对provider进行反馈
				Trust_network.normalize(Users, requester)
				if trans_file.is_valid == 1:
					Trans_valid = 1
					return [Trans_happen, Trans_valid]
				else:
					Trans_valid = 0
					return [Trans_happen, Trans_valid]
		elif globals.TSYS == globals.NONE:
			provider = source_rand_user(requester, file_id)	
			if provider == -1:
				return [0,0]
			else:
				Trans_happen = 1
				trans_file = Users[provider].send_a_file(file_id)	#provider发送一个file
				Users[requester].receive_a_file(trans_file, provider)
				if trans_file.is_valid == 1:
					Trans_valid = 1
					return [Trans_happen, Trans_valid]
				else:
					Trans_valid = 0
					return [Trans_happen, Trans_valid]
		
if __name__ == "__main__":
	'''
	1, 读取输入文件--构建user, file
	2, 读取用户网络结构, 并根据恶意节点, 对网络进行重建
	3, 开始交易--Eigentrust进行推荐, 进行交易, 记录反馈, 根据反馈对Eigentrust进行更新
	'''
	# 首先是读取输入文件
	i = 1
	while i < len(sys.argv):
		if sys.argv[i].lower() == '-input': #input file
			globals.INPUT = sys.argv[i+1]
		elif sys.argv[i].lower() == '-dataset':
			globals.DATASET = sys.argv[i+1]
		elif sys.argv[i].lower() == '-tm':
			if sys.argv[i+1].lower() == "eigen" or sys.argv[i+1].lower() == "eigentrust":
				globals.TSYS = globals.EIGEN
			elif sys.argv[i+1].lower() == "none" or sys.argv[i+1].lower() == "no":
				globals.TSYS = globals.NONE
			elif sys.argv[i+1].lower() == "eigentrust++":
				globals.TSYS = EIGENPLUS
		elif sys.argv[i] == "-output": #output file
			globals.RESULT = sys.argv[i+1]
		elif sys.argv[i] == "-warmup":
			globals.WARMUP = int(argv[i+1])
		else:
			print "\nRequired argument missing. Aborting."
			break
		i += 2
	input = globals.INPUT
	output = globals.RESULT
	if input == "":	#means input file is empty
		print "input shoudn't be empty!"
		exit()
	if output == "": #means output file is empty 
		print "output shoudn't be empty"
		exit()
	infile = open(input, 'r')
	outfile = open(output, 'w')
	parse_and_print_globals(infile)
	parse_users(infile)
	print "total user"
	print len(Users)
	# for key in Users:
		# print "user id:" + str(Users[key].id) + ", type:" + str(Users[key].type)
	parse_files(infile)
	parse_network(globals.DATASET)
	parse_transactions(infile)
	
	cycle = 0
	TimeWindow = 1000
	
	
	########warmup process训练用户之间的信任关系	
	Total_transactions_warmup = 0
	Valid_transactions_warmup = 0
	for cycle in xrange(0, 4000):
		#print "WARMUP: " +str(cycle)
		trans = Transactions[cycle]
		Trans_happen, Trans_valid = perform_a_trans(trans)
		print "len = %d"%len(Eigenvals)
		Total_transactions_warmup += Trans_happen
		Valid_transactions_warmup += Trans_valid	
		#if Trans_happen == 1 and Trans_valid == 0:
		#	print trans
		
	print "Total_transactions_warmup " + str(Total_transactions_warmup)
	print "Valid_transactions_warmup " + str(Valid_transactions_warmup) 
	print Valid_transactions_warmup / Total_transactions_warmup
		
	rounds = 10
	for round in xrange(0, rounds):
		Total_transactions = 0
		Valid_transactions = 0
		for user in Users:
			Users[user].clean()
		round = rounds%5
		from_cycle = 4000 * round
		to_cycle = 4000 * (round+1)
		for cycle in xrange(from_cycle, to_cycle):
			#print "WARMUP: " +str(cycle)
			trans = Transactions[cycle]
			Trans_happen, Trans_valid = perform_a_trans(trans)
			Total_transactions += Trans_happen
			Valid_transactions += Trans_valid	
			#if Trans_happen == 1 and Trans_valid == 0:
			#	print trans
		
		print "Total_transactions " + str(Total_transactions)
		print "Valid_transactions " + str(Valid_transactions)
		print Valid_transactions / Total_transactions
	
#明天任务为：1，节点的localtrust设置，2，Eigentrust更新，3，add_file需根据file类型进行文件的保存			
	

	
		
		
		
		
		
		
		