# Отчёт
## Сборка проекта

Сборка проекта:
```
dotnet build
```
Запуск проекта:
```
dotnet run <путь к файлу>
```
## Структура проекта
- ```src/``` — исходные файлы реализации:
- - ```Ast.fs``` — определение абстрактного синтаксического дерева.
- - ```Parser.fs``` — токенизация и парсинг кода.
- - ```Interpreter.fs``` — интерпретация AST.
- - ```Runtime.fs``` — типы значений и окружение.
- - ```Topology.fs``` — топологические операции.
- - ```Std.fs``` — стандартная библиотека (println).
- - ```Program.fs``` — точка входа.
- ```samples/``` — примеры программ: ```factorial.kron```, ```fibonacci.kron```, ```torus.kron```, ```triangle.kron```, ```mod_and_match.kron```, ```namespace_examples.kron```.
- ```Kron.fsproj``` — файл проекта F#.
- ```run_tests.fsx``` — скрипт для запуска тестов.

## AST

Абстрактное синтаксическое дерево (`AST`), определённое в `Ast.fs`, представляет структуру программы на языке Kron. Оно строится из узлов, соответствующих синтаксису языка, и используется для парсинга и интерпретации. Основные компоненты:

- **Литералы** (`Literal`): 
  - `LInt` (целые числа, например, `42`).
  - `LFloat` (числа с плавающей точкой, например, `3.14`).
  - `LBool` (булевы значения, `true`, `false`).
  - `LString` (строки, например, `"hello"`).
- **Образцы** (`Pattern`): 
  - `PVar` (переменные, например, `n`).
  - `PWildcard` (подстановочный знак `_`).
  - `PCons` (конструкторы для симплексов).
  - `PLit` (литералы в образцах).
- **Выражения** (`Expr`): 
  - `Lit` (литералы).
  - `Var` (переменные).
  - `Match` (сопоставление с образцом).
  - `Lambda` (лямбда-выражения).
  - `Apply` (применение функций).
  - `Let` (привязки).
  - `If` (условные выражения).
  - `List` (списки).
  - `Shell` (команды оболочки).
  - `TopOp` (топологические операции: `boundary`, `faces`, `dimension`).
  - `TopSimplex` (симплексы).
  - `TopGlue` (склейка комплексов).
- **Объявления** (`Decl`): 
  - `DLet` (привязки `let`).
  - `DImport` (импорты модулей).
  - `DModule` (модули).

Каждый узел `Expr` может содержать другие узлы `Expr`, что позволяет представлять сложные конструкции, такие как рекурсивные функции или топологические вычисления.

## Процесс построения синтаксического дерева

### Токенизация

Токенизация, реализованная в функции `tokenize` модуля `Parser.fs`, принимает исходный код в виде строки и разбивает его на токены — минимальные синтаксические единицы. Токены включают ключевые слова (`let`, `lambda`, `match`), идентификаторы, операторы (`+`, `-`, `*`, `/`, `==`), литералы и символы (`(`, `)`, `[`, `]`). Комментарии (`#`, `//`) удаляются, пробелы и табуляции игнорируются.

**Пример**:
```kron
let x = 42
```
**Токены**:
```
["let"; "x"; "="; "42"]
```

### Парсинг

Парсинг, реализованный в `Parser.fs`, преобразует последовательность токенов в AST. Функция `parseModuleFromString` инициирует процесс, вызывая `parseModule`, который рекурсивно анализирует токены. Парсер обрабатывает:
- **Объявления**: `let`, `let rec`, `import`, `module`.
- **Выражения**: литералы, переменные, лямбда-выражения, списки, топологические операции.
- **Образцы**: переменные, подстановочные знаки, литералы для `match`.

Парсинг начинается с первичных выражений (`parsePrimary`), затем обрабатываются применения функций и операторы (`parseApp`), и завершается построением модуля (`parseModule`).

### Создание узлов синтаксического дерева

Узлы AST создаются в соответствии с синтаксисом:
- **Литералы**: `Lit(LInt 42)` для `42`.
- **Переменные**: `Var "x"` для `x`.
- **Лямбда-выражения**: `Lambda(["n"], ...)` для `lambda n -> ...`.
- **Топологические операции**: `TopSimplex([0; 1; 2])` для `simplex [0 1 2]`.

На выходе получается дерево, представляющее структуру программы.

## Парсер

Парсер (`Parser.fs`) работает следующим образом:

1. **Парсинг ключевых слов**:
   Ключевые слова, такие как `let`, `lambda`, `match`, `module`, преобразуются в соответствующие узлы AST.
   ```kron
   let x = 42
   ```
   **Узел**: `DLet("x", Lit(LInt 42))`.

   **Код**:
   ```fsharp
   | "let" :: name :: "=" :: rest ->
       let expr, after = parseExpr rest
       DLet(name, expr), after
   ```

2. **Парсинг литералов**:
   Числа, строки и булевы значения становятся узлами `Lit`.
   ```kron
   42
   ```
   **Узел**: `Lit(LInt 42)`.

   **Код**:
   ```fsharp
   | tok :: rest when Int64.TryParse(tok) |> fst -> Lit(LInt (Int64.Parse tok)), rest
   ```

3. **Парсинг идентификаторов**:
   Идентификаторы преобразуются в `Var`.
   ```kron
   x
   ```
   **Узел**: `Var "x"`.

   **Код**:
   ```fsharp
   | name :: rest when isIdentStart name.[0] -> Var name, rest
   ```

4. **Парсинг лямбда-выражений**:
   Лямбда-выражения парсятся с аргументами и телом.
   ```kron
   lambda n -> n + 1
   ```
   **Узел**: `Lambda(["n"], Apply(Var("+"), [Var("n"); Lit(LInt 1)]))`.

   **Код**:
   ```fsharp
   | "lambda" :: rest ->
       let args, afterArgs = argsAcc [] rest
       let body, afterBody = parseExpr afterArgs
       Lambda(args, body), afterBody
   ```

5. **Парсинг топологических конструкций**:
   Операции, такие как `simplex`, парсятся как специальные узлы.
   ```kron
   simplex [0 1 2]
   ```
   **Узел**: `TopSimplex([0; 1; 2])`.

   **Код**:
   ```fsharp
   | "simplex" :: "[" :: rest ->
       let vs, after = collectInts [] rest
       TopSimplex vs, after
   ```

### Пример использования парсера

**Код** (из `torus.kron`):
```kron
import std
let square = simplex [0 1 2 3]
let torus = glue square square
let result = println (dimension torus)
```

**Токены**:
```
["import"; "std"; "let"; "square"; "="; "simplex"; "["; "0"; "1"; "2"; "3"; "]"; "let"; "torus"; "="; "glue"; "square"; "square"; "let"; "result"; "="; "println"; "("; "dimension"; "torus"; ")"]
```

**AST**:
```fsharp
[
    DImport("std");
    DLet("square", TopSimplex([0; 1; 2; 3]));
    DLet("torus", TopGlue(Var("square"), Var("square")));
    DLet("result", Apply(Var("println"), [TopOp("dimension", [Var("torus")])]))
]
```

**Пояснение**: Парсер преобразует код в AST, представляющее импорт, определение симплекса, склейку и вывод размерности.

## Интерпретатор

Интерпретатор (`Interpreter.fs`) вычисляет AST в окружении `Env` (`Map<string, Value>`), возвращая значения типа `Value` (`VInt`, `VFloat`, `VBool`, `VString`, `VList`, `VClosure`, `VBuiltin`, `VComplex`, `VModule`, `VUnit`).

**Работа интерпретатора**:

1. **Литералы**:
   Литералы преобразуются в значения.
   ```kron
   42
   ```
   **Результат**: `VInt 42`.

   **Код**:
   ```fsharp
   | Lit lit ->
       match lit with
       | LInt i -> VInt i
       | LFloat f -> VFloat f
       | LBool b -> VBool b
       | LString s -> VString s
   ```

2. **Переменные**:
   Поиск переменных в окружении.
   ```kron
   x
   ```
   **Результат**: Значение `x` или ошибка, если не определено.

   **Код**:
   ```fsharp
   | Var name ->
       match Map.tryFind name env with
       | Some v -> v
       | None -> runtimeError $"Undefined variable {name}"
   ```

3. **Лямбда-выражения**:
   Создание замыканий.
   ```kron
   lambda x -> x + 1
   ```
   **Результат**: `VClosure(["x"], Apply(Var("+"), [Var("x"); Lit(LInt 1)]), ref env)`.

   **Код**:
   ```fsharp
   | Lambda (args, body) -> VClosure(args, body, ref env)
   ```

4. **Применение функций**:
   Применение функций к аргументам.
   ```kron
   f x
   ```
   **Результат**: Вычисленное значение `f(x)`.

   **Код**:
   ```fsharp
   | Apply (func, args) ->
       let f = eval env func
       let evaluatedArgs = List.map (eval env) args
       apply f evaluatedArgs
   ```

5. **Топологические операции**:
   Вычисление операций, таких как `boundary`.
   ```kron
   boundary tri
   ```
   **Результат**: `VComplex` с границами.

   **Код**:
   ```fsharp
   | TopOp (op, args) ->
       let evaluated = List.map (eval env) args
       match op, evaluated with
       | "boundary", [VComplex c] ->
           let boundarySimplices = c |> Set.map Topology.boundary |> Set.unionMany
           VComplex boundarySimplices
   ```

6. **Сопоставление с образцом**:
   Сравнение значений с образцами.
   ```kron
   match n with | 0 -> 0 | _ -> 1
   ```
   **Результат**: Значение соответствующей ветви.

   **Код**:
   ```fsharp
   | Match (expr, cases) ->
       let value = eval env expr
       matchPattern env value cases
   ```

7. **Вывод результатов**:
   Вывод значений в консоль.
   ```kron
   println x
   ```
   **Результат**: Выводит `x`.

   **Код**:
   ```fsharp
   prim "println" (function
       | [v] -> printfn "%s" (valueToString v); VUnit
       | _ -> runtimeError "println expects 1 argument")
   ```

### Пример использования интерпретатора

**Код** (из `fibonacci.kron`):
```kron
import std
let rec fib = lambda n ->
    match n with
    | 0    -> 0
    | 1    -> 1
    | n    -> fib (n - 1) + fib (n - 2)
let main = fib 10
let _ = println main
```

**Вывод**:
```
55
```

**Пояснение**: Интерпретатор рекурсивно вычисляет 10-е число Фибоначчи (55) и выводит его.

## Описание функций

### Именованные переменные (`let`)

**Описание**: `let` привязывает значение к имени для последующего использования. Поддерживаются рекурсивные привязки (`let rec`).

**Синтаксис**:
```kron
let <имя> = <выражение>
```

**Пример** (из `factorial.kron`):
```kron
let factorial = lambda n ->
    if n == 0 then 1 else n * factorial (n - 1)
let main = factorial 5
let _ = println main
```

**Пояснение**: Определяет функцию `factorial`, вычисляет `factorial 5` (120) и выводит результат.

**AST**:
```fsharp
[
    DLet("factorial", Lambda(["n"], If(Apply(Var("=="), [Var("n"); Lit(LInt 0)]),
                                      Lit(LInt 1),
                                      Apply(Var("*"), [Var("n"); Apply(Var("factorial"), [Apply(Var("-"), [Var("n"); Lit(LInt 1)])])]))));
    DLet("main", Apply(Var("factorial"), [Lit(LInt 5)]));
    DLet("_", Apply(Var("println"), [Var("main")]))
]
```

### Рекурсия

**Описание**: Рекурсия позволяет функциям вызывать себя для решения задач, разбиваемых на подзадачи.

**Синтаксис**:
```kron
let rec <имя> = lambda <аргументы> -> <тело>
```

**Пример** (из `fibonacci.kron`):
```kron
let rec fib = lambda n ->
    match n with
    | 0    -> 0
    | 1    -> 1
    | n    -> fib (n - 1) + fib (n - 2)
let main = fib 10
let _ = println main
```

**Пояснение**: Вычисляет 10-е число Фибоначчи (55) с помощью рекурсии и выводит результат.

**AST**:
```fsharp
[
    DLet("fib", Lambda(["n"], Match(Var("n"), [
        (PLit(LInt 0), Lit(LInt 0));
        (PLit(LInt 1), Lit(LInt 1));
        (PVar "n", Apply(Var("+"), [Apply(Var("fib"), [Apply(Var("-"), [Var("n"); Lit(LInt 1)])]);
                                    Apply(Var("fib"), [Apply(Var("-"), [Var("n"); Lit(LInt 2)])])]))
    ])));
    DLet("main", Apply(Var("fib"), [Lit(LInt 10)]));
    DLet("_", Apply(Var("println"), [Var("main")]))
]
```

### Функции

**Описание**: Функции позволяют группировать код для повторного использования.

**Синтаксис**:
```kron
lambda <аргументы> -> <тело>
```

**Пример**:
```kron
let add = lambda x y -> x + y
let main = add 3 5
let _ = println main
```

**Пояснение**: Определяет функцию `add`, вычисляет `add 3 5` (8) и выводит результат.

**AST**:
```fsharp
[
    DLet("add", Lambda(["x"; "y"], Apply(Var("+"), [Var("x"); Var("y")])));
    DLet("main", Apply(Var("add"), [Lit(LInt 3); Lit(LInt 5)]));
    DLet("_", Apply(Var("println"), [Var("main")]))
]
```

### Замыкания

**Описание**: Замыкания сохраняют окружение, в котором создана функция.

**Пример** (из `namespace_examples.kron`):
```kron
module Math
  let pi = 3.14159
end
module Main
  import std
  let _ = println (Math.pi)
end
```

**Пояснение**: Переменная `pi` из модуля `Math` доступна в `Main` через окружение.

**AST**:
```fsharp
[
    DModule("Math", [DLet("pi", Lit(LFloat 3.14159))]);
    DModule("Main", [
        DImport("std");
        DLet("_", Apply(Var("println"), [Var("Math.pi")]))
    ])
]
```

### Списки / Последовательности

**Описание**: Списки хранят коллекции элементов.

**Пример**:
```kron
let myList = [1, 2, 3]
let _ = println myList
```

**Пояснение**: Создаёт список `[1, 2, 3]` и выводит его.

**AST**:
```fsharp
[
    DLet("myList", List([Lit(LInt 1); Lit(LInt 2); Lit(LInt 3)]));
    DLet("_", Apply(Var("println"), [Var("myList")]))
]
```

### Топологические операции

**Описание**: Поддержка симплексов и комплексов для геометрических вычислений.

**Пример** (из `triangle.kron`):
```kron
import std
let tri = simplex [0 1 2]
let bd = boundary tri
let _ = println bd
```

**Пояснение**: Определяет треугольник, вычисляет его границу и выводит её (`[[1; 2]; [0; 2]; [0; 1]]`).

**AST**:
```fsharp
[
    DImport("std");
    DLet("tri", TopSimplex([0; 1; 2]));
    DLet("bd", TopOp("boundary", [Var("tri")]));
    DLet("_", Apply(Var("println"), [Var("bd")]))
]
```

## Вклад команды

| Имя | Роль в проекте |
|-----|----------------|
| Тертычный Олег | я            |
| Севастьянов Иван | люблю            |
| Снетков Никита | олега            |


## Использование генеративного ИИ

Если использовались инструменты генеративного ИИ (например, ChatGPT, GitHub Copilot), они помогли в:
- Создании структуры документации и примеров.
- Отладке синтаксических ошибок в F#.
