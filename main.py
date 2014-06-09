__author__ = 'xu'
#import parser

import ast
from llvm import  *
from llvm.core import *
from PModule import PModule
from Compiler import *
import python_yacc
#compile function in python
#a function can be compiled directly means:
#(1)this function has no args
#(2)this function won't use variable out of the function block
modules = []


test_file = open("test2.py")
content = test_file.read()

print content
comp = python_yacc.parse(content, "result.py")
print comp
#table = symtable.symtable(content, "string", "exec")
#compileFunction(compiler)
#pass_manager = FunctionPassManager.new(mymodule)
module = Module.new("main")
executor = ExecutionEngine.new(module)
module._set_data_layout(executor.target_data.__str__())
module._set_target("x86_64-pc-linux-gnu")
compiler = Compiler("main.ll", module)

pmodule = PModule(comp, compiler, "main")
pmodule.compile()
writer = open("result.ll", mode="w")
pmodule.compiler.output(writer)
#compiler.output(writer)

