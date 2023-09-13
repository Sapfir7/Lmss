n = int(input())
m = int(input())
k = int(input())
if n > m and n > k:
    print('Петя')
if n < m and m > k:
    print('Вася')
if n < k and m < k:
    print('Толя')
