a = int(input())
b = int(input())
c = int(input())


def f(x, y, z):
    if x + y > z:
        return 1


if f(a, b, c) and f(a, c, b) and f(b, c, a):
    print('YES')
else:
    print('NO')