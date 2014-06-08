__author__ = 'xu'

from llvm.core import *
from llvm.ee import *
from llvm import *
from llvm.passes import *
from PClass import PClass


import ast


class NameManager:
	count = 0
	prefix = "str"

	def __init__(self):
		print "nameManager"

	def get_next_name(self):
		self.count += 1
		return self.prefix + str(self.count)


class Compiler:

	module = None
	global_builder = None
	global_string = {}
	current_builder = []
	global_variables = {}
	current_variables = {}
	global_class_def = {}
	variable_class = {}
	isMain = False
	names = NameManager()
	function = None


	def __init__(self, module_name, module):
		self.module = module

		self.add_global_str("%d", "printd")
		self.add_global_str("%lf", "pf")
		function_type = Type.function(Type.int(), [Type.pointer(Type.int(8))], True)
		#self.module.add_function(function_type, "printf")
		self.add_declare_function("printf", function_type)

	def output(self, writer):
		writer.write(self.module.__str__())

	def add_global_str(self, string, name=None):
		string = string + "\0"
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
			variable.initializer = Constant.null(Type.pointer(Type.int(type.pointee.width)))
		self.global_variables[name] = variable
		self.current_variables[name] = variable
		return variable

	def add_declare_function(self, function_name, type):
		return self.module.add_function(type, function_name)

	def compile_object(self, node, needLoad = [False]):
		if isinstance(node, ast.Num):
			needLoad[0] = False
			if isinstance(node.n, float):
				return Constant.real(Type.double(), node.n)
			else:
				return Constant.int(Type.int(), node.n)
		elif isinstance(node, ast.Str):
			needLoad[0] = False
			string = self.add_global_str(node.s)
			#value = self.current_builder.load(string)
			#alloc = self.current_builder.alloca(Type.pointer(Type.int(8)))
			#head = self.current_builder.gep(string, [Constant.int(Type.int(), 0), Constant.int(Type.int(), 0)])
			#self.current_builder.store(head, alloc)
			return string
		elif isinstance(node, ast.List):
			needLoad[0] = False
			list_array = node.elts
			n = len(list_array)
			alloca = self.current_builder.alloca(Type.array(Type.int(), n))
			index = Constant.int(Type.int(), 0)
			for item in list_array:
				head = self.current_builder.gep(alloca,  [Constant.int(Type.int(), 0), index])
				index = index.add(Constant.int(Type.int(), 1))
				variable = self.compile_object(item)
				self.current_builder.store(variable, head)
			return alloca


		elif isinstance(node, ast.BinOp):
			needLoad[0] = False
			return self.compile_binop(node)
		elif isinstance(node, ast.Name):
			needLoad[0] = True
			return self.get_variable(node.id)
		elif isinstance(node, ast.BoolOp):
			needLoad[0] = False
			return self.compile_bool_op(node)
		elif isinstance(node, ast.Compare):
			needLoad[0] = False
			return self.compile_compare(node)
		elif isinstance(node, ast.Subscript):
			needLoad[0] = True
			data_array = node.value.id
			variable = self.load_variable(data_array)
			index = self.compile_object(node.slice.value)
			#alloc = self.current_builder.alloca(Type.int())
			#self.current_builder.store(index, alloc)
			#index = self.current_builder.load(alloc)
			if isinstance(index.type, PointerType):
				index = self.current_builder.load(index)
			if isinstance(variable.type.pointee, ArrayType):
				#index = self.current_builder.load(index)
				head = self.current_builder.gep(variable, [Constant.int(Type.int(), 0), index])
			else:
				head = self.current_builder.gep(variable, [index])

			return head
		elif isinstance(node, ast.Call):
			needLoad[0] = True
			if hasattr(node.func, 'value'):
				function_name = node.func.attr
			else:
				function_name = node.func.id
			args = node.args
			args_types = []
			args_val = []
			real_function_name = function_name



			if hasattr(node.func, 'value'):
				obj = self.compile_object(node.func.value)
				args_val.append(obj)
				args_types.append(obj.type)
			if function_name in self.function.vfunction:
				pfunction = self.function.vfunction[function_name]
				if pfunction.isConstructFunction == True:
					real_function_name += '_' + pfunction.pclass.class_name
					class_type = pfunction.pclass.classType
					args_types.append(Type.pointer(class_type))
					class_value = self.current_builder.malloc(class_type, 'self')
					args_val.append(class_value)
			for item in args:
				variable = self.compile_object(item)
				args_type = variable.type
				if isinstance(args_type, PointerType):
					variable = self.load_variable(item.id)
					args_type = variable.type
					try:
						if isinstance(variable.type.pointee, ArrayType):
							variable = self.current_builder.gep(variable, [Constant.int(Type.int(), 0), Constant.int(Type.int(),0)])
							args_type = Type.pointer(Type.int())
					except:
						print "error"
				args_val.append(variable)
				args_types.append(args_type)
				str = self.type2string(args_type)
				real_function_name += "_" + str

			try:
				function = self.get_function(real_function_name)
				if function is None:
					print "right"
				self.current_builder.call(function, args_val)
			except Exception:
				old_function = self.function
				pfunction = self.function.vfunction[function_name]
				if pfunction is not None:
					pfunction.bind_compiler(self, False, args=args_types, name=real_function_name)
				function = self.get_function(real_function_name)
				self.current_builder = old_function.builder
				self.current_variables = old_function.variable
				self.function = old_function
				self.isMain = old_function.isModule
				if pfunction.isConstructFunction == True:
					self.current_builder.call(function, args_val)
					#self.variable_class[pfunction.pclass.class_name] =
					return class_value
				else:
					return self.current_builder.call(function, args_val)
		elif isinstance(node, ast.Attribute):
			needLoad[0] = True
			attr_name = node.attr
			needLoad = [False]
			class_var = self.compile_object(node.value, needLoad)
			if needLoad[0] == True:
				class_var = self.current_builder.load(class_var)
			class_name = class_var.type.pointee.name
			pclass = self.global_class_def[class_name]
			attr_index = pclass.variable_names.index(attr_name)
			if attr_index >= 0:
				#variable = self.current_builder.load(variable)
				shift = [Constant.int(Type.int(), 0), Constant.int(Type.int(), attr_index)]
				variable = self.current_builder.gep(class_var, shift)
			return variable


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

	def print_int(self, variable):
		print_var = self.get_variable("printd")
		function = self.get_function("printf")
		#print len(function.args)
		#ptr = Type.pointer(Type.int(8), module.getel)
		head = self.current_builder.gep(print_var,  [Constant.int(Type.int(), 0), Constant.int(Type.int(), 0)])
		#load from local variables
		if not isinstance(variable.type, IntegerType):
			value = self.current_builder.load(variable)
		else:
			value = variable
		#elif val_name in self.global_variables:
		#	value = self.current_builder.load(self.global_variables[val_name])
		args = [head, value]
		return self.current_builder.call(function, args, 'calltmp')
	def print_float(self, variable):
		print_var = self.get_variable("pf")
		function = self.get_function("printf")
		head = self.current_builder.gep(print_var,  [Constant.int(Type.int(), 0), Constant.int(Type.int(), 0)])
		value = self.current_builder.load(variable)
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
		if isinstance(node, ast.BinOp):
			if isinstance(node.left, ast.BinOp):
				temp1 = self.compile_binop(node.left)
			elif isinstance(node.left, ast.Name):
				temp1 = self.load_variable(node.left.id)

			else: #if the value is constant value
				needLoad = [False]
				temp1 = self.compile_object(node.left, needLoad)
				if needLoad[0] == True:
					temp1 = self.current_builder.load(temp1)

			if isinstance(node.right, ast.BinOp):
				temp2 = self.compile_binop(node.right)
			elif isinstance(node.right, ast.Name):
				temp2 = self.load_variable(node.right.id)
			else:
				needLoad = [False]
				temp2 = self.compile_object(node.right, needLoad)
				if needLoad[0] == True:
					temp2 = self.current_builder.load(temp2)


			if isinstance(node.op, ast.Add):
				if temp1.type == Type.int() and temp2.type == Type.int():
					temp = self.current_builder.add(temp1, temp2)
				elif temp2.type == Type.double() and temp2.type == Type.double():
					temp = self.current_builder.fadd(temp1, temp2)
			elif isinstance(node.op, ast.And):

				temp = self.current_builder.and_(temp1, temp2)

			elif isinstance(node.op, ast.Sub):
				if temp1.type == Type.int() and temp2.type == Type.int():
					temp = self.current_builder.sub(temp1, temp2)
				elif temp1.type == Type.double() and temp2.type == Type.double():
					temp = self.current_builder.fsub(temp1, temp2)
			elif isinstance(node.op, ast.Mult):
				if temp1.type == Type.int() and temp2.type == Type.int():
					temp = self.current_builder.mul(temp1, temp2)
				elif temp1.type == Type.double() and temp2.type == Type.double():
					temp = self.current_builder.fmul(temp1, temp2)
			elif isinstance(node.op, ast.Div):
				if temp1.type == Type.int() and temp2.type == Type.int():
					temp = self.current_builder.sdiv(temp1, temp2)
				elif temp1.type == Type.double() and temp2.type == Type.double():
					temp = self.current_builder.fdiv(temp1, temp2)
			elif isinstance(node.op, ast.RShift):
				temp = self.current_builder.ashr(temp1, temp2)
			else:
				print "unknown symbol"
			return temp


	def type_check(self, a, b):
			return True

	def save_value(self, a, b):
		self.current_builder.store(a, b)

	def compile_assign(self, node):
		if not isinstance(node, ast.Assign):
			print "wrong input to compile assign"
		print self.module
		target = node.targets[0]
		value = node.value
		needLoad = [False]
		right = self.compile_object(value, needLoad)
		if needLoad[0] == True:
			right = self.current_builder.load(right)
		variable = self.compile_object(target, needLoad)
		if isinstance(target, ast.Name):
			name = target.id


			#variable = self.current_builder.get
		if variable is not None:
				self.save_value(right, variable)
		else:
			if self.isMain:

				if isinstance(right.type, PointerType):
					#width = right.type.pointee.element.width
					#variable = self.add_global_variable(Type.pointer(Type.int(width)), name)
					#head = self.current_builder.gep(right, [Constant.int(Type.int(), 0), Constant.int(Type.int(), 0)])
					#self.save_value(head, variable)
					#variable.initializer = head

					aloca = self.current_builder.alloca(right.type, name=name)
					self.current_variables[name] = aloca

					self.save_value(right, aloca)
				else:
					#variable = self.add_global_variable(right.type, name)
				#self.current_variables[name] = variable
					#right = self.current_builder.load(right)
					aloca = self.current_builder.alloca(right.type, name=name)
					self.current_variables[name] = aloca
					self.save_value(right, aloca)
				#variable.initializer = self.current_builder.load(right)
					#self.save_value(right, variable)
			else:
				#right = self.current_builder.store(right)

				aloca = self.current_builder.alloca(right.type, name=name)
				self.current_variables[name] = aloca
				self.save_value(right, aloca)
		#else:
		#	left = self.compile_object(target)
		#	right = self.compile_object(node.value)
		#	self.save_value(self.current_builder.load(right), left)
		#	print "unsupport"

	def compile_print(self, node):
		for item in node.values:
			variable = self.compile_object(item)
			if isinstance(variable.type, IntegerType):
				#variable = self.compile_object(item)
				self.print_int(variable)
			elif variable.type.pointee ==Type.double():
				self.print_float(variable)

			elif isinstance(item, ast.Str):
				variable = self.compile_object(item)
				self.print_string(variable)
			else:
				variable = self.compile_object(item)

				self.print_variable(variable)

	def type2string(self, type):
		if isinstance(type, ArrayType):
			type_str = self.type2string(type.element)
			return type_str
		if isinstance(type, PointerType):
			type_str = self.type2string(type.pointee)
			return type_str+ "*"
		return str(type)

	def compile_return(self, node):
		variable = self.compile_object(node.value)
		self.current_builder.ret(variable)
		return variable.type

	def compile_argument(self, node):
		return_val = {}
		args_val = []
		args_type = []
		for item in node:
			variable = self.compile_object(item)
			args_type = variable.type
			if isinstance(variable, Constant):
				args_val.append(variable)
				args_type.append(variable.type)
			if isinstance(args_type, PointerType):
				variable = self.load_variable(item.id)
				args_type = variable.type

			args_val.append(variable)
			#args_types.append(args_type)
			str = self.compiler.type2string(args_type)
			#real_function_name += "_" + str
	def array2point(self, array):
		print "umimplement"

	def compile_if(self, node):
		condition_bool = self.compile_object(node.test)
		#condition_bool = self.current_builder.fcmp(FCMPEnum.FCMP_ONE,condition, Constant.real(Type.double(), 0), 'ifcond' )
		function = self.function.function
		then_block = function.append_basic_block('then')
		else_block = function.append_basic_block('else')
		merge_block = function.append_basic_block('ifcond')
		self.current_builder.cbranch(condition_bool, then_block, else_block)
		self.current_builder.position_at_end(then_block)
		then_value = self.compile_block(node.body)
		self.current_builder.branch(merge_block)
		self.current_builder.position_at_end(else_block)
		else_value = self.compile_block(node.orelse)
		self.current_builder.branch(merge_block)
		self.current_builder.position_at_end(merge_block)
		phi = self.current_builder.phi(Type.int(), 'iftmp')
		phi.add_incoming(Constant.int(Type.int(), 0), then_block)
		phi.add_incoming(Constant.int(Type.int(), 0), else_block)

		return phi




		print "unsupport if"

	def compile_while(self, node):


		before_block = self.function.function.append_basic_block('beforewhile')
		self.current_builder.branch(before_block)
		while_block = self.function.function.append_basic_block('while')
		after_block = self.function.function.append_basic_block('afterwhile')

		self.current_builder.position_at_end(before_block)

		condition_bool = self.compile_object(node.test)
		self.current_builder.cbranch(condition_bool, while_block, after_block)
		self.current_builder.position_at_end(while_block)
		while_value = self.compile_block(node.body)
		self.current_builder.branch(before_block)
		self.current_builder.position_at_end(after_block)
		#phi = self.current_builder.phi(Type.int(), 'itmp')
		#phi.add_incoming(condition_bool, before_block)
		#return phi





		print "unsupport while"

	def compile_block(self, node):
		return_type = Type.void()
		for item in node:
			if isinstance(item, ast.Assign):
				self.compile_assign(item)
			elif isinstance(item, ast.If):
				self.compile_if(item)
			elif isinstance(item, ast.For):
				self.compile_while(item)
			elif isinstance(item, ast.While):
				self.compile_while(item)
			elif isinstance(item, ast.Print):
				self.compile_print(item)
			elif isinstance(item, ast.Expr):
				value = item.value
				if isinstance(value, ast.Call):
					self.compile_object(value)
				elif isinstance(value, ast.UnaryOp):
					op = value.op
					if isinstance(op, ast.UAdd):
						operand = value.operand.operand.id
						alloc = self.get_variable(operand)
						value = self.current_builder.load(alloc)
						value = self.current_builder.add(value, Constant.int(Type.int(), 1))
						self.current_builder.store(value, alloc)
					elif isinstance(op, ast.USub):
						operand = value.operand.operand.id
						alloc = self.get_variable(operand)
						value = self.current_builder.load(alloc)
						value = self.current_builder.sub(value, Constant.int(Type.int(), 1))
						self.current_builder.store(value, alloc)

			elif isinstance(item, ast.Return):
				type = self.compile_return(item)
				if return_type == Type.void():
					return_type = type
				elif not self.type_check(type, return_type):
					print "don't support two different kind return value"
			elif isinstance(item, ast.ClassDef):
				classdef = PClass(item, self)
				for item in classdef.functions:
					item.selfClassName = classdef.class_name
					self.function.vfunction[item.functionName] = item
				classdef.init_function.isConstructFunction = True
				classdef.init_function.pclass = classdef
				classdef.init_function.selfClassName = classdef.class_name
				self.function.vfunction[classdef.class_name] = classdef.init_function
				self.global_class_def[classdef.class_name] = classdef
		return return_type

		#print "with solve"

	def compile_bool_op(self, node):
		if isinstance(node.op, ast.And):
			compare1 = self.compile_object(node.values[0])
			compare2 = self.compile_object(node.values[1])
			return self.current_builder.and_(compare1, compare2)
		elif isinstance(node.op, ast.Or):
			compare1 = self.compile_object(node.values[0])
			compare2 = self.compile_object(node.values[1])
			return self.current_builder.or_(compare1, compare2)
		elif isinstance(node.op, ast.Not):
			compare = self.compile_object(node.values[0])
			return self.current_builder.not_(compare)

	def compile_compare(self, node):
		if len(node.ops) != 1:
			print "error, why multi ops?"
		op = node.ops[0]
		compare2 = self.load_node(node.comparators[0])
		compare1 = self.load_node(node.left)

		if isinstance(op, ast.Lt):
			return self.current_builder.icmp(IPRED_SLT, compare1, compare2)
		elif isinstance(op, ast.Gt):
			return self.current_builder.icmp(ICMPEnum.ICMP_SGT, compare1, compare2)
		elif isinstance(op, ast.Eq):
			return self.current_builder.icmp(ICMPEnum.ICMP_EQ, compare1, compare2)
		elif isinstance(op, ast.LtE):
			return self.current_builder.icmp(ICMPEnum.ICMP_SLE, compare1, compare2)
		elif isinstance(op, ast.GtE):
			return self.current_builder.icmp(ICMPEnum.ICMP_SGE, compare1, compare2)

	def load_node(self, node):
		if isinstance(node, ast.Num):
			return Constant.int(Type.int(), node.n)
		elif isinstance(node, ast.Name):
			return self.load_variable(node.id)
		elif isinstance(node, ast.BinOp):
			return self.compile_binop(node)
		elif isinstance(node, ast.Subscript):
			head = self.compile_object(node)
			return self.current_builder.load(head)





















