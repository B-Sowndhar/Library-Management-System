# This is a oops based library management system
from datetime import datetime, timedelta

class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = False

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"[{self.book_id}] {self.title} by {self.author} - {status}"


class Person:
    def __init__(self, name):
        self.name = name


class Member(Person):
    def __init__(self, name):
        super().__init__(name)
        self.borrowed_books = []

    def borrow_book(self, library, book_id):
       book = library.get_book_by_id(book_id)
       if book and not book.is_borrowed:
        book.is_borrowed = True
        due_date = datetime.now() + timedelta(days=7)
        self.borrowed_books.append((book, due_date))
        print("\n", self.name, "successfully borrowed", book.title)
        print("Due date:", due_date.strftime("%Y-%m-%d"))
       elif book:
        print("\nSorry,", book.title, "is currently borrowed.")
       else:
         print("\nBook ID not found!")


    def return_book(self, library, book_id):
      for book_tuple in self.borrowed_books:
           book, due_date = book_tuple
           if book.book_id == book_id:
              book.is_borrowed = False
              self.borrowed_books.remove(book_tuple)
              print("\n", self.name, "returned", book.title)
              print("Was due on:", due_date.strftime("%Y-%m-%d"))
              return
      print("\nYou have not borrowed this book.")


class Librarian(Person):
    def __init__(self, name):
        super().__init__(name)

    def add_book(self, library, book_id, title, author):
        new_book = Book(book_id, title, author)
        library.books.append(new_book)
        print("\nBook", title, "added to library.")

    def remove_book(self, library, book_id):
        for book in library.books:
            if book.book_id == book_id:
                library.books.remove(book)
                print("\nBook", book.title, "removed from library.")
                return
        print("\nBook ID not found!")


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def get_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def display_books(self):
        if not self.books:
            print("\nNo books in the library.")
            return
        print("\nBooks in Library:")
        for book in self.books:
            print(book)

    def display_members(self):
        if not self.members:
            print("\nNo registered members.")
            return
        print("\nLibrary Members:")
        for member in self.members:
            print("-", member.name)

def librarian_login():
    username = input("Enter librarian username: ")
    password = input("Enter librarian password: ")
    if username == "library1" and password == "lib123":
        print("Librarian login successful.")
        return True
    else:
        print("Invalid credentials.")
        return False

def main():
    library = Library()
    librarian = Librarian("Admin")

    # Pre-added books
    librarian.add_book(library, 1, "Python Programming", "John Doe")
    librarian.add_book(library, 2, "OOP Concepts", "Jane Smith")
    librarian.add_book(library, 3, "Data Structures", "Brian Cox")

    while True:
        print("\n--- Library Menu ---")
        print("1. Register Member")
        print("2. View All Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Add Book (Librarian)")
        print("6. Remove Book (Librarian)")
        print("7. View Members")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            name = input("Enter member name: ")
            member = Member(name)
            library.members.append(member)
            print(name, "registered as a member.")

        elif choice == '2':
            library.display_books()

        elif choice == '3':
            if not library.members:
                print("No members found. Please register first.")
                continue
            name = input("Enter your name: ")
            member = next((m for m in library.members if m.name == name), None)
            if not member:
                print("Member not found.")
                continue
            book_id = int(input("Enter book ID to borrow: "))
            member.borrow_book(library, book_id)

        elif choice == '4':
            name = input("Enter your name: ")
            member = next((m for m in library.members if m.name == name), None)
            if not member:
                print("Member not found.")
                continue
            book_id = int(input("Enter book ID to return: "))
            member.return_book(library, book_id)


        elif choice == '5':
          if librarian_login():
            book_id = int(input("Enter new book ID: "))
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            librarian.add_book(library, book_id, title, author)

        elif choice == '6':
          if librarian_login():
             book_id = int(input("Enter book ID to remove: "))
             librarian.remove_book(library, book_id)


        elif choice == '7':
            library.display_members()

        elif choice == '8':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


main()
