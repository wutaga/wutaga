# Руководство по автотестам

## Установка окружения

### Установка Python
- Установите Python (3.8+) с [python.org](https://www.python.org/).
- Отметьте "Add Python to PATH".

### Виртуальное окружение
1. Создайте окружение: `python -m venv venv`.
2. Активируйте:
   - Linux/MacOS: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

### Установка зависимостей
`pip install -r requirements.txt`

---

## Запуск тестов

### Базовый запуск
`pytest test_file.py`

### Headless-режим
`pytest test_file.py --headless`