import sys
import os
import time
from pathlib import Path

# Добавляем родительскую папку для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем нашу систему
from text_formatter import (
    FileSystem, TextEditor, Formatter, 
    Typesetter, PublishingSystem, Table
)

class ColorPrint:
    """Класс для цветного вывода в консоль"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def print_success(text):
        print(f"{ColorPrint.GREEN}✓ {text}{ColorPrint.RESET}")
    
    @staticmethod
    def print_error(text):
        print(f"{ColorPrint.RED}✗ {text}{ColorPrint.RESET}")
    
    @staticmethod
    def print_info(text):
        print(f"{ColorPrint.BLUE}ℹ {text}{ColorPrint.RESET}")
    
    @staticmethod
    def print_title(text):
        print(f"\n{ColorPrint.BOLD}{ColorPrint.PURPLE}{'='*70}{ColorPrint.RESET}")
        print(f"{ColorPrint.BOLD}{ColorPrint.PURPLE}{text.center(70)}{ColorPrint.RESET}")
        print(f"{ColorPrint.BOLD}{ColorPrint.PURPLE}{'='*70}{ColorPrint.RESET}\n")
    
    @staticmethod
    def print_step(step_num, text):
        print(f"{ColorPrint.YELLOW}Шаг {step_num}:{ColorPrint.RESET} {text}")
        print("-" * 50)


def wait_for_user():
    """Ожидание нажатия Enter для продолжения"""
    input(f"\n{ColorPrint.CYAN}Нажмите Enter для продолжения...{ColorPrint.RESET}")


def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')


def demo_intro():
    """Вступительная часть"""
    clear_screen()
    print(f"""
{ColorPrint.BOLD}{ColorPrint.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                 АВТОМАТИЧЕСКОЕ ФОРМАТИРОВАНИЕ ТЕКСТА                 ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{ColorPrint.RESET}
    """)


def demo_filesystem():
    """Демонстрация 1: Файловая система"""
    ColorPrint.print_title("ЧАСТЬ 1: ФАЙЛОВАЯ СИСТЕМА")
    
    ColorPrint.print_step("1.1", "Инициализация файловой системы")
    fs = FileSystem("./demo_documents")
    ColorPrint.print_success("Файловая система создана")
    
    ColorPrint.print_step("1.2", "Сохранение документа")
    result = fs.save("demo1.txt", "Содержимое первого документа")
    if result:
        ColorPrint.print_success("Документ 'demo1.txt' сохранен")
    
    ColorPrint.print_step("1.3", "Сохранение второго документа")
    fs.save("demo2.txt", "Содержимое второго документа\nСо второй строкой")
    ColorPrint.print_success("Документ 'demo2.txt' сохранен")
    
    ColorPrint.print_step("1.4", "Просмотр списка файлов")
    files = fs.list_files()
    print(f"  Файлы в системе: {files}")
    ColorPrint.print_success(f"Всего файлов: {len(files)}")
    
    ColorPrint.print_step("1.5", "Загрузка документа")
    content = fs.load("demo1.txt")
    print(f"  Содержимое 'demo1.txt': '{content}'")
    content2 = fs.load("demo2.txt")
    print(f"  Содержимое 'demo2.txt':")
    print(f"    {content2}")
    ColorPrint.print_success("Документ загружен успешно")
    
    wait_for_user()


def demo_editor():
    """Демонстрация 2: Редактор текста"""
    ColorPrint.print_title("ЧАСТЬ 2: РЕДАКТОР ТЕКСТА")
    
    ColorPrint.print_step("2.1", "Создание редактора")
    fs = FileSystem("./demo_documents")
    editor = TextEditor(fs)
    ColorPrint.print_success("Редактор создан")
    
    ColorPrint.print_step("2.2", "Создание нового документа")
    editor.create_new("article.txt")
    editor.insert_text("Это пример текста.")
    editor.save()
    print(f"  Текущий файл: {editor.current_file}")
    print(f"  Содержимое: '{editor.content}'")
    ColorPrint.print_success("Документ создан")
    input("  Нажмите Enter чтобы увидеть вставку в конец...")
    
    ColorPrint.print_step("2.3", "Вставка текста в конец")
    editor.insert_text(" Добавлен новый текст.")
    editor.save()
    print(f"  После вставки: '{editor.content}'")
    ColorPrint.print_success("Текст добавлен")
    input("  Нажмите Enter чтобы увидеть вставку в середину...")
    
    ColorPrint.print_step("2.4", "Вставка текста в указанную позицию")
    editor.insert_text("ОЧЕНЬ ВАЖНЫЙ ТЕКСТ ", position=4)
    editor.save()
    print(f"  После вставки: '{editor.content}'")
    ColorPrint.print_success("Текст вставлен в позицию 4")
    input("  Нажмите Enter чтобы увидеть поиск и замену...")
    
    ColorPrint.print_step("2.5", "Поиск и замена")
    count = editor.find_and_replace("пример", "образец")
    editor.save()
    print(f"  Найдено и заменено вхождений: {count}")
    print(f"  Результат: '{editor.content}'")
    ColorPrint.print_success("Замена выполнена")
    input("  Нажмите Enter чтобы увидеть удаление текста...")
    
    ColorPrint.print_step("2.6", "Удаление текста")
    editor.delete_text(4, 22)
    editor.save()
    print(f"  После удаления: '{editor.content}'")
    ColorPrint.print_success("Текст удален")
    
    editor.save()
    ColorPrint.print_success("Изменения сохранены")
    
    wait_for_user()


def demo_formatter():
    """Демонстрация 3: Форматор"""
    ColorPrint.print_title("ЧАСТЬ 3: ФОРМАТОР")
    
    ColorPrint.print_step("3.1", "Инициализация форматера")
    formatter = Formatter(page_width=60, page_height=50)
    print(f"  Ширина страницы: {formatter.page_width}")
    print(f"  Высота страницы: {formatter.page_height}")
    ColorPrint.print_success("Форматер создан")
    
    ColorPrint.print_step("3.2", "Разбивка на слова")
    text = "Привет, мир! Как дела?"
    words = formatter.split_into_words(text)
    print(f"  Исходный текст: '{text}'")
    print(f"  Слова: {[w.text for w in words]}")
    ColorPrint.print_success(f"Найдено {len(words)} слов")
    
    ColorPrint.print_step("3.3", "Разбивка на предложения")
    sentences = formatter.split_into_sentences("Первое предложение. Второе предложение! Третье?")
    print(f"  Количество предложений: {len(sentences)}")
    for i, s in enumerate(sentences, 1):
        print(f"    Предложение {i}: '{s.get_text()}'")
    ColorPrint.print_success("Предложения выделены")
    
    ColorPrint.print_step("3.4", "Разбивка на абзацы")
    paragraphs_text = "Первый абзац.\n\nВторой абзац с текстом.\n\nТретий абзац."
    paragraphs = formatter.split_into_paragraphs(paragraphs_text)
    print(f"  Количество абзацев: {len(paragraphs)}")
    for i, p in enumerate(paragraphs, 1):
        preview = p.get_text()[:50] + "..." if len(p.get_text()) > 50 else p.get_text()
        print(f"    Абзац {i}: '{preview}'")
    ColorPrint.print_success("Абзацы выделены")
    
    wait_for_user()


def demo_formatting():
    """Демонстрация 4: Форматирование документа"""
    ColorPrint.print_title("ЧАСТЬ 4: ФОРМАТИРОВАНИЕ ДОКУМЕНТА")
    
    formatter = Formatter(page_width=60)
    
    ColorPrint.print_step("4.1", "Форматирование без заголовка")
    text = "Это тестовый документ для демонстрации работы форматера. "
    text += "Он автоматически разбивается на строки нужной длины. "
    text += "Слова не разрываются."
    
    formatted = formatter.format_document(text)
    print(formatted)
    ColorPrint.print_success("Форматирование выполнено")

    ColorPrint.print_step("4.2", "Форматирование с заголовком")
    formatted_with_title = formatter.format_document(
        "Короткий текст для демонстрации заголовка.",
        title="ВАЖНЫЙ ДОКУМЕНТ"
    )
    print(formatted_with_title)
    ColorPrint.print_success("Форматирование с заголовком выполнено")
    
    
    ColorPrint.print_step("4.3", "Форматирование ТАБЛИЦЫ")
    
    # Создаем таблицу
    headers = ["Название", "Количество", "Цена"]
    rows = [
        ["Книга", "10", "500 ₽"],
        ["Ручка", "50", "50 ₽"],
        ["Блокнот", "25", "150 ₽"]
    ]
    
    table = Table(headers, rows)
    
    print(formatter.format_table(table))
    ColorPrint.print_success("Таблица отформатирована")
    
    ColorPrint.print_step("4.4", "Документ с текстом и таблицей")
    
    doc_with_table = formatter.format_document_with_tables(
        text="Ниже представлена статистика товаров на складе:",
        tables=[table],
        title="ОТЧЕТ ПО ТОВАРАМ"
    )
    

    print(doc_with_table)
    ColorPrint.print_success("Документ с таблицей создан")

    wait_for_user()


def demo_typesetter():
    """Демонстрация 5: Наборщик"""
    ColorPrint.print_title("ЧАСТЬ 5: НАБОРЩИК")
    
    ColorPrint.print_step("5.1", "Инициализация наборщика")
    typesetter = Typesetter(font_size=14, line_spacing=1.8)
    print(f"  Размер шрифта: {typesetter.font_size}pt")
    print(f"  Интерлиньяж: {typesetter.line_spacing}")
    ColorPrint.print_success("Наборщик создан")
    
    ColorPrint.print_step("5.2", "Генерация команд для печати")
    formatted_text = "Первая строка текста\nВторая строка\nТретья строка"
    commands = typesetter.get_print_commands(formatted_text)
    
    print("\n  Сгенерированные команды:")
    for i, cmd in enumerate(commands, 1):
        print(f"    {i}. {cmd}")
    
    ColorPrint.print_success(f"Сгенерировано {len(commands)} команд")
    
    ColorPrint.print_step("5.3", "Сохранение в файл")
    result = typesetter.render_to_file(formatted_text, "output_demo.json")
    if result:
        ColorPrint.print_success("Файл 'output_demo.json' создан")
        # Покажем содержимое файла с правильной обработкой кодировки
        try:
            import json
            # Пробуем разные кодировки
            encodings = ['utf-8', 'cp1251', 'latin-1', 'koi8-r']
            data = None
            
            for encoding in encodings:
                try:
                    with open("output_demo.json", 'r', encoding=encoding) as f:
                        data = json.load(f)
                    print(f"\n  Файл прочитан в кодировке: {encoding}")
                    break
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
            
            if data:
                print(f"\n  Содержимое файла:")
                print(f"    Шрифт: {data['font_size']}pt")
                print(f"    Интерлиньяж: {data['line_spacing']}")
                print(f"    Текст: {data['content'][:50]}...")
            else:
                # Если не удалось прочитать как JSON, покажем сырое содержимое
                with open("output_demo.json", 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                print(f"\n  Содержимое файла (raw):")
                print(f"    {content[:200]}...")
        except Exception as e:
            ColorPrint.print_error(f"Не удалось прочитать файл: {e}")
    
    wait_for_user()


def demo_publishing():
    """Демонстрация 6: Полный цикл публикации"""
    ColorPrint.print_title("ЧАСТЬ 6: ПОЛНЫЙ ЦИКЛ ПУБЛИКАЦИИ")
    
    ColorPrint.print_step("6.1", "Создание публикации через PublishingSystem")
    system = PublishingSystem()
    
    content = """Демонстрирую свою работу =)

Данная система предназначена для автоматического форматирования текстовых документов.

Она включает в себя четыре основных компонента:
1. Файловая система для хранения документов
2. Редактор для внесения изменений
3. Форматор для правильного расположения текста
4. Наборщик для вывода на печать

Продемонстрировала Степанова Е.В."""
    
    result = system.create_publication(
        filename="demo.txt",
        content=content,
        title="КУРСОВАЯ РАБОТА"
    )
    
    if result:
        ColorPrint.print_success("Публикация успешно создана!")
    
    wait_for_user()


def demo_cleanup():
    """Очистка после демонстрации"""
    ColorPrint.print_title("ЗАВЕРШЕНИЕ ДЕМОНСТРАЦИИ")
    
    print("Созданные файлы во время демонстрации:")
    demo_files = Path(".").glob("*.json")
    for f in demo_files:
        print(f"  • {f}")
    
    demo_docs = Path("./demo_documents")
    if demo_docs.exists():
        print(f"  • Папка {demo_docs} с документами")
    
    choice = input(f"\n{ColorPrint.YELLOW}Удалить созданные файлы? (y/n): {ColorPrint.RESET}")
    if choice.lower() == 'y':
        import shutil
        for f in Path(".").glob("*.json"):
            f.unlink()
        if demo_docs.exists():
            shutil.rmtree(demo_docs)
        ColorPrint.print_success("Временные файлы удалены")
    else:
        ColorPrint.print_info("Файлы сохранены для дальнейшего просмотра")


def demo_outro():
    """Заключительная часть"""
    clear_screen()
    print(f"""
{ColorPrint.BOLD}{ColorPrint.GREEN}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                         ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{ColorPrint.RESET}
    """)
    
    print(f"\n{ColorPrint.BOLD}Выполнила:{ColorPrint.RESET}")
    print("  Степанова Е.В.")
    print("  Группа: 5140904/50401")
    
    print("\n")


def main():
    """Главная функция демонстрации"""
    print("Загрузка демонстрационной программы...")
    time.sleep(1)
    
    demo_intro()
    demo_filesystem()
    demo_editor()
    demo_formatter()
    demo_formatting()
    demo_typesetter()
    demo_publishing()
    demo_cleanup()
    demo_outro()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{ColorPrint.YELLOW}Демонстрация прервана пользователем{ColorPrint.RESET}")
    except Exception as e:
        print(f"{ColorPrint.RED}Ошибка: {e}{ColorPrint.RESET}")
        import traceback
        traceback.print_exc()
        