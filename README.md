#Pyww#
version:0.0

##Developer:##
- Xu Wang  xu-wang11@mails.thu.edu.cn
- <a href="http://wenqingfu.me" target="_blank">Qingfu Wen</a> wenqf11@mails.thu.edu.cn
- <a href="http://yanglei.me" target="_blank">Lei Yang</a> yanglei11@mails.thu.edu.cn

##Environment##
-Compiler the project:
clang++ -g main.cpp \`llvm-config --cppflags --ldflags --libs core jit native\` -O3 -o main

##Reference##
- <a href="http://llvm.org/docs/tutorial/LangImpl4.html">LLVM-LangImpl</a>
- <a href= "http://root.cern.ch/svn/root/vendors/llvm/examples/Kaleidoscope/Chapter4/toy.cpp">Kaleidoscope</a>
