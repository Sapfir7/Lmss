name = str(input())
price = int(input())
weight = int(input())
money = int(input())
print('================Чек================\n'
      'Товар:', '{0: >28}'.format(f'{name}'), '\n'
                                              'Цена:', '{0: >29}'.format(f'{weight}кг * {price}руб/кг'), '\n'
                                                                                                         'Итого:',
      '{0: >28}'.format(f'{weight * price}руб'), '\n'
                                                 'Внесено:', '{0: >26}'.format(f'{money}руб'), '\n'
                                                                                               'Сдача:',
      '{0: >28}'.format(f'{abs(weight * price - money)}руб'), '\n'
                                                              '===================================')
