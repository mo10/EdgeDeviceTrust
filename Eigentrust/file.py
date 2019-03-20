from __future__ import division
import globals
import random

class File(object):
	id = 0
	is_valid = 0
	def __init__(self, id, type):
		self.id = id
		self.is_valid = type