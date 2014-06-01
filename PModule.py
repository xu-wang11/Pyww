__author__ = 'xu'

from PFunction import PFunction
from util import *
from Compiler import Compiler


class PModule:
	function = None
	astModule = None
	compiler = None
	#modulename = None

	def __init__(self, ast_module,  compiler,  name="main"):
		self.astModule = ast_module
		self.compiler = compiler
		self.function = PFunction(True, ast_module)

	def compile(self):
		self.function.bind_compiler(self.compiler, True)

		self.compiler.print_module()







