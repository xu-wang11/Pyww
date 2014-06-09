#Pyww#
version:0.0
###Description#
Pyww is a python compiler  using LLVM

##Developer:##
- Xu Wang  xu-wang11@mails.thu.edu.cn
- <a href="http://wenqingfu.me" target="_blank">Qingfu Wen</a> wenqf11@mails.thu.edu.cn
- <a href="http://yanglei.me" target="_blank">Lei Yang</a> yanglei11@mails.thu.edu.cn

##Environment##

###Support Grammar#

- compile class but don't support extends
- support +/-/*//>>/<< and not or 
- support if, while, for sentence
- a list's elment must be the only type
- variable cannot change its' type
- a lots of thing to do for the compiler for python

###packages#
<table>
<tr>
<th>name</th><th>version</th>
</tr>
<tr>
<td>LLVM</td><td>3.2</td>
</tr>
<tr>
<td>Clang</td><td>3.2</td>
</tr>
<tr>
<td>llvmpy</td><td>0.12.0</td>
</tr>
<tr><td>ply</td><td>3.4</td>
</table>

###Compiler the project:#
make
###Solution#
Solve Return Type: guess then compile, then compile twice<br>
compile *.c to *.ll<br>
clang -emit-llvm main.c -S -o main.ll<br>


##Reference##
- <a href="http://llvm.org/docs/tutorial/LangImpl4.html">LLVM-LangImpl</a>
- <a href= "http://root.cern.ch/svn/root/vendors/llvm/examples/Kaleidoscope/Chapter4/toy.cpp">Kaleidoscope</a>
