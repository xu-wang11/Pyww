#import parser
import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *

import sys
#compile function in python
#a function can be compiled directly means:
#(1)this function has no args
#(2)this function won't use variable out of the function block

def canFunctionBeCompiler(functionnode):
    
    return false
def compileFunction(astnode):
    for item in ast.iter_child_nodes(astnode):
    
        if isinstance(item, ast.FunctionDef):
            print "function"
        elif isinstance(item, ast.Expr):
            print "expression"
        elif isinstance(item, ast.Assign):
            print "assign"
        elif isinstance(item, ast.While):
            print "while"
        elif isinstance(item, ast.If):
            print "If"
        else:
            print "no idea"
        
    
                
        
    
file = open("sort.py")
lines = file.readlines()
content = ""
for item in lines:
    content = content + item
print content
compiler = ast.parse(content, "result.py", mode='exec')
compileFunction(compiler)
    
print "end"
