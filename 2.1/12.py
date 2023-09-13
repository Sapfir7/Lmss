a = str(input())
b = str(input())
a = '00' + a
b = '00' + b
c = []
for i in range(-1, -4, -1):
    c.append((int(a[i]) + int(b[i])) % 10)
numb = int(c[2]) * 100 + int(c[1]) * 10 + int(c[0])
print(numb)