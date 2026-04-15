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


# ============== ТЕСТЫ ФАЙЛОВОЙ СИСТЕМЫ ==============
class TestFileSystem:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.fs = FileSystem(self.temp_dir)
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_save_and_load(self):
        assert self.fs.save("test.txt", "Hello World") is True
        content = self.fs.load("test.txt")
        assert content == "Hello World"
    
    def test_load_nonexistent(self):
        assert self.fs.load("missing.txt") is None
    
    def test_list_files(self):
        self.fs.save("a.txt", "A")
        self.fs.save("b.txt", "B")
        files = self.fs.list_files()
        assert "a.txt" in files
        assert "b.txt" in files
    
    def test_delete_file(self):
        self.fs.save("delete.txt", "Content")
        assert self.fs.delete("delete.txt") is True
        assert self.fs.load("delete.txt") is None


# ============== ТЕСТЫ РЕДАКТОРА ==============
class TestTextEditor:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.fs = FileSystem(self.temp_dir)
        self.editor = TextEditor(self.fs)
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_create_new(self):
        assert self.editor.create_new("doc.txt") is True
        assert self.editor.current_file == "doc.txt"
        assert self.editor.content == ""
    
    def test_insert_text_at_end(self):
        self.editor.create_new("doc.txt")
        self.editor.insert_text("Hello")
        assert self.editor.content == "Hello"
        self.editor.insert_text(" World")
        assert self.editor.content == "Hello World"
    
    def test_insert_text_at_position(self):
        self.editor.create_new("doc.txt")
        self.editor.insert_text("Hello World")
        self.editor.insert_text("Beautiful ", position=6)
        assert self.editor.content == "Hello Beautiful World"
    
    def test_delete_text(self):
        self.editor.create_new("doc.txt")
        self.editor.insert_text("Hello World")
        self.editor.delete_text(0, 5)
        assert self.editor.content == " World"
    
    def test_delete_text_invalid_bounds(self):
        self.editor.create_new("doc.txt")
        self.editor.insert_text("Hello")
        assert self.editor.delete_text(10, 5) is False
    
    def test_find_and_replace(self):
        self.editor.create_new("doc.txt")
        self.editor.insert_text("foo bar foo baz")
        count = self.editor.find_and_replace("foo", "qux")
        assert count == 2
        assert self.editor.content == "qux bar qux baz"
    
    def test_save_and_open(self):
        self.editor.create_new("test.txt")
        self.editor.insert_text("Saved content")
        assert self.editor.save() is True
        
        new_editor = TextEditor(self.fs)
        assert new_editor.open("test.txt") is True
        assert new_editor.content == "Saved content"


# ============== ТЕСТЫ СЛОВ ==============
class TestWord:
    def test_word_creation(self):
        w = Word("Hello")
        assert w.text == "Hello"
    
    def test_capitalize(self):
        w = Word("hello")
        assert w.capitalize().text == "Hello"
    
    def test_upper(self):
        w = Word("hello")
        assert w.upper().text == "HELLO"
    
    def test_lower(self):
        w = Word("HELLO")
        assert w.lower().text == "hello"
    
    def test_len(self):
        assert len(Word("Hello")) == 5


# ============== ТЕСТЫ ПРЕДЛОЖЕНИЙ ==============
class TestSentence:
    def test_from_string(self):
        s = Sentence.from_string("Hello world!")
        assert len(s.words) == 2
        assert s.words[0].text == "Hello"
    
    def test_get_text(self):
        s = Sentence.from_string("Hello beautiful world")
        assert s.get_text() == "Hello beautiful world"
    
    def test_word_count(self):
        s = Sentence.from_string("One two three four")
        assert s.word_count() == 4


# ============== ТЕСТЫ АБЗАЦЕВ ==============
class TestParagraph:
    def test_from_string(self):
        p = Paragraph.from_string("First sentence. Second sentence!")
        assert p.sentence_count() == 2
    
    def test_get_text(self):
        p = Paragraph.from_string("Hello world. How are you?")
        text = p.get_text()
        assert "Hello" in text
        assert "world" in text


# ============== ТЕСТЫ ТАБЛИЦ ==============
class TestTable:
    def test_get_column_widths(self):
        headers = ["Name", "Age"]
        rows = [["Alice", "25"], ["Bob", "100"]]
        table = Table(headers, rows)
        widths = table.get_column_widths()
        assert widths[0] >= 4  # "Name" or "Bob"
        assert widths[1] >= 3  # "Age" or "100"
    
    def test_render(self):
        headers = ["A", "B"]
        rows = [["1", "2"]]
        table = Table(headers, rows)
        rendered = table.render(cell_width=5)
        assert "| A | B |" in rendered
        assert "| 1 | 2 |" in rendered


# ============== ТЕСТЫ ФОРМАТОРА ==============
class TestFormatter:
    def setup_method(self):
        self.formatter = Formatter(page_width=40)
    
    def test_split_into_words(self):
        words = self.formatter.split_into_words("Hello, world! How are you?")
        assert len(words) == 5
        assert words[0].text == "Hello"
    
    def test_split_into_sentences(self):
        sentences = self.formatter.split_into_sentences("First. Second! Third?")
        assert len(sentences) == 3
    
    def test_split_into_paragraphs(self):
        text = "First paragraph.\n\nSecond paragraph.\n\nThird."
        paragraphs = self.formatter.split_into_paragraphs(text)
        assert len(paragraphs) == 3
    
    def test_wrap_line(self):
        words = [Word("a"), Word("b"), Word("c")]
        line, remaining = self.formatter.wrap_line(words, max_width=3)
        assert len(line) == 2
        assert len(remaining) == 1
    
    def test_format_paragraph(self):
        p = Paragraph.from_string("This is a test paragraph.")
        formatted = self.formatter.format_paragraph(p, indent=0)
        assert isinstance(formatted, str)
    
    def test_format_document_with_title(self):
        result = self.formatter.format_document("Hello world", title="My Title")
        assert "My Title" in result
        assert "===" in result
    
    def test_format_document_without_title(self):
        result = self.formatter.format_document("Just text")
        assert "Just text" in result
    
    def test_format_table(self):
        headers = ["Col1", "Col2"]
        rows = [["Data1", "Data2"]]
        table = Table(headers, rows)
        formatted = self.formatter.format_table(table)
        assert "Col1" in formatted
        assert "Data1" in formatted
    
    def test_format_document_with_tables(self):
        headers = ["X", "Y"]
        rows = [["1", "2"]]
        table = Table(headers, rows)
        result = self.formatter.format_document_with_tables(
            "Here is data:", [table], title="Report"
        )
        assert "Report" in result
        assert "Here is data" in result
        assert "X" in result


# ============== ТЕСТЫ НАБОРЩИКА ==============
class TestTypesetter:
    def setup_method(self):
        self.typesetter = Typesetter(font_size=14, line_spacing=1.8)
    
    def test_get_print_commands(self):
        commands = self.typesetter.get_print_commands("Line1\nLine2")
        assert "SET_FONT_SIZE 14" in commands
        assert "SET_LINE_SPACING 1.8" in commands
        assert "PRINT 'Line1'" in commands
        assert "PRINT 'Line2'" in commands
        assert "EJECT_PAGE" in commands
    
    def test_render_to_file(self):
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
    
    def test_render_to_file_failure(self):
        # Передаём недопустимый путь
        result = self.typesetter.render_to_file("Content", "/invalid/path/file.json")
        assert result is False


# ============== ТЕСТЫ ПОЛНОЙ СИСТЕМЫ ==============
class TestPublishingSystem:
    def setup_method(self):
        self.system = PublishingSystem()
        self.temp_dir = tempfile.mkdtemp()
        self.system.fs = FileSystem(self.temp_dir)
        self.system.editor = TextEditor(self.system.fs)
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_create_publication(self):
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


# ============== ЗАПУСК ТЕСТОВ ==============
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=text_formatter", "--cov-report=term-missing"])
    