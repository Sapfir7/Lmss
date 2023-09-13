import math

a = float(input())
b = float(input())
c = float(input())
discr = b ** 2 - 4 * a * c
if discr > 0:
    print((-b - math.sqrt(discr)) / (2 * a), (-b + math.sqrt(discr)) / (2 * a))
if discr == 0:
    print(-b / (2*a))
if discr < 0:
    print('No solution')