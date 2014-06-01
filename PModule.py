__author__ = 'xu'

import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *
from PVariable import PVariable
#from PAssign import  PAssign
from PFunction import PFunction
from util import *


class PModule:
	function = None
	astModule = None
	llvmModule = None
	modulename = None

	def __init__(self, astmodule, llvmmodule, name):
		self.astModule = astmodule
		self.llvmModule = llvmmodule
		self.modulename = name

		self.function = PFunction(True, astmodule, None, llvmmodule)
		self.function.functionName = name

		if not isinstance(llvmmodule, Module):
			print "not llvm::module"
		else:
			vari = llvmmodule.add_global_variable(Type.array(Type.int(8), 2), name="printd") #"%d"
			value = Constant.string("%d")
			vari.initializer = Constant.string("%d")
			#self.function.builder.store(value, vari)
			type = Type.function(Type.int(), [Type.pointer(Type.int(8))], True)
			llvmmodule.add_function(type, "printf")
	def compile(self):
		self.function.compile()
		module = self.llvmModule

		print self.llvmModule







