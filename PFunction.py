__author__ = 'xu'

import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *



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
			for item in node.args.args:
				self.argnames.append(item.id)
			print "extract attrs"

	def bind_compiler(self, compiler, ismain = False, args = None, ret = None, name=None):
		if ismain:
			function_type = Type.function(Type.int(), [])
			self.compiler = compiler
			self.function = self.compiler.add_declare_function("main", function_type)
			bb = self.function.append_basic_block("entry")
			self.builder = Builder.new(bb)

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
			bb = self.function.append_basic_block("entry")
			self.builder = Builder.new(bb)
			self.compiler.current_builder = self.builder
			self.compiler.current_variables = self.variable
			#print "compile normal function"
			ret_type = self.compile()
			if(ret_type != Type.void()):
				self.function.delete()
				function_type = Type.function(ret_type, args)
				self.function = self.compiler.add_declare_function(name, function_type)
				#print "compile normal function"
				bb = self.function.append_basic_block("entry")
				self.builder = Builder.new(bb)
				self.compiler.current_builder = self.builder
				self.compiler.current_variables = self.variable
				ret_type = self.compile()


	def compile(self):
		#print self.compiler
		return_type = Type.void()
		for item in ast.iter_child_nodes(self.node):
			if isinstance(item, ast.FunctionDef):
				func = PFunction(False, item)
				self.vfunction[item.name] = func
				print "function"
			elif isinstance(item, ast.Expr):
				value = item.value
				if isinstance(value, ast.Call):
					function_name = value.func.id
					args = value.args
					args_types = []
					args_val = []
					real_function_name = function_name
					for item in args:
						variable = self.compiler.get_variable(item.id)
						args_type = variable.type
						value = self.compiler.load_variable(item.id)
						args_val.append(value)
						args_types.append(args_type)
						str = self.compiler.type2string(args_type)
						real_function_name += "_" + str
					try:
						function = self.compiler.get_function(real_function_name)
						if function is None:
							print "right"
					except Exception:
						pfunction = self.vfunction[function_name]
						if pfunction is not None:
							pfunction.bind_compiler(self.compiler, False, args=args_val, name=real_function_name)
						function = self.compiler.get_function(real_function_name)
						self.compiler.current_builder = self.builder
						self.compiler.current_variables = self.variable
						self.compiler.current_builder.call(function, [])

			elif isinstance(item, ast.Assign):
				self.compiler.compile_assign(item)
			elif isinstance(item, ast.While):
				print "while"
			elif isinstance(item, ast.If):
				print "If"
			elif isinstance(item, ast.Print):
				self.compiler.compile_print(item)
			elif isinstance(item, ast.Return):
				type = self.compiler.compile_return(item)
				if return_type == Type.void():
					return_type = type
				elif not self.compiler.type_check(type, return_type):
					print "don't support two different kind return value"


			else:
				print "no idea"
		if not self.isModule and return_type == Type.void():
			self.compiler.current_builder.ret_void()
		return return_type
		#
