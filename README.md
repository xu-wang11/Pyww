#Pyww#
version:0.0
###Description#
Pyww is a python compiler  using LLVM

##Developer:##
- Xu Wang  xu-wang11@mails.thu.edu.cn
- <a href="http://wenqingfu.me" target="_blank">Qingfu Wen</a> wenqf11@mails.thu.edu.cn
- <a href="http://yanglei.me" target="_blank">Lei Yang</a> yanglei11@mails.thu.edu.cn

##Environment##
###packages#
<table>
<tr>
<th>name</th><th>version</th>
</tr>
<tr>
<td>LLVM</td><td>3.4</td>
</tr>
<td>Clang</td><td>3.4</td>
</table>

###Compiler the project:#
clang++ -g main.cpp \`llvm-config --cppflags --ldflags --libs core jit native\` -O3 -o main
###Solution#
Solve Return Type: guess then compile, then compile twice
compile .c to .ll
clang -emit-llvm main.c -S -o main.ll


##Reference##
- <a href="http://llvm.org/docs/tutorial/LangImpl4.html">LLVM-LangImpl</a>
- <a href= "http://root.cern.ch/svn/root/vendors/llvm/examples/Kaleidoscope/Chapter4/toy.cpp">Kaleidoscope</a>
