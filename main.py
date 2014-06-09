__author__ = 'xu'
from PModule import PModule
from Compiler import *
import python_yacc
import sys
#compile function in python
#a function can be compiled directly means:
#(1)this function has no args
#(2)this function won't use variable out of the function block
if len(sys.argv) > 1:
	filename = sys.argv[1]
else:
	filename = "test9.py"
test_file = open(filename)
content = test_file.read()
print content
comp = python_yacc.parse(content, "result.py")
print comp
module = Module.new("main")
executor = ExecutionEngine.new(module)
module._set_data_layout(executor.target_data.__str__())
module._set_target("x86_64-pc-linux-gnu")
compiler = Compiler("main.ll", module)
pmodule = PModule(comp, compiler, "main")
pmodule.compile()

writer = open(filename[0:-2] + "ll", mode="w")
pmodule.compiler.output(writer)
#compiler.output(writer)

