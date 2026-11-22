matrix = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12]]

haha = matrix[1]
haha[2] = -10
print(matrix) # есть -10

# с copy
matrix = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12]]

haha = matrix[1].copy()
haha[2] = -10
print(matrix) # нет -10

# iter(next(set()) - способ получить элемент
st = {1, 2, 3, 7, 6}
# print(st[0]) -> TypeError

print(next(iter(st))) # -> 1
b = iter(st)
print(next(b)) # 1
print(next(b)) # 2
print(next(b)) # 3

#крутость в том, что работает мгновенно и не выделяет список в отличии от list(st)[0]

st = {1, 3}
print(bool(st - {3, 1}))

lst = [1, 2, 3]
a = lst[1:2]
print(a)
a[0] = 53

print(lst)

lst1 = [1, 2, 3, 4]
lst2 = lst1
lst2[1] = 32
print(lst1)

print(str(True))