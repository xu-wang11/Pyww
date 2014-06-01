__author__ = 'xu'

import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *



class PFunction:
	#variable = {}
	node = None
	function = None
	vfunction = []
	compiler = None
	argnames = []
	functionName = ""
	#the function is for module or just for function
	isModule = False

	def __init__(self, ismodule, node):
		self.node = node

		self.isModule = ismodule
		if not ismodule:
			print "extract attrs"

	def bind_compiler(self, compiler, ismain = False, args = None, ret = None):
		if ismain:
			function_type = Type.function(Type.int(), [])
			self.compiler = compiler
			self.function = self.compiler.add_declare_function("main", function_type)
			bb = self.function.append_basic_block("entry")
			builder = Builder.new(bb)

			self.compiler.current_builder = builder
			self.compiler.global_builder = builder
			self.compiler.current_variables = {}
			self.compiler.set_is_main(True)
			self.compile()
		else:
			print "compile normal function"
			self.compile()

	def compile(self):
		#print self.compiler
		for item in ast.iter_child_nodes(self.node):
			if isinstance(item, ast.FunctionDef):
				func = PFunction(False, item, self, self.module)
				self.vfunction.append(func)
				print "function"
			elif isinstance(item, ast.Expr):
				print "expr"
			elif isinstance(item, ast.Assign):
				self.compiler.compile_assign(item)
			elif isinstance(item, ast.While):
				print "while"
			elif isinstance(item, ast.If):
				print "If"
			elif isinstance(item, ast.Print):
				self.compiler.compile_print(item)

			else:
				print "no idea"
		self.compiler.current_builder.ret(Constant.int(Type.int(), 0))
