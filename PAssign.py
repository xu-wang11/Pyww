__author__ = 'xu'
import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *

'''
class PAssign:
	node = None
	parent = None
	compiler = None

	def __init__(self, ast_node, parent, compiler):
		self.node = ast_node
		self.parent = parent
		self.compiler = compiler


	def compile(self):
		target = self.node.targets[0]
		if isinstance(target, ast.Name):
			name = target.id
			value = self.node.value
			right = self.compiler.compile_object(value)

			if name in self.parent.variable:
				var = self.parent.variable[name]
				if self.compiler.type_check(var, right):
					self.compiler.store(right, var)
			else:
				if isinstance(right, IntegerType):
					variable = compiler.
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
'''


