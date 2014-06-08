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
struct_type = Type.struct([Type.int(), Type.int()])

assert struct_type.element_count == len(struct_type.elements)
