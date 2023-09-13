a = input()
maxx = [a[0], a[1], a[2]]
maxx.sort()
if maxx[0] == '0':
    print(f'{maxx[1]}{maxx[0]}', f'{maxx[2]}{maxx[1]}')
else:
    print(f'{maxx[0]}{maxx[1]}', f'{maxx[2]}{maxx[1]}')
