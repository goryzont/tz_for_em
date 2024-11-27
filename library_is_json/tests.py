import unittest
from unittest.mock import patch, mock_open, MagicMock
import uuid
import json
from library_is_json.service import LibraryService


class TestLibraryService(unittest.TestCase):
    def setUp(self):
        self.test_data_file = "test_library.json"
        self.test_books = [
            {
                "id": str(uuid.uuid4()),
                "title": "Book 1",
                "author": "Author 1",
                "year": 2001,
                "status": "в наличии",
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Book 2",
                "author": "Author 2",
                "year": 2002,
                "status": "выдана",
            },
        ]

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_load_books(self, mock_exists, mock_file):
        mock_file.return_value.read.return_value = json.dumps(self.test_books)
        service = LibraryService(self.test_data_file)
        self.assertEqual(service.books, self.test_books)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_books(self, mock_file):
        service = LibraryService(self.test_data_file)
        service.books = self.test_books
        service.save_books()

        # Проверяем, что файл был открыт для записи
        mock_file.assert_called_once_with(self.test_data_file, "w", encoding="utf-8")

        # Получаем все вызовы метода write
        written_data = "".join(call.args[0] for call in mock_file().write.call_args_list)

        # Проверяем, что записанные данные соответствуют ожидаемым
        self.assertEqual(written_data, json.dumps(self.test_books, indent=4, ensure_ascii=False))

    @patch("builtins.open", new_callable=mock_open)
    def test_add_book(self, mock_file):
        service = LibraryService(self.test_data_file)
        service.books = self.test_books
        service.save_books = MagicMock()

        service.add_book("New Book", "New Author", 2023)
        self.assertEqual(len(service.books), len(self.test_books))
        new_book = service.books[-1]
        self.assertEqual(new_book["title"], "New Book")
        self.assertEqual(new_book["author"], "New Author")
        self.assertEqual(new_book["year"], 2023)
        self.assertEqual(new_book["status"], "в наличии")
        service.save_books.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_delete_book(self, mock_file):
        service = LibraryService(self.test_data_file)
        service.books = self.test_books
        service.save_books = MagicMock()

        book_id = self.test_books[0]["id"]
        service.delete_book(book_id)
        self.assertEqual(len(service.books), len(self.test_books))
        self.assertNotIn(book_id, [book["id"] for book in service.books])
        service.save_books.assert_called_once()

    def test_search_books(self):
        service = LibraryService(self.test_data_file)
        service.books = self.test_books

        result = service.search_books("title", "Book 1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["author"], "Author 1")

        result = service.search_books("year", "2002")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Book 2")

    @patch("builtins.print")
    def test_display_books(self, mock_print):
        service = LibraryService(self.test_data_file)
        service.books = self.test_books

        service.display_books()
        self.assertEqual(mock_print.call_count, len(self.test_books) + 1)  # +1 для заголовка

    @patch("builtins.open", new_callable=mock_open)
    def test_update_status(self, mock_file):
        service = LibraryService(self.test_data_file)
        service.books = self.test_books
        service.save_books = MagicMock()

        book_id = self.test_books[0]["id"]
        service.update_status(book_id, "выдана")
        self.assertEqual(service.books[0]["status"], "выдана")
        service.save_books.assert_called_once()


if __name__ == "__main__":
    unittest.main()
