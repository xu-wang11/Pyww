__author__ = 'xu'
#import parser
import symtable
import ast
from llvm import *
from llvm.core import *
from llvm.ee import *
from llvm.passes import *
from llvm.passes import *

import sys
from PModule import PModule

#compile function in python
#a function can be compiled directly means:
#(1)this function has no args
#(2)this function won't use variable out of the function block
modules = []

#modules.append(PywwModule())
file = open("test1.py")
lines = file.readlines()
content = ""
for item in lines:
    content = content + item
print content
compiler = ast.parse(content, "result.py", mode='exec')
table = symtable.symtable(content, "string", "exec")
#compileFunction(compiler)

mymodule = Module.new("main.ll")
#pass_manager = FunctionPassManager.new(mymodule)
executor = ExecutionEngine.new(mymodule)
mymodule._set_data_layout(executor.target_data.__str__())
mymodule._set_target("x86_64-pc-linux-gnu")

moduleitem = PModule(compiler, mymodule, "main")

modules.append(moduleitem)
moduleitem.compile()
writer = open("result.ll", mode="w")
module = moduleitem.llvmModule
if isinstance(module, Module):
	writer.write(module.__str__())
writer.close()
print "end"

