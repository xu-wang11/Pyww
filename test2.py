def qsort(array, head, tail):
	l = head
	r = tail
	m = array[((l + r) >> 1)]
	while l < r:
		while array[r] > m:
			r = r - 1
			print r
		print "\n"
		while array[l] < m:
			l = l + 1
			print l
		print "\n"
		if l <= r:
			t = array[r]
			array[r] = array[l]
			array[l] = t
			r = r - 1
			l = l + 1
			print l, "\n"
	if l < tail:
		qsort(array, l, tail)
	if r > head:
		qsort(array, head, r)



a = [1, 2, 3, 9, 3, 4, 7, 10, 90, 20, 11, 10, 20]
qsort(a, 0, 12)
i = 0
while i < 13:
	print a[i]
	i = i + 1


