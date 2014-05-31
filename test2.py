__author__ = 'xu'


def qsort(array, head, tail):
	l = head
	r = tail
	m = array[((l + r) >> 1)]
	while l < r:
		while array[r] > m:
			--r
		while array[l] < m:
			++l
		if l <= r:
			t = array[r]
			array[r] = array[l]
			array[l] = t
			--r
			++l
	if l < tail:
		qsort(array, l, tail)
	if r > head:
		qsort(array, head, r)


def main():
	a = [1, 2, 3, 9, 3, 4, 7, 10, 90, 20, 11, 10, 20]
	qsort(a, 0, 12)
	for item in a:
		print item
main()

