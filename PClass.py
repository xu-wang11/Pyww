__author__ = 'xu'
#compile class
import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from PFunction import PFunction
from compiler import ast as yacc_ast
class PClass:
	functions = None
	variable_types = None

	init_function = None
	variable_names = None
	variable_init = None

	def __init__(self, node, compiler):
		self.functions = []
		self.variable_types = []
		self.variable_names = []
		self.variable_init = []
		self.class_name = node.name
		function_node = []

		for item in node.code.nodes:
			if isinstance(item, yacc_ast.Assign):
				target = item.nodes[0].name
				value = compiler.compile_object(item.expr)
				self.variable_names.append(target)
				self.variable_types.append(value.type)
				self.variable_init.append(value)

				#self.init_value = value
			elif isinstance(item, yacc_ast.Function):
				function = None
				function = PFunction(False, item)
				function.functionName = item.name
				if function.functionName == "__init__":
					self.init_function = function
					function.functionName = self.class_name
				else:
					self.functions.append(function)

		self.classType = Type.struct(self.variable_types, self.class_name)








