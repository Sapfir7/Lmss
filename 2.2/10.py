a = input()
sum_1 = int(a[2]) + int(a[1])
sum_2 = int(a[0]) + int(a[1])

if sum_1 > sum_2:
    print(f'{sum_1}{sum_2}')
if sum_1 <= sum_2:
    print(f'{sum_2}{sum_1}')