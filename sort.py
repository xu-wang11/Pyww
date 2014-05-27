def qsort(array, head, tail):
	l = head
	r = tail
	m = array[((l + r)>>1)]
	while(l < r):
		while(array[r] > m):
			r = r - 1
		while(array[l] < m):
			l = l + 1
		if(l <= r):
			t = array[r]
			array[r] = array[l]
			array[l] = t
			r = r - 1
			l = l + 1
	if(l < tail):
		qsort(array, l, tail)
	if(r > head):
		qsort(array, head, r)
def main():
	A  = [1, 2, 3, 9, 3, 4, 7, 10, 90, 20, 11, 10, 20]
	qsort(A, 0, 12)
	for item in A:
		print item
main()

