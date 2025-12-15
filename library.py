# -------------------------------------------------
# DIGITAL LIBRARY INVENTORY SYSTEM - MINI PROJECT
# Name: Siddhi Agrawal
# Course: B.Tech Computer Science
# Title: Digital Library Inventory System
# -------------------------------------------------

import json
import logging
from pathlib import Path

# -------------------------------------------------
# Logging Configuration
# -------------------------------------------------
logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------------------------
# MODULE 1: BOOK CLASS
# -------------------------------------------------
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} | {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "issued":
            return False
        self.status = "issued"
        return True

    def return_book(self):
        if self.status == "available":
            return False
        self.status = "available"
        return True

    def is_available(self):
        return self.status == "available"


# -------------------------------------------------
# MODULE 2: LIBRARY INVENTORY MANAGER
# -------------------------------------------------
class LibraryInventory:
    def __init__(self):
        # Absolute path ensures correct execution everywhere
        self.file_path = Path(__file__).resolve().parent / "library_books.json"
        self.books = []
        self.load_books()

    def add_book(self, book: Book):
        self.books.append(book)
        logging.info(f"Book added: {book.title}")

    def search_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def search_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all(self):
        if not self.books:
            print("No books available in the inventory.")
            return

        print("\n------ LIBRARY BOOK LIST ------")
        for book in self.books:
            print(book)

    def save_books(self):
        try:
            with open(self.file_path, "w") as file:
                json.dump([book.to_dict() for book in self.books], file, indent=4)
        except Exception as error:
            logging.error("Error saving data: " + str(error))

    def load_books(self):
        try:
            if not self.file_path.exists():
                self.save_books()
                return

            with open(self.file_path, "r") as file:
                data = json.load(file)
                for item in data:
                    self.books.append(
                        Book(
                            item["title"],
                            item["author"],
                            item["isbn"],
                            item["status"]
                        )
                    )
        except json.JSONDecodeError:
            logging.error("JSON file corrupted. Resetting file.")
            self.save_books()
        except Exception as error:
            logging.error("Error loading data: " + str(error))


# -------------------------------------------------
# MODULE 3: MENU-DRIVEN INTERFACE
# -------------------------------------------------
def menu():
    print("\n========== DIGITAL LIBRARY SYSTEM ==========")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")
    return input("Enter your choice: ")


def main():
    inventory = LibraryInventory()

    while True:
        choice = menu()

        if choice == "1":
            title = input("Enter Book Title: ")
            author = input("Enter Author: ")
            isbn = input("Enter ISBN: ")

            inventory.add_book(Book(title, author, isbn))
            inventory.save_books()
            print("Book Added Successfully!")

        elif choice == "2":
            isbn = input("Enter ISBN to issue: ")
            book = inventory.search_by_isbn(isbn)

            if book and book.issue():
                inventory.save_books()
                print("Book Issued Successfully!")
            else:
                print("Cannot issue book.")

        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            book = inventory.search_by_isbn(isbn)

            if book and book.return_book():
                inventory.save_books()
                print("Book Returned Successfully!")
            else:
                print("Cannot return book.")

        elif choice == "4":
            inventory.display_all()

        elif choice == "5":
            query = input("Enter Title or ISBN: ")

            book = inventory.search_by_isbn(query)
            if book:
                print(book)
            else:
                results = inventory.search_by_title(query)
                if results:
                    for item in results:
                        print(item)
                else:
                    print("No matching book found.")

        elif choice == "6":
            print("Thank you for using the Library System.")
            break

        else:
            print("Invalid choice! Please try again.")


# -------------------------------------------------
# PROGRAM ENTRY POINT
# -------------------------------------------------
if __name__ == "__main__":
    main()

