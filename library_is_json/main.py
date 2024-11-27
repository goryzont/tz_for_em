import re

from service import LibraryService

# Проверяет, соответствует ли строка формату UUID
def is_valid_uuid(book_id: str) -> bool:
    pattern = r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    return bool(re.match(pattern, book_id))

def is_empty_library(library: list[dict[str: int | str]]) -> bool:
    if len(library) == 0:
        return False
    return True

def main() -> None:
    library = LibraryService()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книги")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выход")
        choice = input("Выберите действие: ")

        match choice:
            case "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания книги: "))
                library.add_book(title, author, year)

            case "2":
                if not is_empty_library(library.books):
                    print('Библиотека пуста, вам нечего удалять')
                    continue
                book_id = input("Введите id книги для удаления: ")
                if is_valid_uuid(book_id) is False:
                    print('id должен иметь формат:')
                    print('*' * 8, '-', '*' * 4, '-', '*' * 4, '-', '*' * 4, '-', '*' * 12, sep='')
                    continue
                library.delete_book(book_id)

            case "3":
                if not is_empty_library(library.books):
                    print('Библиотека пуста, вам нечего искать')
                    continue
                field = input("Введите поле для поиска (title, author, year): ")
                value = input("Введите значение для поиска: ")
                if field not in {"title", "author", "year"}:
                    print("Ошибка: допустимые поля для поиска - title, author, year.")
                    continue
                results = library.search_books(field, value)
                if results:
                    print("Результаты поиска:")
                    for book in results:
                        print(
                            f"ID: {book['id']}, Название: {book['title']}, "
                            f"Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}"
                        )
                else:
                    print("Книги по заданному запросу не найдены.")

            case "4":
                library.display_books()

            case "5":
                if not is_empty_library(library.books):
                    print('Библиотека пуста, вам нечего изменять')
                    continue
                book_id = input("Введите id книги: ")
                if is_valid_uuid(book_id) is False:
                    print('id должен иметь формат:')
                    print('*' * 8, '-', '*' * 4, '-', '*' * 4, '-', '*' * 4, '-', '*' * 12, sep='')
                    continue
                status = input("Введите новый статус (в наличии/выдана): ")
                if status not in {"в наличии", "выдана"}:
                    print("Ошибка: допустимые статусы - 'в наличии', 'выдана'.")
                    continue
                library.update_status(book_id, status)

            case "0":
                print("Выход из программы.")
                break

            case _:
                print("Ошибка: некорректный выбор.")

if __name__ == "__main__":
    main()
