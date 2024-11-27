import uuid
import csv


DATA_FILE = 'library.csv'


class LibraryService:
    # Класс для управления библиотекой книг с использованием CSV.

    def __init__(self, data_file: str = DATA_FILE) -> None:
        self.data_file = data_file
        self.books = self.load_books()

    def load_books(self) -> list[dict]:
        # Загрузка данных из CSV.
        books = []
        try:
            with open(self.data_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    books.append(row)
        except FileNotFoundError:
            pass  # Если файл не найден, возвращаем пустой список
        return books

    def save_books(self) -> None:
        # Сохранение данных в CSV
        with open(self.data_file, mode="w", encoding="utf-8", newline="") as file:
            fieldnames = ["id", "title", "author", "year", "status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.books)

    def add_book(self, title: str, author: str, year: int) -> None:
        # Добавление книги
        new_book = {
            "id": str(uuid.uuid4()),  # Генерация уникального ID
            "title": title,
            "author": author,
            "year": int(year),
            "status": "в наличии",
        }
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' успешно добавлена.")

    def delete_book(self, book_id: str) -> None:
        # Удаление книги по ID.
        for book in self.books:
            if book["id"] == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с id {book_id} успешно удалена.")
                return
        print(f"Книга с id {book_id} не найдена.")

    def search_books(self, field: str, value: str) -> list[dict]:
        # Поиск книг по полю
        return [book for book in self.books if book[field].lower() == value.lower()]

    def display_books(self) -> None:
        # Отображение всех книг
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