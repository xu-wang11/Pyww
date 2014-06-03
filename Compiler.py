__author__ = 'xu'

from llvm.core import *
from llvm.ee import *
from llvm import *
from llvm.passes import *

import ast


class NameManager:
	count = 0
	prefix = "str"

	def __init__(self):
		print "nameManager"

	def get_next_name(self):
		++self.count
		return self.prefix + str(self.count)


class Compiler:

	module = None
	global_builder = None
	global_string = {}
	current_builder = []
	global_variables = {}
	current_variables = {}
	isMain = False
	names = NameManager()


	def __init__(self, module_name, module):
		self.module = module

		self.add_global_str("%d", "printd")
		function_type = Type.function(Type.int(), [Type.pointer(Type.int(8))], True)
		#self.module.add_function(function_type, "printf")
		self.add_declare_function("printf", function_type)

	def output(self, writer):
		writer.write(self.module.__str__())

	def add_global_str(self, string, name=None):
		for item in self.global_string:
			varu = self.global_string[item]
			if varu == string:
				return self.global_variables[item]
		if name is None:
			name = self.names.get_next_name()
			#name = 'tmp'
		variable = self.module.add_global_variable(Type.array(Type.int(8), len(string)), name=name)
		variable.initializer = Constant.string(string)
		self.global_variables[name] = variable
		self.global_string[name] = string
		return variable

	def add_global_variable(self, type, name):
		#if isinstance(type, IntegerType):
		#	type = Type.int()

		variable = self.module.add_global_variable(type, name)

		if isinstance(type, IntegerType):
			variable.initializer = Constant.int(Type.int(), 0)
		elif isinstance(type, PointerType):
			variable.initializer = Constant.null(Type.pointer(Type.int(8)))
		self.global_variables[name] = variable
		self.current_variables[name] = variable
		return variable

	def add_declare_function(self, function_name, type):
		return self.module.add_function(type, function_name)

	def compile_object(self, node):
		if isinstance(node, ast.Num):
			return Constant.int(Type.int(), node.n)
		elif isinstance(node, ast.Str):
			return self.add_global_str(node.s)
		elif isinstance(node, ast.List):
			list_array = node.elts
			n = len(list_array)

			alloca = self.current_builder.alloca(Type.array(Type.int(), n))

			index =  Constant.int(Type.int(), 0)


			for item in list_array:
				head = self.current_builder.gep(alloca,  [index, Constant.int(Type.int(), 0)])
				index = index.add(Constant.int(Type.int(), 1))
				variable = self.compile_object(item)
				self.current_builder.store(variable, head)


			return alloca

		elif isinstance(node, ast.BinOp):
			return self.compile_binop(node)
		elif isinstance(node, ast.Name):
			return self.get_variable(node.id)
		else:
			print "unsupport"

	def set_is_main(self, ismain):
		self.isMain = ismain
	def print_module(self):
		print self.module

	def get_function(self, name):
		return self.module.get_function_named(name)

	def get_variable(self, name):
		if name in self.current_variables:
			return self.current_variables[name]
		if name in self.global_variables:
			return self.global_variables[name]

	def load_variable(self, name):
		if name in self.current_variables:
			variable = self.current_variables[name]
		return self.current_builder.load(variable, name)

	def print_int(self, val_name):
		print_var = self.get_variable("printd")
		function = self.get_function("printf")
		#print len(function.args)
		#ptr = Type.pointer(Type.int(8), module.getel)
		head = self.current_builder.gep(print_var,  [Constant.int(Type.int(), 0), Constant.int(Type.int(), 0)])
		#load from local variables
		if val_name in self.current_variables:
			value = self.current_builder.load(self.current_variables[val_name])
		#elif val_name in self.global_variables:
		#	value = self.current_builder.load(self.global_variables[val_name])
		args = [head, value]
		return self.current_builder.call(function, args, 'calltmp')

	def print_variable(self, variable):
		print_var = self.get_variable("printd")
		function = self.get_function("printf")
		#print len(function.args)
		#ptr = Type.pointer(Type.int(8), module.getel)
		head = self.current_builder.gep(print_var,  [Constant.int(Type.int(), 0), Constant.int(Type.int(), 0)])
		#load from local variables

		value = self.current_builder.load(variable)
		#elif val_name in self.global_variables:
		#	value = self.current_builder.load(self.global_variables[val_name])
		args = [head, value]
		return self.current_builder.call(function, args, 'calltmp')

	def print_string(self, variable):
		head = self.current_builder.gep(variable, [Constant.int(Type.int(), 0), Constant.int(Type.int(), 0)])
		args = [head]
		function = self.get_function("printf")
		return self.current_builder.call(function, args, 'calltmp')

	def compile_binop(self, node):
		while isinstance(node, ast.BinOp):
			if isinstance(node.left, ast.BinOp):
				temp1 = self.compile_binop(node.left)
			elif isinstance(node.left, ast.Name):
				temp1 = self.get_variable(node.left.id)

			else: #if the value is constant value
				temp1 = self.compile_object(node.left)

			if isinstance(node.right, ast.BinOp):
				temp2 = self.compile_binop(node.right)
			elif isinstance(node.right, ast.Name):
				temp2 = self.get_variable(node.right.id)
			else:
				temp2 = self.compile_object(node.right)


			if isinstance(node.op, ast.Add):

				temp = self.current_builder.add(temp1, temp2)

			elif isinstance(node.op, ast.And):
				temp = self.current_builder.and_(temp1, temp2)
			elif isinstance(node.op, ast.Sub):
				temp = self.current_builder.sub(temp1, temp2)
			elif isinstance(node.op, ast.Mult):
				temp = self.current_builder.mul(temp1, temp2)
			elif isinstance(node.op, ast.Div):
				temp = self.current_builder.fdiv(temp1, temp2)
			else:
				print "unknown symbol"
			return temp


	def type_check(self, a, b):
			return a.type == b.type

	def save_value(self, a, b):
		self.current_builder.store(a, b)

	def compile_assign(self, node):
		if not isinstance(node, ast.Assign):
			print "wrong input to compile assign"
		print self.module
		target = node.targets[0]
		if isinstance(target, ast.Name):
			name = target.id
			value = node.value
			right = self.compile_object(value)

			variable = self.get_variable(name)
			if variable is not None:
				self.save_value(right, variable)
			else:
				if self.isMain:
					if isinstance(right.type, PointerType):
						variable = self.add_global_variable(Type.pointer(Type.int(8)), name)
						head = self.current_builder.gep(right, [Constant.int(Type.int(), 0), Constant.int(Type.int(), 0)])
						self.save_value(head, variable)
						#variable.initializer = head
					else:
						variable = self.add_global_variable(right.type, name)
					#self.current_variables[name] = variable

					#variable.initializer = self.current_builder.load(right)
						self.save_value(right, variable)
				else:
					#right = self.current_builder.store(right)
					aloca = self.current_builder.alloca(right.type, name=name)
					self.current_variables[name] = aloca
					self.save_value(right, aloca )

	def compile_print(self, node):
		for item in node.values:
			if isinstance(item, ast.Name):
				self.print_int(item.id)
			elif isinstance(item, ast.BinOp):
				variable = self.compile_object(item)
				aloca = self.current_builder.alloca(Type.int())
				self.save_value(variable, aloca)
				self.print_variable(aloca)
			elif isinstance(item, ast.Str):
				variable = self.compile_object(item)
				self.print_string(variable)

	def type2string(self, type):
		if isinstance(type, IntegerType):
			return "int"
		elif isinstance(type, PointerType):
			return "str"
		elif isinstance(type, ArrayType):
			return "array"
	#def compile_function(self, node):

	def compile_return(self, node):
		variable = self.compile_object(node.value)
		self.current_builder.ret(variable)
		return variable.type










