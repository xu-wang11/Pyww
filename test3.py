def binary_search(a, n, m):
	low = 0
	high = n
	while low <= high:
		mid = (low + high)/2
		midval = a[mid]

		if midval < m:
			low = mid + 1
		elif midval > m:
			high = mid - 1
		else:
			print mid
			return




array = [1, 2, 3, 4, 7, 10, 20, 20, 90]
num = 10
binary_search(array, 8, num)

