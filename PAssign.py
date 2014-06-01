__author__ = 'xu'
import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *


class PAssign:
	sentence = None
	parent = None
	module = None
	builder = None
	isModule = False
	def __init__(self, ismodule, astsent, parent, builder, module):
		self.sentence = astsent
		self.parent = parent
		self.module = module
		self.builder = builder
		self.isModule = ismodule


	def compile_binop(self, item, count, istop, name):

		while isinstance(item, ast.BinOp):
			if isinstance(item.left, ast.BinOp):
				temp1 = self.compile_binop(item.left, count, False, name)
			elif isinstance(item.left, ast.Name):
				temp1 = self.builder.load(self.parent.variable[item.left.id], item.left.id)
				#temp1 = self.parent.variable[item.left.id]
			elif isinstance(item.left, ast.Num):
				temp1 = Constant.int(Type.int(), "@temp" + str(count[0]))
				++count[0]
			if isinstance(item.right, ast.BinOp):
				temp2 = self.compile_binop(item.right, count, False, name)
			elif isinstance(item.right, ast.Name):
				temp2 = self.builder.load(self.parent.variable[item.right.id], item.right.id)
				#temp2 = self.parent.variable[item.right.id]
			elif isinstance(item.right, ast.Num):
				temp2 = Constant.int(Type.int(), "@temp" + str(count[0]))
				++count[0]

			if isinstance(item.op, ast.Add):

				temp = self.builder.add(temp1, temp2, name="temp" + str(count[0]))

			elif isinstance(item.op, ast.And):
				temp = self.builder.and_(temp1, temp2, name="@temp" + str(count[0]))
			elif isinstance(item.op, ast.Sub):
				temp = self.builder.sub(temp1, temp2, name="@temp" + str(count[0]))
			elif isinstance(item.op, ast.Mult):
				temp = self.builder.mul(temp1, temp2, name="@temp" + str(count[0]))
			elif isinstance(item.op, ast.Div):
				temp = self.builder.fdiv(temp1, temp2, name="@temp"+ str(count[0]))
			else:
				print "unknown symbol"
			++count[0]
			return temp

	def compile(self):
		target = self.sentence.targets[0]
		if isinstance(target, ast.Name):
			name = target.id
			value = self.sentence.value
			module = self.module

			if name in self.parent.variable:
				vari = self.parent.variable[name]
			else:
				#aloca = None
				if self.isModule:
					#aloca = self.builder.alloca(Type.int(), name=name)
					#self.parent.variable[name] = aloca

					aloca = module.add_global_variable(Type.int(), name)
					self.parent.variable[name] = aloca
				else:
					entry = self.parent.function.get_entry_basic_block()
					bui = Builder.new(entry)
					bui.position_at_beginning(entry)
					aloca = bui.alloca(Type.int(), name)
					self.parent.variable[name] = aloca
			if isinstance(value, ast.Num):
				if self.isModule:
					aloca.initializer = Constant.int(Type.int(), value.n)
				else:
					val = Constant.int(Type.int(), value.n)
					self.builder.store(val, aloca)
				#vari.initializer = Constant.int(Type.int(), value.n)
			elif isinstance(value, ast.BinOp):
				count = [0]
				val = self.compile_binop(value, count, True, name)
				self.builder.store(val, vari)


