import pytest
import os
import json
import tempfile
import shutil
from pathlib import Path

from text_formatter import (
    FileSystem, TextEditor, Word, Sentence, Paragraph, Table,
    Formatter, Typesetter, PublishingSystem
)


class TestFileSystem:                       # ТЕСТЫ ФАЙЛОВОЙ СИСТЕМЫ
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.fs = FileSystem(self.temp_dir)
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_save_and_load(self):                      # проверка сохранения и загрузки файла
        assert self.fs.save("test.txt", "Hello World") is True
        content = self.fs.load("test.txt")
        assert content == "Hello World"
    
    def test_load_nonexistent(self):                   # проверка загрузки несуществующего файла
        assert self.fs.load("missing.txt") is None
    
    def test_list_files(self):                         # проверка получения списка файлов
        self.fs.save("a.txt", "A")
        self.fs.save("b.txt", "B")
        files = self.fs.list_files()
        assert "a.txt" in files
        assert "b.txt" in files
    
    def test_delete_file(self):                        # проверка удаления файла
        self.fs.save("delete.txt", "Content")
        assert self.fs.delete("delete.txt") is True
        assert self.fs.load("delete.txt") is None


class TestTextEditor:                       # ТЕСТЫ РЕДАКТОРА
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.fs = FileSystem(self.temp_dir)
        self.editor = TextEditor(self.fs)
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_create_new(self):                          # Тест создания нового документа
        assert self.editor.create_new("doc.txt") is True
        assert self.editor.current_file == "doc.txt"
        assert self.editor.content == ""
    
    def test_insert_text_at_end(self):                  # Тест вставки текста в конец
        self.editor.create_new("doc.txt")
        self.editor.insert_text("Hello")
        assert self.editor.content == "Hello"
        self.editor.insert_text(" World")
        assert self.editor.content == "Hello World"
    
    def test_insert_text_at_position(self):             # Тест вставки текста в указанную позицию
        self.editor.create_new("doc.txt")
        self.editor.insert_text("Hello World")
        self.editor.insert_text("Beautiful ", position=6)
        assert self.editor.content == "Hello Beautiful World"
    
    def test_delete_text(self):                         # Тест удаления текста
        self.editor.create_new("doc.txt")
        self.editor.insert_text("Hello World")
        self.editor.delete_text(0, 5)
        assert self.editor.content == " World"
    
    def test_delete_text_invalid_bounds(self):          # Тест удаления с некорректными границами
        self.editor.create_new("doc.txt")
        self.editor.insert_text("Hello")
        assert self.editor.delete_text(10, 5) is False
    
    def test_find_and_replace(self):                    # Тест поиска и замены
        self.editor.create_new("doc.txt")
        self.editor.insert_text("foo bar foo baz")
        count = self.editor.find_and_replace("foo", "qux")
        assert count == 2
        assert self.editor.content == "qux bar qux baz"
    
    def test_save_and_open(self):                       # Тест сохранения и открытия файла
        self.editor.create_new("test.txt")
        self.editor.insert_text("Saved content")
        assert self.editor.save() is True
        
        new_editor = TextEditor(self.fs)
        assert new_editor.open("test.txt") is True
        assert new_editor.content == "Saved content"


class TestWord:                             # ТЕСТЫ СЛОВ
    def test_word_creation(self):                      # Проверяет корректность инициализации
        w = Word("Hello")
        assert w.text == "Hello"
    
    def test_capitalize(self):                         # Проверяет преобразование первой буквы в заглавную
        w = Word("hello")
        assert w.capitalize().text == "Hello"
    
    def test_upper(self):                              # Проверяет преобразование всех букв в ЗАГЛАВНЫЕ
        w = Word("hello")
        assert w.upper().text == "HELLO"
    
    def test_lower(self):                              # Проверяет преобразование всех букв в строчные
        w = Word("HELLO")
        assert w.lower().text == "hello"
    
    def test_len(self):                                # Проверяет, что можно получить длину слова через len()
        assert len(Word("Hello")) == 5


class TestSentence:                          # ТЕСТЫ ПРЕДЛОЖЕНИЙ
    def test_from_string(self):                        # Проверяет создание объекта Sentence из строки
        s = Sentence.from_string("Hello world!")
        assert len(s.words) == 2
        assert s.words[0].text == "Hello"
    
    def test_get_text(self):                           # Проверяет преобразование предложения обратно в строку
        s = Sentence.from_string("Hello beautiful world")
        assert s.get_text() == "Hello beautiful world"
    
    def test_word_count(self):                         # Проверяет подсчёт количества слов в предложении
        s = Sentence.from_string("One two three four")
        assert s.word_count() == 4


class TestParagraph:                         # ТЕСТЫ АБЗАЦЕВ
    def test_from_string(self):                        # Проверяет создание объекта Paragraph из строки с несколькими предложениями
        p = Paragraph.from_string("First sentence. Second sentence!")
        assert p.sentence_count() == 2
    
    def test_get_text(self):                           # Проверяет преобразование абзаца обратно в строку
        p = Paragraph.from_string("Hello world. How are you?")
        text = p.get_text()
        assert "Hello" in text
        assert "world" in text


class TestTable:                             # ТЕСТЫ ТАБЛИЦ
    def test_get_column_widths(self):                  # Проверяет вычисление оптимальной ширины колонок таблицы
        headers = ["Name", "Age"]
        rows = [["Alice", "25"], ["Bob", "100"]]
        table = Table(headers, rows)
        widths = table.get_column_widths()
        assert widths[0] >= 4  # "Name" or "Bob"
        assert widths[1] >= 3  # "Age" or "100"
    
    def test_render(self):                             # Проверяет отрисовку таблицы в виде строки
        headers = ["A", "B"]
        rows = [["1", "2"]]
        table = Table(headers, rows)
        rendered = table.render(cell_width=5)
        assert "| A | B |" in rendered
        assert "| 1 | 2 |" in rendered


class TestFormatter:                         # ТЕСТЫ ФОРМАТОРА
    def setup_method(self):
        self.formatter = Formatter(page_width=40)
    
    def test_split_into_words(self):                    # Проверяет разбивку текста на отдельные слова
        words = self.formatter.split_into_words("Hello, world! How are you?")
        assert len(words) == 5
        assert words[0].text == "Hello"
    
    def test_split_into_sentences(self):                # Проверяет разбивку текста на предложения
        sentences = self.formatter.split_into_sentences("First. Second! Third?")
        assert len(sentences) == 3
    
    def test_split_into_paragraphs(self):               # Проверяет разбивку текста на абзацы по двойным переносам строк
        text = "First paragraph.\n\nSecond paragraph.\n\nThird."
        paragraphs = self.formatter.split_into_paragraphs(text)
        assert len(paragraphs) == 3
    
    def test_wrap_line(self):                           # Проверяет перенос строки (разбиение списка слов на строки)
        words = [Word("a"), Word("b"), Word("c")]
        line, remaining = self.formatter.wrap_line(words, max_width=3)
        assert len(line) == 2
        assert len(remaining) == 1
    
    def test_format_paragraph(self):                    # Проверяет форматирование одного абзаца
        p = Paragraph.from_string("This is a test paragraph.")
        formatted = self.formatter.format_paragraph(p, indent=0)
        assert isinstance(formatted, str)
    
    def test_format_document_with_title(self):          # Тест форматирования документа с заголовком
        result = self.formatter.format_document("Hello world", title="My Title")
        assert "My Title" in result
        assert "===" in result
    
    def test_format_document_without_title(self):       # Тест форматирования документа без заголовка
        result = self.formatter.format_document("Just text")
        assert "Just text" in result
    
    def test_format_table(self):                        # Тест форматирования таблицы
        headers = ["Col1", "Col2"]
        rows = [["Data1", "Data2"]]
        table = Table(headers, rows)
        formatted = self.formatter.format_table(table)
        assert "Col1" in formatted
        assert "Data1" in formatted
    
    def test_format_document_with_tables(self):        # Тест форматирования документа с таблицами
        headers = ["X", "Y"]
        rows = [["1", "2"]]
        table = Table(headers, rows)
        result = self.formatter.format_document_with_tables(
            "Here is data:", [table], title="Report"
        )
        assert "Report" in result
        assert "Here is data" in result
        assert "X" in result


class TestTypesetter:                       # ТЕСТЫ НАБОРЩИКА
    def setup_method(self):
        self.typesetter = Typesetter(font_size=14, line_spacing=1.8)
    
    def test_get_print_commands(self):                  # Проверяет генерацию команд для печати
        commands = self.typesetter.get_print_commands("Line1\nLine2")
        assert "SET_FONT_SIZE 14" in commands
        assert "SET_LINE_SPACING 1.8" in commands
        assert "PRINT 'Line1'" in commands
        assert "PRINT 'Line2'" in commands
        assert "EJECT_PAGE" in commands
    
    def test_render_to_file(self):                      # Тест успешного сохранения в файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = self.typesetter.render_to_file("Test content", tmp_path)
            assert result is True
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert data["font_size"] == 14
            assert data["line_spacing"] == 1.8
            assert data["content"] == "Test content"
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_render_to_file_failure(self):              # Тест обработки ошибок при сохранении
        # Передаём недопустимый путь
        result = self.typesetter.render_to_file("Content", "/invalid/path/file.json")
        assert result is False


class TestPublishingSystem:                 # ТЕСТЫ ПОЛНОЙ СИСТЕМЫ
    def setup_method(self):
        self.system = PublishingSystem()
        self.temp_dir = tempfile.mkdtemp()
        self.system.fs = FileSystem(self.temp_dir)
        self.system.editor = TextEditor(self.system.fs)
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_create_publication(self):                 # Тест полного цикла публикации
        result = self.system.create_publication(
            filename="test.txt",
            content="Hello world",
            title="Test Title"
        )
        assert result is True
        
        # Проверяем, что файл сохранён
        assert self.system.fs.load("test.txt") == "Hello world"
        
        # JSON создаётся в текущей рабочей директории, а не в temp_dir
        json_path = Path("test_formatted.json")
        assert json_path.exists()
        
        # Очистка после теста
        if json_path.exists():
            json_path.unlink()


# ЗАПУСК ТЕСТОВ
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=text_formatter", "--cov-report=term-missing"])
    