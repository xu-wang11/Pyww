__author__ = 'xu'
#compile class
import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from PFunction import PFunction
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

		for item in node.body:
			if isinstance(item, ast.Assign):
				target = item.targets[0].id
				value = compiler.compile_object(item.value)
				self.variable_names.append(target)
				self.variable_types.append(value.type)
				self.variable_init.append(value)

				#self.init_value = value
			elif isinstance(item, ast.FunctionDef):
				function = None
				function = PFunction(False, item)
				function.functionName = item.name
				if function.functionName == "__init__":
					self.init_function = function
					function.functionName = self.class_name
				else:
					self.functions.append(function)

		self.classType = Type.struct(self.variable_types, self.class_name)








