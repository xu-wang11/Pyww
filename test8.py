class h:
    a = 0
    b = 1
    def __init__(self):
        print "hello world"
    def sum(self):
        return self.a + self.b
    def setA(self, a):
        self.a = a
    def setB(self, b):
        self.b = b
v = h()
v.setA(2)
c = v.sum()
print c

