alf = 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'
alf_1 = 'АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
n = input()
m = input()
k = input()


def foo(a, b, c):
    if alf_1.find(a[0]) < alf_1.find(b[0]) and alf_1.find(a[0]) < alf_1.find(c[0]):
        return a
    if alf.find(a[1]) < alf.find(b[1]) and alf_1.find(a[0]) == alf_1.find(b[0]) and alf.find(a[1]) < alf.find(c[1]):
        return a
    if alf.find(a[1]) < alf.find(c[1]) and alf.find(a[1]) < alf.find(b[1]) and alf_1.find(a[0]) == alf_1.find(c[0]):
        return a
    if alf.find(a[2]) < alf.find(b[2]) and alf_1.find(a[0]) == alf_1.find(b[0]) and alf_1.find(a[1]) == alf_1.find(b[1]):
        return a
    if alf.find(a[2]) < alf.find(c[2]) and alf_1.find(a[0]) == alf_1.find(c[0]) and alf_1.find(a[1]) == alf_1.find(c[1]):
        return a
    return 0


if foo(n, m, k):
    print(foo(n, m, k))
if foo(m, k, n):
    print(foo(m, k, n))
if foo(k, m, n):
    print(foo(k, m, n))

