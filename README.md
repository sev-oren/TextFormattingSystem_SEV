# Автоматическое форматирование текста

***
## Описание

Разработанная система представляет собой программный комплекс для автоматической подготовки текстовых публикаций к печати в типографии. Система состоит из четырех основных компонентов, каждый из которых выполняет свою функцию в процессе обработки текста.

### Основные компоненты

1. **Файловая система (FileSystem)** - управление хранением текстовых документов
2. **Редактор текста (TextEditor)** - внесение изменений и правок в документы
3. **Форматор (Formatter)** - форматирование текста (заголовки, абзацы, отступы)
4. **Наборщик (Typesetter)** - вывод форматированного текста на устройство печати

## Установка и запуск

### Клонирование репозитория

```bash
    git clone https://github.com/sev-oren/TextFormattingSystem_SEV.git
    cd TextFormattingSystem_SEV
```

### Установка зависимостей

```bash
    pip install -r requirements.txt
```

Или вручную:

```bash
    pip install pytest pytest-cov
```

### Запуск демонстрации

```bash
    python complete_demo.py
```

### Запуск тестов

```bash
    pytest test_text_formatter.py -v
```

### Проверка покрытия кода

```bash
    coverage run -m pytest test_text_formatter.py  # тесты
    coverage report -m
```

Для просмотра HTML-отчёта:

```bash
    coverage html
    start htmlcov/index.html
```

Затем откроется htmlcov/index.html в браузере.

Очистить старую статистику:

```bash
    coverage erase
```

## Требования

- Python 3.8+

- pytest 7.0+

- pytest-cov 4.0+

***
## Выполнила
Степанова Е.В., гр. 5140904/50401
 