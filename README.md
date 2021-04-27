## mygrep
Аналог утилиты `grep`, которая выполняет поиск указанной подстроки во всеx файлах указанной директории и всех её поддиректорий.

`mygrep [path] [substring]`

### Примеры вызова

Пусть в текущей директории есть два файла:
`>> cat f1.py`

```python
print("Hello, world!")
```

`>> cat f2.txt`

```
world
hello
```

Вызов: `mygrep . "Hello"`

Результат:

```
f1.py line=1: print("Hello, world!")
```

Вызов: `mygrep . world`

Результат:

```
f1.py line=1: print("Hello, world!")
f2.txt line=2: hello
```

### Makefile

- `make venv` - для установки виртуального окружения
- `make test` - для запуска тестов
- `make lint` - для запуска линтера
- `make format` - для форматирования кода
- `make ci` - для запуская линтера и тестов

### setup.py

Для установки пакета запустите

```
python3 setup.py install
```

После установки появится команда `mygrep [path] [substring]`

