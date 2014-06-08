__author__ = 'xu'

import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *
from types import ListType



class PFunction:
	variable = None
	builder = None
	node = None
	function = None
	vfunction = None
	compiler = None
	argnames = None
	argtypes = None
	functionName = None
	#the function is for module or just for function
	isModule = False
	expr_array = None
	isConstructFunction = False
	selfClassName = None
	pclass = None


	def __init__(self, ismodule, node):
		self.variable = {}
		self.vfunction = {}
		self.argnames = []
		self.argtypes = []
		self.expr_array = []
		self.functionName = ""
		self.selfClassName = ""
		self.node = node

		self.isModule = ismodule
		if not ismodule:
			for item in node.args.args:
				self.argnames.append(item.id)
			print "extract attrs"


	def extract_function(self):
		for item in ast.iter_child_nodes(self.node):
			if isinstance(item, ast.FunctionDef):
				func = PFunction(False, item)
				self.vfunction[item.name] = func
				print "function"
			else:
				self.expr_array.append(item)

	def bind_compiler(self, compiler, ismain = False, args = None, ret = None, name=None):
		if ismain:
			function_type = Type.function(Type.int(), [])
			self.compiler = compiler
			self.function = self.compiler.add_declare_function("main", function_type)
			bb = self.function.append_basic_block("entry")
			self.builder = Builder.new(bb)
			self.compiler.function = self
			self.compiler.current_builder = self.builder
			self.compiler.global_builder = self.builder
			self.variable = {}
			self.compiler.current_variables = self.variable
			self.compiler.set_is_main(True)
			self.compile()
			self.compiler.current_builder.ret(Constant.int(Type.int(), 0))
		else:
			#guess function return type is int
			function_type = Type.function(Type.void(), args)
			self.compiler = compiler
			self.function = self.compiler.add_declare_function(name, function_type)
			self.compiler.function = self
			bb = self.function.append_basic_block("entry")
			self.builder = Builder.new(bb)
			self.compiler.current_builder = self.builder
			self.variable = {}
			self.compiler.current_variables = self.variable
			self.compiler.set_is_main(False)
			#print "compile normal function"
			ret_type = self.compile(args)
			if(ret_type != Type.void()):
				self.function.delete()
				function_type = Type.function(ret_type, args)

				self.function = self.compiler.add_declare_function(name, function_type)
				self.compiler.function = self
				#print "compile normal function"
				bb = self.function.append_basic_block("entry")
				self.builder = Builder.new(bb)
				self.compiler.current_builder = self.builder
				self.compiler.current_variables = self.variable
				ret_type = self.compile(args)


	def compile(self, types=[]):
		arg_size = len(self.argnames)

		if(len(types) == len(self.argnames)):
			arg_values = self.function.args

			for item in range(0, arg_size):
				alloca = self.compiler.current_builder.alloca(types[item], name=self.argnames[item])
				self.compiler.current_builder.store(arg_values[item], alloca)
				#if item == IntegerType:
				#print 'error'

				self.compiler.current_variables[self.argnames[item]]= alloca


		#print self.compiler

		if self.isConstructFunction == True:
			index = Constant.int(Type.int(), 0)
			n = len(self.pclass.variable_init)
			for i in range(0, n):

				variab = self.compiler.current_builder.load(self.compiler.current_variables['self'])
				head = self.compiler.current_builder.gep(variab, [Constant.int(Type.int(), 0), index])
				index = index.add(Constant.int(Type.int(), 1))

				self.compiler.current_builder.store(self.pclass.variable_init[i], head)
		return_type = Type.void()
		self.expr_array = []
		self.extract_function()
		return_type = self.compiler.compile_block(self.expr_array)


		if not self.isModule and return_type == Type.void():
			self.compiler.current_builder.ret_void()
		return return_type
		#
