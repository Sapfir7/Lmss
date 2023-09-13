n = input()
a = [n[0], n[1], n[2]]
a.sort()
if int(a[0]) + int(a[2]) == int(a[1]) * 2:
    print('YES')
else:
    print('NO')