PY = python
CC = clang
all: t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11
clean:
	rm *.ll
	rm t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11
t1: test1.ll
	$(CC) test1.ll -o t1
test1.ll: test1.py
	$(PY) main.py test1.py
t2: test2.ll
	$(CC) test2.ll -o t2
test2.ll: test2.py
	$(PY) main.py test2.py
t3: test3.ll
	$(CC) test3.ll -o t3
test3.ll:test3.py
	$(PY) main.py test3.py
t4:test4.ll
	$(CC) test4.ll -o t4
test4.ll:test4.py
	$(PY) main.py test4.py
t5: test5.ll
	$(CC) test5.ll -o t5
test5.ll:test5.py
	$(PY) main.py test5.py
t6: test6.ll
	$(CC) test6.ll -o t6
test6.ll: test6.py
	$(PY) main.py test6.py
t7: test7.ll
	$(CC) test7.ll -o t7
test7.ll:test7.py
	$(PY) main.py test7.py
t8: test8.ll
	$(CC) test8.ll -o t8
test8.ll:test8.py
	$(PY) main.py test8.py
t9: test9.ll
	$(CC) test9.ll -o t9
test9.ll:test9.py
	$(PY) main.py test9.py
t10: test10.ll
	$(CC) test10.ll -o t10
test10.ll:test10.py
	$(PY) main.py test10.py
t11: test11.ll
	$(CC) test11.ll -o t11
test11.ll:test11.py
	$(PY) main.py test11.py
