__author__ = 'xu'

import ast
from compiler import ast as yacc_ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *
import python_yacc


class PFunction:
	variable = {}
	builder = None
	node = None
	function = None
	vfunction = {}
	compiler = None
	argnames = []
	functionName = ""
	#the function is for module or just for function
	isModule = False

	def __init__(self, ismodule, node):
		self.node = node

		self.isModule = ismodule
		if not ismodule:
			for item in node.argnames:
				self.argnames.append(item)
			print "extract attrs"

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
		return_type = Type.void()
		expr_array = []
		statements = None
		if isinstance(self.node, yacc_ast.Function):
			statements = self.node.code.nodes
		else:
			statements = self.node.node.nodes
		for item in statements:
			if isinstance(item, yacc_ast.Function):
				func = PFunction(False, item)
				self.vfunction[item.name] = func
				print "function"
			else:
				expr_array.append(item)


		self.compiler.compile_block(expr_array)


		if not self.isModule and return_type == Type.void():
			self.compiler.current_builder.ret_void()
		return return_type
		#
