import json
import os
import uuid
from typing import List, Dict, Union


# Тип данных для книги
Book = Dict[str, Union[int, str]]

DATA_FILE = "library.json"


class LibraryService:
    # Класс для управления библиотекой книг.

    def __init__(self, data_file: str = DATA_FILE) -> None:
        self.data_file = data_file
        self.books: List[Book] = self.load_books()

    def load_books(self) -> List[Book]:
        # загрузка книг из файла JSON
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_books(self) -> None:
        # Сохранение книг в файл JSON
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(self.books, file, indent=4, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: int) -> None:
         # Добавление новой книги в библиотеку
        new_book = {
            "id": str(uuid.uuid4()),
            "title": title,
            "author": author,
            "year": year,
            "status": "в наличии",
        }
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' успешно добавлена.")

    def delete_book(self, book_id: str ) -> None: #добавить проверку uuid
        # Удаление книги по её id.
        for book in self.books:
            if book_id == book['id']:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с id {book_id} успешно удалена.")
                return
        print(f"Книга с id {book_id} не найдена.")

    def search_books(self, field: str, value: str) -> List[Book]:
        # Поиск книг по заданному полю
        return [book for book in self.books if str(book[field]).lower() == value.lower()]

    def display_books(self) -> None:
        # Отображение всех книг в библиотеке.
        if not self.books:
            print("Библиотека пуста.")
            return
        print("Список книг:")
        for book in self.books:
            print(
                f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                f"Год: {book['year']}, Статус: {book['status']}"
            )

    def update_status(self, book_id: str, status: str) -> None:
        # Изменение статуса книги
        for book in self.books:
            if book["id"] == book_id:
                book["status"] = status
                self.save_books()
                print(f"Статус книги с id {book_id} обновлён на '{status}'.")
                return
        print(f"Книга с id {book_id} не найдена.")
