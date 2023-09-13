a = input()
b = input()
arr = [a[0], a[1], b[0], b[1]]
arr.sort()
print(f'{arr[3]}{(int(arr[2]) + int(arr[1])) % 10}{arr[0]}')
