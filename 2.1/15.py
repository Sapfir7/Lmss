n = int(input())
m = int(input())
t = int(input())
ost_n = (m + t) // 60
m = (m + t) % 60
m = str(m)
if len(m) == 1:
    m = '0' + str(m)
if n + ost_n >= 24:
    n = (n + ost_n) % 24
else:
    n += ost_n
n = str(n)
if len(n) == 1:
    n = '0' + n
print(f'{n}:{m}')
