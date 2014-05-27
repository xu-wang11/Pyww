all: main.cpp
	clang++ -g main.cpp `llvm-config --cppflags --ldflags --libs core jit native` -O3 -o main