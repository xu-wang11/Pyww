__author__ = 'xu'
#import parser
import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *

import sys
import PywwFunction
from PywwModule import PywwModule
#compile function in python
#a function can be compiled directly means:
#(1)this function has no args
#(2)this function won't use variable out of the function block
modules = []

#modules.append(PywwModule())
file = open("main.py")
lines = file.readlines()
content = ""
for item in lines:
    content = content + item
print content
compiler = ast.parse(content, "result.py", mode='exec')
#compileFunction(compiler)
mymodule = Module.new("main")
moduleitem = PywwModule(compiler, mymodule)
modules.append(moduleitem)
moduleitem.compile()
print "end"

