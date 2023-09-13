a = int(input())
b = int(input())
c = int(input())

if a > b and a > c:
    if b < c:
        print(f'          Петя          \n'
              f'  Толя  \n'
              f'                  Вася  \n'
              '   II      I      III   ')
    else:
        print(f'          Петя          \n'
              f'  Вася  \n'
              f'                  Толя  \n'
              '   II      I      III   ')
if b > a and b > c:
    if a > c:
        print(f'          Вася          \n'
              f'  Петя  \n'
              f'                  Толя  \n'
              '   II      I      III   ')
    else:
        print(f'          Вася          \n'
              f'  Толя  \n'
              f'                  Петя  \n'
              '   II      I      III   ')
if c > b and c > a:
    if b > a:
        print(f'          Толя          \n'
              f'  Вася  \n'
              f'                  Петя  \n'
              '   II      I      III   ')
    else:
        print(f'          Толя          \n'
              f'  Петя  \n'
              f'                  Вася  \n'
              '   II      I      III   ')
