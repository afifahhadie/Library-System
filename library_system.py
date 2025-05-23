import json
import datetime
from typing import Dict, List, Optional

class Book:
    def __init__(self, book_id: str, title: str, author: str, year: int, stock: int = 1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.stock = stock
        self.available = stock
    
    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'stock': self.stock,
            'available': self.available
        }
    
    @classmethod
    def from_dict(cls, data):
        book = cls(data['book_id'], data['title'], data['author'], 
                   data['year'], data['stock'])
        book.available = data['available']
        return book

class Member:
    def __init__(self, member_id: str, name: str, address: str, phone: str):
        self.member_id = member_id
        self.name = name
        self.address = address
        self.phone = phone
        self.borrowed_books = []
    
    def to_dict(self):
        return {
            'member_id': self.member_id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'borrowed_books': self.borrowed_books
        }
    
    @classmethod
    def from_dict(cls, data):
        member = cls(data['member_id'], data['name'], 
                      data['address'], data['phone'])
        member.borrowed_books = data.get('borrowed_books', [])
        return member

class Loan:
    def __init__(self, loan_id: str, member_id: str, book_id: str, 
                 loan_date: str, return_date: str = None):
        self.loan_id = loan_id
        self.member_id = member_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.status = "borrowed" if return_date is None else "returned"
    
    def to_dict(self):
        return {
            'loan_id': self.loan_id,
            'member_id': self.member_id,
            'book_id': self.book_id,
            'loan_date': self.loan_date,
            'return_date': self.return_date,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['loan_id'], data['member_id'], data['book_id'],
                   data['loan_date'], data.get('return_date'))

class LibrarySystem:
    def __init__(self):
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.loans: Dict[str, Loan] = {}
        self.loan_counter = 1
        
    def add_book(self, book_id: str, title: str, author: str, 
                    year: int, stock: int = 1) -> bool:
        """Add new book to library"""
        if book_id in self.books:
            print(f"Book with ID {book_id} already exists!")
            return False
        
        self.books[book_id] = Book(book_id, title, author, year, stock)
        print(f"Book '{title}' successfully added!")
        return True
    
    def add_member(self, member_id: str, name: str, address: str, phone: str) -> bool:
        """Add new member"""
        if member_id in self.members:
            print(f"Member with ID {member_id} already exists!")
            return False
        
        self.members[member_id] = Member(member_id, name, address, phone)
        print(f"Member '{name}' successfully added!")
        return True
    
    def borrow_book(self, member_id: str, book_id: str) -> bool:
        """Borrow book"""
        if member_id not in self.members:
            print("Member not found!")
            return False
        
        if book_id not in self.books:
            print("Book not found!")
            return False
        
        book = self.books[book_id]
        member = self.members[member_id]
        
        if book.available <= 0:
            print("Book not available!")
            return False
        
        if len(member.borrowed_books) >= 3:
            print("Member has already borrowed maximum 3 books!")
            return False
        
        # Check if member already borrowed the same book
        if book_id in member.borrowed_books:
            print("Member has already borrowed this book!")
            return False
        
        # Process loan
        loan_id = f"L{self.loan_counter:04d}"
        loan_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        loan = Loan(loan_id, member_id, book_id, loan_date)
        self.loans[loan_id] = loan
        
        book.available -= 1
        member.borrowed_books.append(book_id)
        self.loan_counter += 1
        
        print(f"Loan successful! ID: {loan_id}")
        return True
    
    def return_book(self, member_id: str, book_id: str) -> bool:
        """Return book"""
        if member_id not in self.members:
            print("Member not found!")
            return False
        
        member = self.members[member_id]
        
        if book_id not in member.borrowed_books:
            print("Member has not borrowed this book!")
            return False
        
        # Find active loan
        active_loan = None
        for loan in self.loans.values():
            if (loan.member_id == member_id and loan.book_id == book_id and 
                loan.status == "borrowed"):
                active_loan = loan
                break
        
        if active_loan:
            active_loan.return_date = datetime.datetime.now().strftime("%Y-%m-%d")
            active_loan.status = "returned"
            
            self.books[book_id].available += 1
            member.borrowed_books.remove(book_id)
            
            print("Book successfully returned!")
            return True
        
        print("Loan not found!")
        return False
    
    def search_books(self, keyword: str) -> List[Book]:
        """Search books by title or author"""
        results = []
        keyword = keyword.lower()
        
        for book in self.books.values():
            if (keyword in book.title.lower() or 
                keyword in book.author.lower()):
                results.append(book)
        
        return results
    
    def display_all_books(self):
        """Display all books"""
        if not self.books:
            print("No books in the library.")
            return
        
        print("\n=== BOOK LIST ===")
        print(f"{'ID':<8} {'Title':<30} {'Author':<20} {'Year':<6} {'Stock':<5} {'Available':<9}")
        print("-" * 85)
        
        for book in self.books.values():
            print(f"{book.book_id:<8} {book.title:<30} {book.author:<20} "
                  f"{book.year:<6} {book.stock:<5} {book.available:<9}")
    
    def display_all_members(self):
        """Display all members"""
        if not self.members:
            print("No registered members.")
            return
        
        print("\n=== MEMBER LIST ===")
        print(f"{'ID':<8} {'Name':<25} {'Address':<30} {'Phone':<15} {'Books Borrowed':<5}")
        print("-" * 90)
        
        for member in self.members.values():
            borrowed_count = len(member.borrowed_books)
            print(f"{member.member_id:<8} {member.name:<25} {member.address:<30} "
                  f"{member.phone:<15} {borrowed_count:<5}")
    
    def display_loan_history(self):
        """Display loan history"""
        if not self.loans:
            print("No loan history.")
            return
        
        print("\n=== LOAN HISTORY ===")
        print(f"{'ID':<8} {'Member':<10} {'Book':<10} {'Loan Date':<12} {'Return Date':<12} {'Status':<12}")
        print("-" * 75)
        
        for loan in self.loans.values():
            return_date = loan.return_date if loan.return_date else "-"
            print(f"{loan.loan_id:<8} {loan.member_id:<10} {loan.book_id:<10} "
                  f"{loan.loan_date:<12} {return_date:<12} {loan.status:<12}")
    
    def save_data(self, filename: str = "library.json"):
        """Save data to JSON file"""
        data = {
            'books': {k: v.to_dict() for k, v in self.books.items()},
            'members': {k: v.to_dict() for k, v in self.members.items()},
            'loans': {k: v.to_dict() for k, v in self.loans.items()},
            'loan_counter': self.loan_counter
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data successfully saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self, filename: str = "library.json"):
        """Load data from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.books = {k: Book.from_dict(v) for k, v in data.get('books', {}).items()}
            self.members = {k: Member.from_dict(v) for k, v in data.get('members', {}).items()}
            self.loans = {k: Loan.from_dict(v) for k, v in data.get('loans', {}).items()}
            self.loan_counter = data.get('loan_counter', 1)
            
            print(f"Data successfully loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with empty data.")
        except Exception as e:
            print(f"Error loading data: {e}")

def main_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("         LIBRARY SYSTEM")
    print("="*50)
    print("1. Manage Books")
    print("2. Manage Members")
    print("3. Borrowing & Returning")
    print("4. Reports")
    print("5. Save Data")
    print("6. Load Data")
    print("0. Exit")
    print("="*50)

def book_menu():
    """Book management menu"""
    print("\n=== MANAGE BOOKS ===")
    print("1. Add Book")
    print("2. Display All Books")
    print("3. Search Books")
    print("0. Back")

def member_menu():
    """Member management menu"""
    print("\n=== MANAGE MEMBERS ===")
    print("1. Add Member")
    print("2. Display All Members")
    print("0. Back")

def loan_menu():
    """Loan menu"""
    print("\n=== BORROWING & RETURNING ===")
    print("1. Borrow Book")
    print("2. Return Book")
    print("0. Back")

def report_menu():
    """Report menu"""
    print("\n=== REPORTS ===")
    print("1. Book List")
    print("2. Member List")
    print("3. Loan History")
    print("0. Back")

def main():
    """Main program function"""
    system = LibrarySystem()
    
    # Sample data
    system.add_book("B001", "Python Programming", "John Smith", 2023, 3)
    system.add_book("B002", "Data Science Handbook", "Jane Doe", 2022, 2)
    system.add_book("B003", "Machine Learning Basics", "Bob Johnson", 2024, 1)
    
    system.add_member("M001", "Ahmad Rizki", "123 Main Street", "081234567890")
    system.add_member("M002", "Siti Nurhaliza", "456 Oak Avenue", "081298765432")
    
    while True:
        main_menu()
        choice = input("Choose menu (0-6): ").strip()
        
        if choice == "1":  # Manage Books
            while True:
                book_menu()
                sub_choice = input("Choose menu (0-3): ").strip()
                
                if sub_choice == "1":  # Add Book
                    book_id = input("Book ID: ").strip()
                    title = input("Title: ").strip()
                    author = input("Author: ").strip()
                    try:
                        year = int(input("Publication Year: "))
                        stock = int(input("Stock (default 1): ") or "1")
                        system.add_book(book_id, title, author, year, stock)
                    except ValueError:
                        print("Year and stock input must be numbers!")
                
                elif sub_choice == "2":  # Display All Books
                    system.display_all_books()
                
                elif sub_choice == "3":  # Search Books
                    keyword = input("Enter keyword (title/author): ").strip()
                    results = system.search_books(keyword)
                    if results:
                        print(f"\nFound {len(results)} books:")
                        for book in results:
                            print(f"- {book.title} by {book.author} ({book.year})")
                    else:
                        print("Books not found.")
                
                elif sub_choice == "0":  # Back
                    break
                
                else:
                    print("Invalid choice!")
        
        elif choice == "2":  # Manage Members
            while True:
                member_menu()
                sub_choice = input("Choose menu (0-2): ").strip()
                
                if sub_choice == "1":  # Add Member
                    member_id = input("Member ID: ").strip()
                    name = input("Name: ").strip()
                    address = input("Address: ").strip()
                    phone = input("Phone: ").strip()
                    system.add_member(member_id, name, address, phone)
                
                elif sub_choice == "2":  # Display All Members
                    system.display_all_members()
                
                elif sub_choice == "0":  # Back
                    break
                
                else:
                    print("Invalid choice!")
        
        elif choice == "3":  # Borrowing & Returning
            while True:
                loan_menu()
                sub_choice = input("Choose menu (0-2): ").strip()
                
                if sub_choice == "1":  # Borrow Book
                    member_id = input("Member ID: ").strip()
                    book_id = input("Book ID: ").strip()
                    system.borrow_book(member_id, book_id)
                
                elif sub_choice == "2":  # Return Book
                    member_id = input("Member ID: ").strip()
                    book_id = input("Book ID: ").strip()
                    system.return_book(member_id, book_id)
                
                elif sub_choice == "0":  # Back
                    break
                
                else:
                    print("Invalid choice!")
        
        elif choice == "4":  # Reports
            while True:
                report_menu()
                sub_choice = input("Choose menu (0-3): ").strip()
                
                if sub_choice == "1":  # Book List
                    system.display_all_books()
                
                elif sub_choice == "2":  # Member List
                    system.display_all_members()
                
                elif sub_choice == "3":  # Loan History
                    system.display_loan_history()
                
                elif sub_choice == "0":  # Back
                    break
                
                else:
                    print("Invalid choice!")
        
        elif choice == "5":  # Save Data
            filename = input("File name (default: library.json): ").strip()
            if not filename:
                filename = "library.json"
            system.save_data(filename)
        
        elif choice == "6":  # Load Data
            filename = input("File name (default: library.json): ").strip()
            if not filename:
                filename = "library.json"
            system.load_data(filename)
        
        elif choice == "0":  # Exit
            print("Thank you for using the Library System!")
            break
        
        else:
            print("Invalid choice!")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()