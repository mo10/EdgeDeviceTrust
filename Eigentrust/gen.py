#coding:utf-8

from __future__ import division
import random
import sys
import globals

malicious_users = []
good_users = []


def print_header(output):
	text = str(globals.NUM_USERS) + " Users" + "\n" 
	output.write(text)
	text = str(globals.NUM_FILES ) + " Files" + "\n"
	output.write(text)
	text = str(globals.NUM_TRANS) + " Transactions" + "\n" 
	output.write(text)
	text = str(globals.FILES_PER_USER) + " Files Per User" + "\n"
	output.write(text)
	text = str(globals.USER_GOOD) + " Well-Behaved (Good) Users"  + "\n"
	output.write(text)
	text = str(globals.USER_PURE) + " Indepent Malicious Users"  + "\n"
	output.write(text)
	text = str(globals.USER_COLLECTIVE) + " Collective Malicious Users" + "\n"
	output.write(text)
	text = str(globals.USER_CAMOUFLAGE) + " Camouflage Malicious Users" + "\n"
	output.write(text)
	
def generate_users(num_malicious, output):#生成USER_PURE个恶意用户
	malicious_users = []
	output.write("malicious_users:\n")
	if globals.NUM_USERS > 0:
		malicious_users = sorted(random.sample(range(0, globals.NUM_USERS), num_malicious))
		for user in malicious_users:
			output.write(str(user) + "\n")
	
	for i in xrange(0, globals.NUM_USERS):
		if i not in malicious_users:
			good_users.append(i)
	output.write("good_users: \n")
	for user in good_users:
		output.write(str(user) + "\n")
	
def generate_files(output):
	output.write("files:\n")
	for i in xrange(0, globals.NUM_USERS):
		if i in good_users:
			valid = 1
		else:
			valid = 0
		files = sorted(random.sample(range(0, globals.NUM_FILES), globals.FILES_PER_USER))
		for j in files:
			text = "%d %d %d \n" % (i, j, valid)
			output.write(text)
			
def generate_transactions(output):
	output.write("transactions:\n")
	round = int(globals.NUM_TRANS / globals.NUM_USERS)
	for i in xrange(0, round):
		for recv in xrange(0, globals.NUM_USERS):
			file = random.randint(0, globals.NUM_FILES)
			text = "%d %d \n" % (recv, file)
			output.write(text)
			file = random.randint(0, globals.NUM_FILES)
			text = "%d %d \n" % (recv, file)
			output.write(text)
			file = random.randint(0, globals.NUM_FILES)
			text = "%d %d \n" % (recv, file)
			output.write(text)
			file = random.randint(0, globals.NUM_FILES)
			text = "%d %d \n" % (recv, file)
			output.write(text)
			
if __name__ == "__main__":
	'''
	1, 攻击类型, 恶意节点数量--据此初始化用户
	2, 初始化用户拥有的文件
	3, 初始化交易
	'''
	i = 1
	print sys.argv
	# 处理arguments
	# python gen.py -file 2000 -trans 20000 -files_per_user 15 -user:purely 100
	while i < len(sys.argv):
		if sys.argv[i].lower() == '-file': 
			globals.NUM_FILES = int(sys.argv[i+1])
		elif sys.argv[i].lower() == '-trans':
			globals.NUM_TRANS = int(sys.argv[i+1])
		elif sys.argv[i].lower() == '-files_per_user':
			globals.FILES_PER_USER = int(sys.argv[i+1])
		elif sys.argv[i].lower() == '-user:purely':
			globals.USER_PURE = int(sys.argv[i+1])
		elif sys.argv[i].lower() == '-user:collective':
			globals.USER_COLLECTIVE = int(sys.argv[i+1])
		elif sys.argv[i].lower() == '-user:camouflage':
			globals.USER_CAMOUFLAGE = int(sys.argv[i+1])
		elif sys.argv[i].lower() == '-output':
			globals.OUTPUT = sys.argv[i+1]
		else:
			print "\nInvalid argument structure. Aborting.\n\n"
			break
		i += 2
	
	if globals.USER_PURE > 0:	
		globals.USER_GOOD = globals.NUM_USERS - globals.USER_PURE
	elif globals.USER_COLLECTIVE > 0:
		globals.USER_GOOD = globals.NUM_USERS - globals.USER_COLLECTIVE
	elif globals.USER_CAMOUFLAGE > 0:
		globals.USER_GOOD = globals.NUM_USERS - globals.USER_CAMOUFLAGE
		
	file = open(globals.OUTPUT, 'w')
	print_header(file)
	if globals.USER_PURE > 0:
		generate_users(globals.USER_PURE, file)
	elif globals.USER_COLLECTIVE > 0:
		generate_users(globals.USER_COLLECTIVE, file)
	elif globals.USER_CAMOUFLAGE > 0:
		generate_users(globals.USER_CAMOUFLAGE, file)
	generate_files(file)
	generate_transactions(file)
	
	
	
	