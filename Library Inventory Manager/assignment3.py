"""
Library Inventory Manager - Single File Version
Assignment 3
Object-Oriented Programming + JSON Persistence + CLI + Exception Handling
"""

import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
import datetime
import sys

# ---------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Book Class
# ---------------------------------------------------------
@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"
    issued_to: str = ""
    issued_on: str = ""

    def __str__(self):
        info = f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {self.status}"
        if self.status == "issued":
            info += f" | Issued to: {self.issued_to} on {self.issued_on}"
        return info

    def to_dict(self):
        return asdict(self)

    def is_available(self):
        return self.status == "available"

    def issue(self, user_name: str):
        if not self.is_available():
            raise Exception(f"Book already issued to {self.issued_to}.")
        self.status = "issued"
        self.issued_to = user_name
        self.issued_on = datetime.datetime.now().isoformat(timespec="seconds")

    def return_book(self):
        if self.is_available():
            raise Exception("Book is already available.")
        self.status = "available"
        self.issued_to = ""
        self.issued_on = ""


# ---------------------------------------------------------
# Library Inventory Class
# ---------------------------------------------------------
class LibraryInventory:
    def __init__(self, storage_path="catalog.json"):
        self.storage_path = Path(storage_path)
        self.books = []
        self._ensure_storage()
        self.load_from_file()

    def _ensure_storage(self):
        """Ensure the JSON file exists."""
        if not self.storage_path.exists():
            self.save_to_file()

    def add_book(self, book: Book):
        """Add a new book if ISBN not duplicate."""
        if any(b.isbn == book.isbn for b in self.books):
            raise ValueError("ISBN already exists in catalog.")
        self.books.append(book)
        self.save_to_file()
        logger.info(f"Book added: {book.title}")

    def search_by_title(self, text):
        q = text.lower()
        return [b for b in self.books if q in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return list(self.books)

    def issue_book(self, isbn, user_name):
        book = self.search_by_isbn(isbn)
        if not book:
            raise FileNotFoundError("Book with that ISBN not found.")
        book.issue(user_name)
        self.save_to_file()

    def return_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if not book:
            raise FileNotFoundError("Book not found.")
        book.return_book()
        self.save_to_file()

    def save_to_file(self):
        """Save all books to JSON."""
        try:
            with self.storage_path.open("w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=2)
        except Exception as e:
            logger.error("Failed to save: %s", e)

    def load_from_file(self):
        """Load catalog from JSON."""
        try:
            if not self.storage_path.exists():
                self.books = []
                return
            with self.storage_path.open("r") as f:
                data = json.load(f)
            self.books = [Book(**item) for item in data]
        except json.JSONDecodeError:
            logger.error("JSON corrupt. Starting empty catalog.")
            self.books = []
        except Exception:
            logger.exception("Unexpected error loading file.")
            self.books = []


# ---------------------------------------------------------
# CLI Menu
# ---------------------------------------------------------
inventory = LibraryInventory()

def menu():
    print("\n========== Library Inventory Manager ==========")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search by Title")
    print("6. Search by ISBN")
    print("7. Exit")
    return input("Enter choice (1-7): ")

def add_book_flow():
    t = input("Title: ").strip()
    a = input("Author: ").strip()
    i = input("ISBN: ").strip()
    if not t or not i:
        print("Title and ISBN required!")
        return
    try:
        inventory.add_book(Book(title=t, author=a, isbn=i))
        print("Book added.")
    except Exception as e:
        print("Error:", e)

def issue_flow():
    isbn = input("ISBN: ").strip()
    user = input("Issue to: ").strip()
    try:
        inventory.issue_book(isbn, user)
        print("Book issued.")
    except Exception as e:
        print("Error:", e)

def return_flow():
    isbn = input("ISBN: ").strip()
    try:
        inventory.return_book(isbn)
        print("Book returned.")
    except Exception as e:
        print("Error:", e)

def view_books():
    books = inventory.display_all()
    if not books:
        print("No books in catalog.")
        return
    for b in books:
        print(b)

def search_title():
    text = input("Title contains: ").strip()
    res = inventory.search_by_title(text)
    if not res:
        print("No results.")
        return
    for b in res:
        print(b)

def search_isbn():
    isbn = input("ISBN: ").strip()
    b = inventory.search_by_isbn(isbn)
    if not b:
        print("Not found.")
        return
    print(b)

def main():
    while True:
        choice = menu()
        if choice == "1":
            add_book_flow()
        elif choice == "2":
            issue_flow()
        elif choice == "3":
            return_flow()
        elif choice == "4":
            view_books()
        elif choice == "5":
            search_title()
        elif choice == "6":
            search_isbn()
        elif choice == "7":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
