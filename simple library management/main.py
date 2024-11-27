class Library:
    def __init__(self):
        self.books = {"Python 101": 3, "Data Science Handbook": 2, "Machine Learning Basics": 1}

    def list_books(self):
        print("Available books:")
        for book, count in self.books.items():
            if count > 0:
                print(f"{book} - {count} copies")

    def borrow_book(self, book_name):
        if self.books.get(book_name, 0) > 0:
            self.books[book_name] -= 1
            print(f"You borrowed '{book_name}'.")
        else:
            print(f"Sorry, '{book_name}' is not available.")

    def return_book(self, book_name):
        if book_name in self.books:
            self.books[book_name] += 1
            print(f"You returned '{book_name}'.")
        else:
            print(f"'{book_name}' is not recognized by the library.")

def main():
    library = Library()

    while True:
        print("\nMenu:")
        print("1. List Books")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            library.list_books()
        elif choice == "2":
            book_name = input("Enter the book name to borrow: ")
            library.borrow_book(book_name)
        elif choice == "3":
            book_name = input("Enter the book name to return: ")
            library.return_book(book_name)
        elif choice == "4":
            print("Exiting the library system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
