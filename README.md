# Библиотека с хранением в CSV или JSON

## Описание
Реализовано два приложения для управления библиотекой книг с различными способами хранения данных:
- **Библиотека, хранящая данные в CSV-файле.**
- **Библиотека, хранящая данные в JSON-файле.**

### Общая структура проекта
Обе библиотеки имеют одинаковую структуру, различия касаются только работы с форматом файла.

- **`main.py`**: Основной файл, где запускается приложение.
- **`service.py`**: Файл с логикой работы приложения.
- **`tests.py`**: Файл с тестами.

---

## Основные функции (`service.py`)

### 1. **Добавление книги: `add_book(title, author, year)`**
   - Добавляет книгу в библиотеку.
   - Для генерации уникального идентификатора (ID) используется встроенная библиотека `uuid`.
   - Для проверки корректности ID реализована функция **`is_valid_uuid`**, которая находится в `main.py`.




### 2. **Удаление книги: `delete_book(book_id)`**
   - Удаляет книгу из библиотеки по-указанному ID.




### 3. **Поиск книги: `search_books(field, value)`**
   - Выполняет поиск книги в библиотеке.
   - Параметры:
     - **`field`**: Поле, по которому осуществляется поиск (`title`, `author`, `year`).
     - **`value`**: Значение, которое нужно найти.




### 4. **Отображение всех книг: `display_books()`**
   - Отображает список всех книг, которые хранятся в библиотеке.




### 5. **Обновление статуса книги: `update_status(book_id, status)`**
   - Изменяет статус книги на основе указанного ID.
   - Возможные статусы:
     - **`в наличии`**
     - **`выдана`**

---

## Тесты (`tests.py`)
Тесты реализованы с использованием библиотеки `unittest`. Они проверяют основные функции обеих библиотек для обеспечения корректности их работы.

---

## Примечания
- Генерация ID с использованием библиотеки **`uuid`** гарантирует уникальность.
- Разные форматы хранения (CSV и JSON) обеспечивают гибкость выбора, подходящую под различные требования.

---

## Как использовать
1. Укажите формат хранения библиотеки (CSV или JSON).
2. Запустите приложение через `main.py`.
3. Используйте команды для управления книгами:
   - Добавление, удаление, поиск, отображение и обновление статуса.
