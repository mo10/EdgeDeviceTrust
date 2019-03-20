#coding:utf-8

from __future__ import division
import random
import sys
import globals
from file import *
from user import *
from network import *


class Relation(object):
	# int* pos;	// Should be for access calls 
	# int* neg;
	# int global_pos; // Should be used for update calls
	# int global_neg;
	# int honest_pos;
	# int honest_neg;
	# float trust_val;
	def __init__(self):
		self.global_pos = 0 # 有效文件的数量
		self.global_neg = 0	# 无效文件的数量
		self.trust_val = 0  # local trust
	
	def trust_cal(self):
		pass