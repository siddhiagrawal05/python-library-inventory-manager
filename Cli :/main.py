import logging
from library_manager.book import Book
from library_manager.inventory import LibraryInventory

logging.basicConfig(filename="library.log", level=logging.INFO)

def menu():
    print("\n1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")
    return input("Enter choice: ")

def main():
    inventory = LibraryInventory()

    while True:
        choice = menu()

        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")
            inventory.add_book(Book(title, author, isbn))
            inventory.save_books()

        elif choice == "2":
            isbn = input("ISBN: ")
            book = inventory.search_by_isbn(isbn)
            if book and book.issue():
                inventory.save_books()

        elif choice == "3":
            isbn = input("ISBN: ")
            book = inventory.search_by_isbn(isbn)
            if book and book.return_book():
                inventory.save_books()

        elif choice == "4":
            inventory.display_all()

        elif choice == "5":
            query = input("Search: ")
            book = inventory.search_by_isbn(query)
            if book:
                print(book)
            else:
                results = inventory.search_by_title(query)
                for item in results:
                    print(item)

        elif choice == "6":
            break

if __name__ == "__main__":
    main()
