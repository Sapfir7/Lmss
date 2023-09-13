n = int(input())
m = int(input())
k_1 = int(input())
k_2 = int(input())
c = n
for i in range(1, n + 1):
    c -= 1
    if k_1 * i + k_2 * c == n * m:
        print(i, c)
        exit()