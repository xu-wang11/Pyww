__author__ = 'xu'

import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *
from PVariable import PVariable

from util import *


class PModule:
	function = []
	variable = []
	expression = []
	astModule = 0
	llvmModule = 0

	def __init__(self, astmodule, llvmmodule):
		self.astModule = astmodule
		self.llvmModule = llvmmodule
		if not isinstance(llvmmodule, Module):
			print "not llvm::module"

	def compile(self):
		for item in ast.iter_child_nodes(self.astModule):
			if isinstance(item, ast.FunctionDef):
				func = PFunction(item)
				self.function.append(func)
				print "function"
			elif isinstance(item, ast.Expr):
				print "expr"
			elif isinstance(item, ast.Assign):
				name = item.targets[0].id
				module = self.llvmModule
				if isinstance(item.value, ast.Num):
					val = item.value.n
				elif isinstance((item.value, ast.BinOp)):
					val = 0
				type = getTypeFromAST(item)
				variable = module.get_global_variable_named(name)
				if not variable:
					variable = GlobalVariable.new(module, type, name)
				if




				print "assign"
			elif isinstance(item, ast.While):
				print "while"
			elif isinstance(item, ast.If):
				print "If"
			else:
				print "no idea"
		print module







