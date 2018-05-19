import heapq

a = [(3, 5), (3, 4), (5, 5), (5, 1)]

s_list =heapq.nsmallest(5, a, key=lambda x: x[0] + x[1] / 100)
print(s_list)