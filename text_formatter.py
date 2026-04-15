# text_formatter.py
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime


# ============== КОМПОНЕНТ 1: ФАЙЛОВАЯ СИСТЕМА ==============
class FileSystem:
    """Хранение текстовых файлов"""
    
    def __init__(self, base_path: str = "./documents"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self._files: Dict[str, str] = {}
        self._load_existing_files()
    
    def _load_existing_files(self):
        """Загрузка существующих файлов из директории"""
        for file_path in self.base_path.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self._files[file_path.name] = f.read()
            except Exception:
                pass
    
    def save(self, filename: str, content: str) -> bool:
        """Сохранение файла"""
        try:
            file_path = self.base_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self._files[filename] = content
            return True
        except Exception:
            return False
    
    def load(self, filename: str) -> Optional[str]:
        """Загрузка файла"""
        file_path = self.base_path / filename
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self._files[filename] = content
                    return content
            except Exception:
                return None
        return self._files.get(filename)
    
    def list_files(self) -> List[str]:
        """Список файлов"""
        files = set(self._files.keys())
        for file_path in self.base_path.glob("*.txt"):
            files.add(file_path.name)
        return sorted(list(files))
    
    def delete(self, filename: str) -> bool:
        """Удаление файла"""
        file_path = self.base_path / filename
        if filename in self._files:
            del self._files[filename]
        if file_path.exists():
            file_path.unlink()
            return True
        return False


# ============== КОМПОНЕНТ 2: РЕДАКТОР ТЕКСТА ==============
class TextEditor:
    """Редактирование текстовых файлов"""
    
    def __init__(self, file_system: FileSystem):
        self.fs = file_system
        self.current_file: Optional[str] = None
        self.content: str = ""
    
    def create_new(self, filename: str) -> bool:
        """Создание нового документа"""
        self.current_file = filename
        self.content = ""
        return True
    
    def open(self, filename: str) -> bool:
        """Открытие существующего документа"""
        content = self.fs.load(filename)
        if content is not None:
            self.current_file = filename
            self.content = content
            return True
        return False
    
    def insert_text(self, text: str, position: Optional[int] = None) -> bool:
        """Вставка текста в указанную позицию"""
        if position is None:
            position = len(self.content)
        if position < 0:
            position = 0
        if position > len(self.content):
            position = len(self.content)
        
        self.content = self.content[:position] + text + self.content[position:]
        return True
    
    def delete_text(self, start: int, end: int) -> bool:
        """Удаление текста от start до end"""
        if start < 0:
            start = 0
        if end > len(self.content):
            end = len(self.content)
        if start >= end:
            return False
        
        self.content = self.content[:start] + self.content[end:]
        return True
    
    def find_and_replace(self, search: str, replace: str) -> int:
        """Поиск и замена, возвращает количество замен"""
        count = self.content.count(search)
        self.content = self.content.replace(search, replace)
        return count
    
    def save(self) -> bool:
        """Сохранение текущего документа"""
        if self.current_file:
            return self.fs.save(self.current_file, self.content)
        return False


# ============== ЭЛЕМЕНТЫ ТЕКСТА ==============
class Word:
    """Слово"""
    def __init__(self, text: str):
        self.text = text.strip()
    
    def capitalize(self) -> 'Word':
        return Word(self.text.capitalize())
    
    def upper(self) -> 'Word':
        return Word(self.text.upper())
    
    def lower(self) -> 'Word':
        return Word(self.text.lower())
    
    def get_text(self) -> str:
        return self.text
    
    def __len__(self):
        return len(self.text)
    
    def __repr__(self):
        return f"Word('{self.text}')"


class Sentence:
    """Предложение"""
    def __init__(self, words: List[Word]):
        self.words = words
    
    @classmethod
    def from_string(cls, text: str):
        word_texts = re.findall(r"\b\w+(?:['-]\w+)?\b", text)
        words = [Word(w) for w in word_texts]
        return cls(words)
    
    def get_text(self) -> str:
        return " ".join(w.get_text() for w in self.words)
    
    def word_count(self) -> int:
        return len(self.words)
    
    def __repr__(self):
        return f"Sentence({self.words})"


class Paragraph:
    """Абзац"""
    def __init__(self, sentences: List[Sentence]):
        self.sentences = sentences
    
    @classmethod
    def from_string(cls, text: str):
        # Разбиваем на предложения по .!?
        sentence_texts = re.split(r'([.!?])\s*', text)
        sentences = []
        for i in range(0, len(sentence_texts) - 1, 2):
            sent_text = sentence_texts[i] + sentence_texts[i + 1]
            if sent_text.strip():
                sentences.append(Sentence.from_string(sent_text))
        if sentence_texts and not sentences:
            sentences.append(Sentence.from_string(sentence_texts[0]))
        return cls(sentences)
    
    def get_text(self) -> str:
        texts = [s.get_text() for s in self.sentences]
        return " ".join(texts)
    
    def sentence_count(self) -> int:
        return len(self.sentences)
    
    def __repr__(self):
        return f"Paragraph({len(self.sentences)} sentences)"


@dataclass
class Table:
    """Таблица"""
    headers: List[str]
    rows: List[List[str]]
    
    def get_column_widths(self) -> List[int]:
        """Вычисление ширины колонок"""
        widths = [len(h) for h in self.headers]
        for row in self.rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))
        return widths
    
    def render(self, cell_width: int = 15) -> str:
        """Отрисовка таблицы"""
        widths = self.get_column_widths()
        # Ограничиваем ширину
        widths = [min(w, cell_width) for w in widths]
        
        def format_row(row: List[str]) -> str:
            cells = []
            for i, cell in enumerate(row):
                if i < len(widths):
                    cells.append(str(cell)[:widths[i]].ljust(widths[i]))
            return "| " + " | ".join(cells) + " |"
        
        separator = "+-" + "-+-".join("-" * w for w in widths) + "-+"
        lines = [separator]
        lines.append(format_row(self.headers))
        lines.append(separator)
        for row in self.rows:
            lines.append(format_row(row))
        lines.append(separator)
        
        return "\n".join(lines)


# ============== КОМПОНЕНТ 3: ФОРМАТОР ==============
class Formatter:
    """Форматирование текста: заголовки, абзацы, таблицы"""
    
    def __init__(self, page_width: int = 80, page_height: int = 60):
        self.page_width = page_width
        self.page_height = page_height
    
    def split_into_words(self, text: str) -> List[Word]:
        """Разбивка текста на слова"""
        words = re.findall(r"\b\w+(?:['-]\w+)?\b", text)
        return [Word(w) for w in words]
    
    def split_into_sentences(self, text: str) -> List[Sentence]:
        """Разбивка на предложения"""
        sentence_texts = re.split(r'([.!?])\s*', text)
        sentences = []
        for i in range(0, len(sentence_texts) - 1, 2):
            sent_text = sentence_texts[i] + sentence_texts[i + 1]
            if sent_text.strip():
                sentences.append(Sentence.from_string(sent_text))
        if sentence_texts and not sentences and sentence_texts[0].strip():
            sentences.append(Sentence.from_string(sentence_texts[0]))
        return sentences
    
    def split_into_paragraphs(self, text: str) -> List[Paragraph]:
        """Разбивка на абзацы по двойным переносам строк"""
        paragraph_texts = re.split(r'\n\s*\n', text.strip())
        paragraphs = []
        for p_text in paragraph_texts:
            if p_text.strip():
                paragraphs.append(Paragraph.from_string(p_text))
        return paragraphs
    
    def wrap_line(self, words: List[Word], max_width: int) -> Tuple[List[Word], List[Word]]:
        """Перенос строки: возвращает (строка, остаток)"""
        if not words:
            return [], []
        
        line = []
        current_length = 0
        
        for i, word in enumerate(words):
            word_len = len(word.text)
            if current_length == 0:
                if word_len <= max_width:
                    line.append(word)
                    current_length = word_len
                else:
                    # Слишком длинное слово
                    line.append(word)
                    return line, words[i+1:]
            else:
                if current_length + 1 + word_len <= max_width:
                    line.append(word)
                    current_length += 1 + word_len
                else:
                    return line, words[i:]
        
        return line, []
    
    def format_paragraph(self, paragraph: Paragraph, indent: int = 0) -> str:
        """Форматирование одного абзаца"""
        text = paragraph.get_text()
        words = self.split_into_words(text)
        max_width = self.page_width - indent
        
        lines = []
        remaining = words
        
        while remaining:
            line_words, remaining = self.wrap_line(remaining, max_width)
            if line_words:
                line_text = " ".join(w.text for w in line_words)
                lines.append(" " * indent + line_text)
            else:
                break
        
        return "\n".join(lines)
    
    def format_document(self, text: str, title: Optional[str] = None) -> str:
        """Форматирование всего документа"""
        result = []
        
        if title:
            result.append("=" * self.page_width)
            result.append(title.center(self.page_width))
            result.append("=" * self.page_width)
            result.append("")
        
        paragraphs = self.split_into_paragraphs(text)
        for para in paragraphs:
            formatted = self.format_paragraph(para, indent=2)
            result.append(formatted)
            result.append("")
        
        return "\n".join(result)
    
    def format_table(self, table: Table) -> str:
        """Форматирование таблицы"""
        return table.render(cell_width=self.page_width // 4)
    
    def format_document_with_tables(self, text: str, tables: List[Table], title: Optional[str] = None) -> str:
        """Форматирование документа с таблицами"""
        result = []
        
        if title:
            result.append("=" * self.page_width)
            result.append(title.center(self.page_width))
            result.append("=" * self.page_width)
            result.append("")
        
        result.append(self.format_document(text))
        
        for i, table in enumerate(tables):
            result.append("")
            result.append(f"Таблица {i+1}:")
            result.append(self.format_table(table))
        
        return "\n".join(result)


# ============== КОМПОНЕНТ 4: НАБОРЩИК ==============
class Typesetter:
    """Преобразование форматированного текста в команды для вывода"""
    
    def __init__(self, font_size: int = 12, line_spacing: float = 1.5):
        self.font_size = font_size
        self.line_spacing = line_spacing
    
    def get_print_commands(self, formatted_text: str) -> List[str]:
        """Генерация команд для печати"""
        commands = []
        lines = formatted_text.split('\n')
        
        for line in lines:
            commands.append(f"SET_FONT_SIZE {self.font_size}")
            commands.append(f"SET_LINE_SPACING {self.line_spacing}")
            commands.append(f"PRINT '{line}'")
            commands.append("NEWLINE")
        
        commands.append("EJECT_PAGE")
        return commands
    
    def render_to_file(self, formatted_text: str, output_path: str) -> bool:
        """Сохранение в файл команд"""
        try:
            commands = self.get_print_commands(formatted_text)
            output_data = {
                "font_size": self.font_size,
                "line_spacing": self.line_spacing,
                "content": formatted_text,
                "commands": commands,
                "timestamp": datetime.now().isoformat()
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False


# ============== ПОЛНАЯ СИСТЕМА ПУБЛИКАЦИИ ==============
class PublishingSystem:
    """Объединение всех компонентов"""
    
    def __init__(self):
        self.fs = FileSystem()
        self.editor = TextEditor(self.fs)
        self.formatter = Formatter()
        self.typesetter = Typesetter()
    
    def create_publication(self, filename: str, content: str, title: Optional[str] = None) -> bool:
        """Полный цикл публикации"""
        # 1. Сохраняем через редактор
        self.editor.create_new(filename)
        self.editor.insert_text(content)
        self.editor.save()
        
        # 2. Форматируем
        formatted = self.formatter.format_document(content, title=title)
        
        # 3. Готовим к печати
        output_filename = filename.replace('.txt', '_formatted.json')
        return self.typesetter.render_to_file(formatted, output_filename)
    