__author__ = 'xu'
'''
in this file define some common function
'''
import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *


def getTypeFromAST(node):
	if isinstance(node, ast.Num):
		return Type.int()
	elif isinstance(node, ast.Str):
		return Type.int(bits=8)
