__author__ = 'xu'

a = [1]

class f:
	a = None

def func():
	a[0] = 2
	print a[0]
func()
print a[0]