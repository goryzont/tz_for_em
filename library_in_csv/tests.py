import unittest
from unittest.mock import mock_open, patch, MagicMock
import uuid
import csv
from library_in_csv.service import LibraryService


class TestLibraryService(unittest.TestCase):

    def setUp(self):
        self.test_data_file = "test_books.csv"
        self.test_books = [
            {
                "id": str(uuid.uuid4()),
                "title": "Book 1",
                "author": "Author 1",
                "year": 2000,
                "status": "в наличии",
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Book 2",
                "author": "Author 2",
                "year": 2010,
                "status": "выдана",
            },
        ]

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_books_empty(self, mock_file):
        service = LibraryService(self.test_data_file)
        self.assertEqual(service.books, [])


    @patch("builtins.open", new_callable=mock_open)
    def test_save_books(self, mock_file):
        service = LibraryService(self.test_data_file)
        service.books = self.test_books
        service.save_books()

        mock_file.assert_called_with(self.test_data_file, mode="w", encoding="utf-8", newline="")
        handle = mock_file()
        handle.write.assert_called()

    @patch("builtins.open", new_callable=mock_open)
    def test_add_book(self, mock_file):
        service = LibraryService(self.test_data_file)

        # Инициализируем книги вручную
        service.books = self.test_books
        service.save_books = MagicMock()  # Мокаем сохранение

        # Добавляем книгу
        service.add_book("New Book", "New Author", 2021)

        # Проверяем, что длина увеличилась
        self.assertEqual(len(service.books), len(self.test_books))

        # Проверяем данные новой книги
        new_book = service.books[-1]
        self.assertEqual(new_book["title"], "New Book")
        self.assertEqual(new_book["author"], "New Author")
        self.assertEqual(new_book["year"], 2021)
        self.assertEqual(new_book["status"], "в наличии")

        # Проверяем, что метод save_books был вызван
        service.save_books.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_delete_book(self, mock_file):
        service = LibraryService(self.test_data_file)
        service.books = self.test_books
        service.save_books = MagicMock()

        book_id_to_delete = self.test_books[0]["id"]
        service.delete_book(book_id_to_delete)

        self.assertEqual(len(service.books), len(self.test_books))
        self.assertNotIn(book_id_to_delete, [book["id"] for book in service.books])
        service.save_books.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_search_books(self, mock_file):
        service = LibraryService(self.test_data_file)
        service.books = self.test_books

        result = service.search_books("title", "Book 1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["author"], "Author 1")

    @patch("builtins.open", new_callable=mock_open)
    def test_update_status(self, mock_file):
        service = LibraryService(self.test_data_file)
        service.books = self.test_books
        service.save_books = MagicMock()

        book_id_to_update = self.test_books[0]["id"]
        new_status = "выдана"
        service.update_status(book_id_to_update, new_status)

        self.assertEqual(
            [book["status"] for book in service.books if book["id"] == book_id_to_update][0],
            new_status,
        )
        service.save_books.assert_called_once()


if __name__ == "__main__":
    unittest.main()
