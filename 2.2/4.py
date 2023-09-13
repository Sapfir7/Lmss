n = int(input())
m = int(input())
k = int(input())


def foo(a):
    if a == n:
        return ('Петя')
    if a == m:
        return ('Вася')
    if a == k:
        return ('Толя')


a = [n, m, k]
a.sort()
print(f'1. {foo(a[2])}\n'
      f'2. {foo(a[1])}\n'
      f'3. {foo(a[0])}\n')
