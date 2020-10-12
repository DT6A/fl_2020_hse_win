# Парсер-комбинаторы 

## Parsita
[Описание библиотеки](https://pypi.org/project/parsita/#:~:text=Parsita%20is%20a%20parser%20combinator,are%20the%20easiest%20to%20write.).

Установка
```buildoutcfg
pip install parsita
```

## Использование
Построить AST по файлу (пишет в выходной файл ошибку в случае неудачи) 
```buildoutcfg
python parse_comb/combinators.py <file name>
```
Запуск тестов
```buildoutcfg
python parse_comb/tests.py
```