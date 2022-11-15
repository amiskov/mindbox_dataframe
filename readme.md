# Add Sessions to DataFrame

## Задача
Есть Pandas DataFrame со столбцами `["customer_id", "product_id", "timestamp"]`, который содержит данные по просмотрам товаров на сайте.

Есть проблема – просмотры *одного* `customer_id` не разбиты на сессии (появления на сайте). Мы хотим разместить сессии так, чтобы сессией считались все смежные просмотры, между которыми не более 3 минут.

Написать метод, который создаст в Pandas DataFrame столбец `session_id` и проставит в нем уникальный `int id` для каждой сессии.

У каждого пользователя может быть по несколько сессий. Исходный DataFrame может быть большим, до 100 млн строк.

## Понимание
Сессия — непрерывное пребывание кастомера от 0 до 3 минут. Если строки отсортировать по `timestamp`, то сессия — это набор строк подряд, где `customer_id` один и тот же и `timestamp` отклоняется на <= 3 минуты от стартового значения.

## Решение
- отсортировать данные по `timestamp`;
- взять `timestamp` из первой строки за стартовый;
- пройтись по строкам, проставляя одинаковый `session_id` тем, в которых одинаковый `customer_id` и `timestamp` увеличивается от стартового не более чем на 3 минуты;
- новой сессией считаем случаи, когда:
  - меняется `customer_id`;
  - `timestamp` больше первого в группе на 3 минуты.

Датасет может быть большой, поэтому меняем его in-place и используем библиотеку `pandarallel` для распараллеливания вычислений. В качестве `session_id` будем использовать просто сумму `customer_id+timestamp`, т.к. по условию нам нужен `int` и сумма считается быстро.

## Тесты
Запустить тесты:

```sh
make test
# or
pytest .
```

## Benchmark
Можно запустить генерацию большого датасета, задав размер аргументом в командной строке:

```sh
make bench
# or
python benchmark.py --ds-size=100000000
```

В текущей реализации датасет из 100_000_000 записей обработался на 4 ядрах по 2.2GHz за 15 минут.
