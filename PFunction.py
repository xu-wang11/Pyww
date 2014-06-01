__author__ = 'xu'

import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *
from PAssign import PAssign


class PFunction:
	variable = {}
	parent = None
	node = None
	function = None
	module = None
	builder = None
	argnames = []
	functionName = ""
	#the function is for module or just for function
	isModule = True
	def __init__(self, ismodule, node, parent, module):
		self.node = node
		self.parent = parent
		self.module = module
		self.isModule = ismodule
		if isinstance(module, Module):
			if self.isModule:
				function = Type.function(Type.void(), [])
				func = module.add_function(function, "main")
				self.function = func
			else:
				print "agrs"
			bb = func.append_basic_block("entry")
			self.builder = Builder.new(bb)

	def compile(self, args = None, ret=None):
		for item in ast.iter_child_nodes(self.node):
			if isinstance(item, ast.FunctionDef):
				func = PFunction(False, item, self, self.module)
				self.function.append(func)
				print "function"
			elif isinstance(item, ast.Expr):
				print "expr"
			elif isinstance(item, ast.Assign):
				assign = PAssign(self.isModule, item, self, self.builder, self.module)
				assign.compile()

				print "assign"
			elif isinstance(item, ast.While):
				print "while"
			elif isinstance(item, ast.If):
				print "If"
			elif isinstance(item, ast.Print):
				for content in item.values:
					if isinstance(content, ast.Name):
						if content.id in self.variable:

							str = self.module.get_global_variable_named("printd")

							function = self.module.get_function_named("printf")
							#print len(function.args)
							#ptr = Type.pointer(Type.int(8), module.getel)
							head = self.builder.gep(str,  [Constant.int(Type.int(), 0), Constant.int(Type.int(), 0)])
							value = self.builder.load(self.variable[content.id])
							args = [head, value]
							if isinstance(value.type, IntegerType):
								self.builder.call(function, args, 'calltmp')
						else:
							print "error!"

			else:
				print "no idea"
		self.builder.ret_void()
