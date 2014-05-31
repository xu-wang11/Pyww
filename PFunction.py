__author__ = 'xu'

import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *

class PFunction:
	variable = []
	parent = 0
	node = 0
	function = []
	module = 0
	builder = 0

	def __init__(self, node, parent, module):
		self.node = node
		self.parent = parent
		self.module = module
		if isinstance(module, Module):
			func = module.add_function(Type.int(), Type.int())
