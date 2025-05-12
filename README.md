# Отчёт по языку Kron

## Сборка проекта

**Сборка**:
```bash
dotnet build
```

Компилирует проект (.NET SDK 6.0+).

**Запуск**:
```bash
dotnet run -- <путь_к_файлу>
```

Пример:
```bash
dotnet run -- samples/factorial.kron
```

**Структура**:
- `src/`:
  - `Ast.fs` — структура программы.
  - `Parser.fs` — разбор кода.
  - `Interpreter.fs` — выполнение.
  - `Topology.fs` — топология.
  - `Std.fs` — функции (`println`).
  - `Runtime.fs` — значения, окружение.
  - `Program.fs` — вход.
- `samples/` — примеры: `factorial.kron`, `fibonacci.kron`, `torus.kron`, `triangle.kron`, `namespace_examples.kron`, `mod_and_match.kron`.
- `Kron.fsproj` — проект F#.
- `run_tests.fsx` — тесты.

## AST

AST (абстрактное синтаксическое дерево) представляет программу как структуру: переменные, функции, списки, топология. Определено в `Ast.fs`:
- Литералы: числа (`42`, `3.14`), строки (`"hello"`), `true`/`false`.
- Выражения: переменные, лямбда-функции, списки, `if`, `match`, топология (`simplex`, `boundary`).
- Объявления: `let`, импорты, модули.
- Образцы: для `match` (`0 -> 0`).

Основа для парсинга и выполнения.

## Построение AST

### Токенизация

Код разбивается на токены. Пример:
```kron
let x = 42
```
Токены: `["let"; "x"; "="; "42"]`.

Функция `tokenize` в `Parser.fs` убирает пробелы, комментарии (`#`, `//`), выделяет ключевые слова, числа, операторы.

### Парсинг

Токены преобразуются в AST. Определяется роль: `let` — привязка, `lambda` — функция, `[0 1 2]` — симплекс. Реализовано в `Parser.fs`. Пример (`let x = 42`): узел `DLet("x", Lit(LInt 42))`.

## Парсер

Парсер (`Parser.fs`) преобразует код в AST. Анализирует токены:
- `let`, `let rec` — привязки.
- `lambda` — функции.
- `match` — сопоставление.
- `simplex`, `glue` — топология.
- Числа, строки — значения.

Пример (`factorial.kron`):
```kron
let factorial = lambda n ->
    if n == 0 then 1 else n * factorial (n - 1)
let main = factorial 5
let _ = println main
```

Создаётся AST с узлами `DLet`, `Lambda`, `If`. Обрабатывает все конструкции, выдаёт ошибки при неверном синтаксисе.

## Интерпретатор

Интерпретатор (`Interpreter.fs`) выполняет AST. Использует окружение (словарь переменных). 
Действия:
- Числа, строки — возвращает значения.
- Переменные — поиск в окружении.
- Функции — создаёт замыкания.
- Топология (`boundary`, `glue`) — использует `Topology.fs`.
- `println` — выводит результат.

Пример (`triangle.kron`):
```kron
import std
let tri = simplex [0 1 2]
let bd = boundary tri
let _ = println bd
```

Вывод: `[[1; 2]; [0; 2]; [0; 1]]`. Вычисляет границы треугольника.

## Реализованные функции

Добавлены функции, обеспечивающие мощность и универсальность Kron.

### Привязки (`let`)

Добавлена привязка значений к именам (`let`, `let rec`).

Пример (`factorial.kron`):
```kron
let factorial = lambda n ->
    if n == 0 then 1 else n * factorial (n - 1)
let main = factorial 5
let _ = println main
```

Вывод: `120`.

### Рекурсия

Добавлена рекурсия через `let rec`.

Пример (`fibonacci.kron`):
```kron
let rec fib = lambda n ->
    match n with
    | 0    -> 0
    | 1    -> 1
    | n    -> fib (n - 1) + fib (n - 2)
let main = fib 10
let _ = println main
```

Вывод: `55`.

### Функции

Добавлены лямбда-выражения.

Пример:
```kron
let add = lambda x y -> x + y
let main = add 3 5
let _ = println main
```

Вывод: `8`.

### Замыкания

Добавлены замыкания для сохранения окружения.

Пример (`namespace_examples.kron`):
```kron
module Math
  let pi = 3.14159
end
module Main
  import std
  let _ = println (Math.pi)
end
```

Вывод: `3.14159`.

### Списки

Добавлены списки для коллекций.

Пример:
```kron
let myList = [1, 2, 3]
let _ = println myList
```

Вывод: `[1, 2, 3]`.

### Топологические операции

Добавлены симплексы, комплексы, операции `simplex`, `glue`, `boundary`, `dimension`.

Пример (`torus.kron`):
```kron
let square = simplex [0 1 2 3]
let torus = glue square square
let result = println (dimension torus)
```

Вывод: `2`.

Пример (`triangle.kron`):
```kron
import std
let tri = simplex [0 1 2]
let bd = boundary tri
let _ = println bd
```

Вывод: `[[1; 2]; [0; 2]; [0; 1]]`.

### Сопоставление с образцом

Добавлено `match` для управления потоком.

Пример (`mod_and_match.kron`):
```kron
let rec even = lambda n ->
    match n with
    | 0    -> true
    | n    -> odd (n - 1)
let rec odd = lambda n ->
    match n with
    | 0    -> false
    | n    -> even (n - 1)
let main = even 4
let _ = println main
```

Вывод: `true`.

### Модули

Добавлены модули для организации кода.

Пример (`namespace_examples.kron`):
```kron
module Math
  let pi = 3.14159
  let sin = lambda x -> builtin_sin x
end
module Main
  import std
  let _ = println (Math.pi)
end
```

Вывод: `3.14159`.

### Условные выражения

Добавлены `if` для ветвления.

Пример:
```kron
let max = lambda x y ->
    if x > y then x else y
let main = max 10 5
let _ = println main
```

Вывод: `10`.

### Встроенные функции

Добавлены операции:
- Арифметика: `+`, `-`, `*`, `/`.
- Сравнение: `==`, `>`.
- Вывод: `println`.
- Математика: `builtin_sin`.

Пример:
```kron
let x = 3 + 5
let _ = println x
```

Вывод: `8`.


## Выполнение задач и критериев

Выполнены все задачи и критерии:
- Реализован язык: функциональный, с привязками, рекурсией, функциями, замыканиями, списками, топологией, модулями, сопоставлением, условиями, встроенными функциями.
- Полнота по Тьюрингу: обеспечена рекурсией (`fibonacci.kron`), условными выражениями (`if`, `match`), функциями высшего порядка. Моделирует любые вычисления.
- Топология: добавлены операции (`simplex`, `glue`, `boundary`, `dimension`) для геометрии (`torus.kron`, `triangle.kron`).
- Примеры: `samples/` демонстрируют функции:
  - `factorial.kron` — привязки, рекурсия.
  - `fibonacci.kron` — сопоставление, рекурсия.
  - `torus.kron`, `triangle.kron` — топология.
  - `namespace_examples.kron` — модули, замыкания.
  - `mod_and_match.kron` — сопоставление.
- Документация: описывает язык, сборку, функции, реализацию.

## Вклад команды

| Имя | Роль |
|-----|------|
| я | очень  |
| сильно | люблю  |
| пузо | Сошникова  |


## Использование ИИ

ИИ (ChatGPT, GitHub Copilot) применялся для:
- Шаблоны кода для парсера, интерпретатора.
- Структура документации, примеры.
- Поиск ошибок в F#.
