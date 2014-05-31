__author__ = 'xu'
import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *

class PAssign:
	sentence = 0
	parent = 0
	module = 0

	def __init__(self, astsent, parent, module):
		self.sentence = astsent
		self.parent = parent
		self.module = module


    def compile(self):
        target = self.sentence.targets[0]
        if isinstance(target, ast.Name):
            name = target.targets[0].id
            value = self.sentence.value
            if isinstance(value, ast.Num):
                print "value"
        print target


