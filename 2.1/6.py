name = input()
a = int(input())
b = int(input())
c = int(input())
print('Чек\n'
      f'{name} - {b}кг - {a}руб/кг\n'
      f'Итого: {a*b}руб\n'
      f'Внесено: {c}руб\n'
      f'Сдача: {c - a * b}руб')