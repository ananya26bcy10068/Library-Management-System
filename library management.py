import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta


# ============================================================
# CONSTANTS
# ============================================================

LOAN_DAYS = 14
FINE_PER_DAY = 5
FONT = ("Times New Roman", 12)
DB_NAME = "library.db"


# ============================================================
# DATABASE SETUP
# ============================================================

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            copies INTEGER NOT NULL,
            available INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            due_date TEXT,
            returned INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# CLI INTERFACE
# ============================================================

class LibraryCLI:

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

    # --------------------------------------------------------
    # ADD BOOK
    # --------------------------------------------------------

    def add_book(self):
        print("\n========== ADD BOOK ==========")

        title = input("Enter book title: ").strip()

        if not title:
            print("Book title cannot be empty.")
            return

        copies_text = input("Enter number of copies: ").strip()

        try:
            copies = int(copies_text)

            if copies <= 0:
                print("Number of copies must be greater than 0.")
                return

        except ValueError:
            print("Please enter a valid whole number.")
            return

        self.cursor.execute(
            """
            INSERT INTO books (title, copies, available)
            VALUES (?, ?, ?)
            """,
            (title, copies, copies)
        )

        self.conn.commit()

        print("Book added successfully.")

    # --------------------------------------------------------
    # VIEW BOOKS
    # --------------------------------------------------------

    def view_books(self):
        print("\n========== BOOKS ==========")

        self.cursor.execute("""
            SELECT id, title, copies, available
            FROM books
            ORDER BY id
        """)

        books = self.cursor.fetchall()

        if not books:
            print("No books found.")
            return

        print("\nID   Book Title                    Available")
        print("-" * 55)

        for book_id, title, copies, available in books:
            print(
                f"{book_id:<4} "
                f"{title:<30} "
                f"{available}/{copies}"
            )

    # --------------------------------------------------------
    # DELETE BOOK
    # --------------------------------------------------------

    def delete_book(self):
        print("\n========== DELETE BOOK ==========")

        self.view_books()

        try:
            book_id = int(input("\nEnter Book ID to delete: "))
        except ValueError:
            print("Invalid Book ID.")
            return

        self.cursor.execute(
            "SELECT id FROM books WHERE id = ?",
            (book_id,)
        )

        if self.cursor.fetchone() is None:
            print("Book not found.")
            return

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM loans
            WHERE book_id = ? AND returned = 0
            """,
            (book_id,)
        )

        if self.cursor.fetchone()[0] > 0:
            print("Cannot delete this book because it is currently on loan.")
            return

        self.cursor.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,)
        )

        self.conn.commit()

        print("Book deleted successfully.")

    # --------------------------------------------------------
    # ADD MEMBER
    # --------------------------------------------------------

    def add_member(self):
        print("\n========== ADD MEMBER ==========")

        name = input("Enter member name: ").strip()

        if not name:
            print("Member name cannot be empty.")
            return

        self.cursor.execute(
            "INSERT INTO members (name) VALUES (?)",
            (name,)
        )

        self.conn.commit()

        print("Member added successfully.")

    # --------------------------------------------------------
    # VIEW MEMBERS
    # --------------------------------------------------------

    def view_members(self):
        print("\n========== MEMBERS ==========")

        self.cursor.execute("""
            SELECT id, name
            FROM members
            ORDER BY id
        """)

        members = self.cursor.fetchall()

        if not members:
            print("No members found.")
            return

        print("\nID   Member Name")
        print("-" * 35)

        for member_id, name in members:
            print(f"{member_id:<4} {name}")

    # --------------------------------------------------------
    # DELETE MEMBER
    # --------------------------------------------------------

    def delete_member(self):
        print("\n========== DELETE MEMBER ==========")

        self.view_members()

        try:
            member_id = int(input("\nEnter Member ID to delete: "))
        except ValueError:
            print("Invalid Member ID.")
            return

        self.cursor.execute(
            "SELECT id FROM members WHERE id = ?",
            (member_id,)
        )

        if self.cursor.fetchone() is None:
            print("Member not found.")
            return

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM loans
            WHERE member_id = ? AND returned = 0
            """,
            (member_id,)
        )

        if self.cursor.fetchone()[0] > 0:
            print("Cannot delete this member because they have a book on loan.")
            return

        self.cursor.execute(
            "DELETE FROM members WHERE id = ?",
            (member_id,)
        )

        self.conn.commit()

        print("Member deleted successfully.")

    # --------------------------------------------------------
    # ISSUE BOOK
    # --------------------------------------------------------

    def issue_book(self):
        print("\n========== ISSUE BOOK ==========")

        self.cursor.execute("""
            SELECT id, title, copies, available
            FROM books
            WHERE available > 0
            ORDER BY id
        """)

        books = self.cursor.fetchall()

        if not books:
            print("No books are currently available.")
            return

        print("\nAvailable Books:")

        for book_id, title, copies, available in books:
            print(
                f"{book_id}. {title} "
                f"({available}/{copies} available)"
            )

        try:
            book_id = int(input("\nEnter Book ID: "))
        except ValueError:
            print("Invalid Book ID.")
            return

        valid_book = False

        for book in books:
            if book[0] == book_id:
                valid_book = True
                break

        if not valid_book:
            print("Book not found or unavailable.")
            return

        self.cursor.execute("""
            SELECT id, name
            FROM members
            ORDER BY id
        """)

        members = self.cursor.fetchall()

        if not members:
            print("No members found. Please add a member first.")
            return

        print("\nMembers:")

        for member_id, name in members:
            print(f"{member_id}. {name}")

        try:
            member_id = int(input("\nEnter Member ID: "))
        except ValueError:
            print("Invalid Member ID.")
            return

        valid_member = False

        for member in members:
            if member[0] == member_id:
                valid_member = True
                break

        if not valid_member:
            print("Member not found.")
            return

        due_date = datetime.now() + timedelta(days=LOAN_DAYS)

        self.cursor.execute(
            """
            INSERT INTO loans
            (book_id, member_id, due_date, returned)
            VALUES (?, ?, ?, 0)
            """,
            (
                book_id,
                member_id,
                due_date.strftime("%Y-%m-%d")
            )
        )

        self.cursor.execute(
            """
            UPDATE books
            SET available = available - 1
            WHERE id = ?
            """,
            (book_id,)
        )

        self.conn.commit()

        print("\nBook issued successfully.")
        print(
            "Due date:",
            due_date.strftime("%Y-%m-%d")
        )

    # --------------------------------------------------------
    # VIEW LOANS
    # --------------------------------------------------------

    def view_loans(self):
        print("\n========== CURRENT LOANS ==========")

        self.cursor.execute("""
            SELECT loans.id,
                   books.title,
                   members.name,
                   loans.due_date
            FROM loans
            JOIN books
                ON loans.book_id = books.id
            JOIN members
                ON loans.member_id = members.id
            WHERE loans.returned = 0
            ORDER BY loans.id
        """)

        loans = self.cursor.fetchall()

        if not loans:
            print("No books are currently on loan.")
            return

        print(
            "\nLoan ID   Book                     "
            "Member               Due Date"
        )
        print("-" * 75)

        for loan_id, title, member_name, due_date in loans:
            print(
                f"{loan_id:<9}"
                f"{title:<25}"
                f"{member_name:<21}"
                f"{due_date}"
            )

    # --------------------------------------------------------
    # RETURN BOOK
    # --------------------------------------------------------

    def return_book(self):
        print("\n========== RETURN BOOK ==========")

        self.cursor.execute("""
            SELECT loans.id,
                   books.title,
                   members.name,
                   loans.due_date
            FROM loans
            JOIN books
                ON loans.book_id = books.id
            JOIN members
                ON loans.member_id = members.id
            WHERE loans.returned = 0
            ORDER BY loans.id
        """)

        loans = self.cursor.fetchall()

        if not loans:
            print("No books are currently on loan.")
            return

        print(
            "\nLoan ID   Book                     "
            "Member               Due Date"
        )
        print("-" * 75)

        for loan_id, title, member_name, due_date in loans:
            print(
                f"{loan_id:<9}"
                f"{title:<25}"
                f"{member_name:<21}"
                f"{due_date}"
            )

        try:
            loan_id = int(input("\nEnter Loan ID to return: "))
        except ValueError:
            print("Invalid Loan ID.")
            return

        self.cursor.execute(
            """
            SELECT book_id, due_date
            FROM loans
            WHERE id = ? AND returned = 0
            """,
            (loan_id,)
        )

        result = self.cursor.fetchone()

        if result is None:
            print("Loan not found.")
            return

        book_id, due_date_text = result

        today = datetime.now()
        due_date = datetime.strptime(
            due_date_text,
            "%Y-%m-%d"
        )

        late_days = (today - due_date).days

        if late_days > 0:
            fine = late_days * FINE_PER_DAY

            print(
                f"\nBook is {late_days} day(s) late."
            )

            print(f"Fine: Rs. {fine}")

        else:
            print("\nBook returned on time.")
            print("Fine: Rs. 0")

        self.cursor.execute(
            """
            UPDATE loans
            SET returned = 1
            WHERE id = ?
            """,
            (loan_id,)
        )

        self.cursor.execute(
            """
            UPDATE books
            SET available = available + 1
            WHERE id = ?
            """,
            (book_id,)
        )

        self.conn.commit()

        print("Book returned successfully.")

    # --------------------------------------------------------
    # CLI MENU
    # --------------------------------------------------------

    def run(self):

        while True:

            print("\n")
            print("=" * 45)
            print("       LIBRARY MANAGEMENT SYSTEM")
            print("              CLI MODE")
            print("=" * 45)

            print("1. Add Book")
            print("2. View Books")
            print("3. Delete Book")
            print("4. Add Member")
            print("5. View Members")
            print("6. Delete Member")
            print("7. Issue Book")
            print("8. View Books on Loan")
            print("9. Return Book")
            print("10. Exit")

            print("=" * 45)

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_book()

            elif choice == "2":
                self.view_books()

            elif choice == "3":
                self.delete_book()

            elif choice == "4":
                self.add_member()

            elif choice == "5":
                self.view_members()

            elif choice == "6":
                self.delete_member()

            elif choice == "7":
                self.issue_book()

            elif choice == "8":
                self.view_loans()

            elif choice == "9":
                self.return_book()

            elif choice == "10":
                print("\nExiting CLI...")
                break

            else:
                print("\nInvalid choice. Please enter 1-10.")

        self.conn.close()


# ============================================================
# GUI INTERFACE
# ============================================================

class LibraryGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("Library Management System")
        self.root.geometry("600x700")

        self.root.option_add(
            "*Font",
            "{Times New Roman} 12"
        )

        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

        self.book_ids = []
        self.available_book_ids = []
        self.member_ids = []
        self.loan_ids = []

        self.create_widgets()
        self.refresh_all()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

    # --------------------------------------------------------
    # GUI WIDGETS
    # --------------------------------------------------------

    def create_widgets(self):

        style = ttk.Style()

        style.configure(
            "TNotebook.Tab",
            font=FONT
        )

        tabs = ttk.Notebook(self.root)

        tabs.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        books_tab = tk.Frame(tabs)
        members_tab = tk.Frame(tabs)
        loans_tab = tk.Frame(tabs)

        tabs.add(
            books_tab,
            text="Books"
        )

        tabs.add(
            members_tab,
            text="Members"
        )

        tabs.add(
            loans_tab,
            text="Issue / Return"
        )

        # ====================================================
        # BOOK TAB
        # ====================================================

        tk.Label(
            books_tab,
            text="Book Title:"
        ).pack(pady=(10, 0))

        self.title_entry = tk.Entry(
            books_tab,
            width=35
        )

        self.title_entry.pack()

        tk.Label(
            books_tab,
            text="Number of Copies:"
        ).pack()

        self.copies_entry = tk.Entry(
            books_tab,
            width=10
        )

        self.copies_entry.pack()

        tk.Button(
            books_tab,
            text="Add Book",
            bg="light blue",
            command=self.add_book
        ).pack(pady=5)

        self.books_list = tk.Listbox(
            books_tab,
            width=55,
            height=12,
            exportselection=False
        )

        self.books_list.pack(pady=10)

        tk.Button(
            books_tab,
            text="Delete Selected Book",
            command=self.delete_book
        ).pack()

        # ====================================================
        # MEMBER TAB
        # ====================================================

        tk.Label(
            members_tab,
            text="Member Name:"
        ).pack(pady=(10, 0))

        self.member_entry = tk.Entry(
            members_tab,
            width=35
        )

        self.member_entry.pack()

        tk.Button(
            members_tab,
            text="Add Member",
            bg="light blue",
            command=self.add_member
        ).pack(pady=5)

        self.members_list = tk.Listbox(
            members_tab,
            width=55,
            height=12,
            exportselection=False
        )

        self.members_list.pack(pady=10)

        tk.Button(
            members_tab,
            text="Delete Selected Member",
            command=self.delete_member
        ).pack()

        # ====================================================
        # ISSUE / RETURN TAB
        # ====================================================

        tk.Label(
            loans_tab,
            text="Choose a book:"
        ).pack(pady=(10, 0))

        self.loan_books_list = tk.Listbox(
            loans_tab,
            width=55,
            height=6,
            exportselection=False
        )

        self.loan_books_list.pack()

        tk.Label(
            loans_tab,
            text="Choose a member:"
        ).pack(pady=(10, 0))

        self.loan_members_list = tk.Listbox(
            loans_tab,
            width=55,
            height=6,
            exportselection=False
        )

        self.loan_members_list.pack()

        tk.Button(
            loans_tab,
            text="Issue Book",
            bg="light green",
            command=self.issue_book
        ).pack(pady=5)

        tk.Label(
            loans_tab,
            text="Books currently on loan:"
        ).pack()

        self.loans_list = tk.Listbox(
            loans_tab,
            width=55,
            height=8,
            exportselection=False
        )

        self.loans_list.pack()

        tk.Button(
            loans_tab,
            text="Return Selected Book",
            bg="light yellow",
            command=self.return_book
        ).pack(pady=5)

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_all(self):

        self.load_books()
        self.load_members()
        self.load_loans()

    # ========================================================
    # BOOK FUNCTIONS
    # ========================================================

    def add_book(self):

        title = self.title_entry.get().strip()
        copies_text = self.copies_entry.get().strip()

        if not title or not copies_text:

            messagebox.showwarning(
                "Missing Information",
                "Please enter book title and number of copies."
            )

            return

        try:

            copies = int(copies_text)

            if copies <= 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Value",
                "Copies must be a positive whole number."
            )

            return

        self.cursor.execute(
            """
            INSERT INTO books
            (title, copies, available)
            VALUES (?, ?, ?)
            """,
            (
                title,
                copies,
                copies
            )
        )

        self.conn.commit()

        self.title_entry.delete(
            0,
            tk.END
        )

        self.copies_entry.delete(
            0,
            tk.END
        )

        self.refresh_all()

        messagebox.showinfo(
            "Success",
            "Book added successfully."
        )

    def load_books(self):

        self.books_list.delete(
            0,
            tk.END
        )

        self.loan_books_list.delete(
            0,
            tk.END
        )

        self.book_ids = []
        self.available_book_ids = []

        self.cursor.execute("""
            SELECT id, title, available, copies
            FROM books
            ORDER BY id
        """)

        books = self.cursor.fetchall()

        for book_id, title, available, copies in books:

            self.book_ids.append(
                book_id
            )

            line = (
                f"{title} "
                f"({available}/{copies} available)"
            )

            self.books_list.insert(
                tk.END,
                line
            )

            if available > 0:

                self.available_book_ids.append(
                    book_id
                )

                self.loan_books_list.insert(
                    tk.END,
                    line
                )

    def delete_book(self):

        selection = self.books_list.curselection()

        if not selection:

            messagebox.showwarning(
                "No Selection",
                "Please select a book."
            )

            return

        book_id = self.book_ids[
            selection[0]
        ]

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM loans
            WHERE book_id = ?
            AND returned = 0
            """,
            (book_id,)
        )

        active_loans = self.cursor.fetchone()[0]

        if active_loans > 0:

            messagebox.showwarning(
                "Cannot Delete",
                "This book is currently on loan."
            )

            return

        self.cursor.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,)
        )

        self.conn.commit()

        self.refresh_all()

    # ========================================================
    # MEMBER FUNCTIONS
    # ========================================================

    def add_member(self):

        name = self.member_entry.get().strip()

        if not name:

            messagebox.showwarning(
                "Missing Information",
                "Please enter member name."
            )

            return

        self.cursor.execute(
            """
            INSERT INTO members (name)
            VALUES (?)
            """,
            (name,)
        )

        self.conn.commit()

        self.member_entry.delete(
            0,
            tk.END
        )

        self.refresh_all()

        messagebox.showinfo(
            "Success",
            "Member added successfully."
        )

    def load_members(self):

        self.members_list.delete(
            0,
            tk.END
        )

        self.loan_members_list.delete(
            0,
            tk.END
        )

        self.member_ids = []

        self.cursor.execute("""
            SELECT id, name
            FROM members
            ORDER BY id
        """)

        members = self.cursor.fetchall()

        for member_id, name in members:

            self.member_ids.append(
                member_id
            )

            self.members_list.insert(
                tk.END,
                name
            )

            self.loan_members_list.insert(
                tk.END,
                name
            )

    def delete_member(self):

        selection = self.members_list.curselection()

        if not selection:

            messagebox.showwarning(
                "No Selection",
                "Please select a member."
            )

            return

        member_id = self.member_ids[
            selection[0]
        ]

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM loans
            WHERE member_id = ?
            AND returned = 0
            """,
            (member_id,)
        )

        active_loans = self.cursor.fetchone()[0]

        if active_loans > 0:

            messagebox.showwarning(
                "Cannot Delete",
                "This member currently has a book on loan."
            )

            return

        self.cursor.execute(
            "DELETE FROM members WHERE id = ?",
            (member_id,)
        )

        self.conn.commit()

        self.refresh_all()

    # ========================================================
    # ISSUE BOOK
    # ========================================================

    def issue_book(self):

        book_selection = (
            self.loan_books_list.curselection()
        )

        member_selection = (
            self.loan_members_list.curselection()
        )

        if not book_selection or not member_selection:

            messagebox.showwarning(
                "Missing Information",
                "Please select both a book and a member."
            )

            return

        book_id = self.available_book_ids[
            book_selection[0]
        ]

        member_id = self.member_ids[
            member_selection[0]
        ]

        due_date = (
            datetime.now()
            + timedelta(days=LOAN_DAYS)
        )

        self.cursor.execute(
            """
            INSERT INTO loans
            (book_id, member_id, due_date, returned)
            VALUES (?, ?, ?, 0)
            """,
            (
                book_id,
                member_id,
                due_date.strftime("%Y-%m-%d")
            )
        )

        self.cursor.execute(
            """
            UPDATE books
            SET available = available - 1
            WHERE id = ?
            """,
            (book_id,)
        )

        self.conn.commit()

        self.refresh_all()

        messagebox.showinfo(
            "Book Issued",
            "Book issued successfully.\n"
            f"Due date: {due_date.strftime('%Y-%m-%d')}"
        )

    # ========================================================
    # LOAD LOANS
    # ========================================================

    def load_loans(self):

        self.loans_list.delete(
            0,
            tk.END
        )

        self.loan_ids = []

        self.cursor.execute("""
            SELECT loans.id,
                   books.title,
                   members.name,
                   loans.due_date
            FROM loans
            JOIN books
                ON loans.book_id = books.id
            JOIN members
                ON loans.member_id = members.id
            WHERE loans.returned = 0
            ORDER BY loans.id
        """)

        loans = self.cursor.fetchall()

        for loan_id, title, member_name, due_date in loans:

            self.loan_ids.append(
                loan_id
            )

            self.loans_list.insert(
                tk.END,
                f"{title} -> {member_name} "
                f"(due {due_date})"
            )

    # ========================================================
    # RETURN BOOK
    # ========================================================

    def return_book(self):

        selection = self.loans_list.curselection()

        if not selection:

            messagebox.showwarning(
                "No Selection",
                "Please select a book to return."
            )

            return

        loan_id = self.loan_ids[
            selection[0]
        ]

        self.cursor.execute(
            """
            SELECT book_id, due_date
            FROM loans
            WHERE id = ?
            """,
            (loan_id,)
        )

        result = self.cursor.fetchone()

        if result is None:
            messagebox.showerror(
                "Error",
                "Loan record not found."
            )
            return

        book_id, due_date_text = result

        today = datetime.now()

        due_date = datetime.strptime(
            due_date_text,
            "%Y-%m-%d"
        )

        late_days = (
            today - due_date
        ).days

        if late_days > 0:

            fine = late_days * FINE_PER_DAY

            messagebox.showinfo(
                "Returned Late",
                f"Book is {late_days} day(s) late.\n"
                f"Fine: ₹{fine}"
            )

        else:

            messagebox.showinfo(
                "Returned",
                "Book returned on time.\n"
                "Fine: ₹0"
            )

        self.cursor.execute(
            """
            UPDATE loans
            SET returned = 1
            WHERE id = ?
            """,
            (loan_id,)
        )

        self.cursor.execute(
            """
            UPDATE books
            SET available = available + 1
            WHERE id = ?
            """,
            (book_id,)
        )

        self.conn.commit()

        self.refresh_all()

    # ========================================================
    # CLOSE GUI
    # ========================================================

    def close(self):

        self.conn.close()
        self.root.destroy()


# ============================================================
# MAIN INTERFACE SELECTION
# ============================================================

def main():

    setup_database()

    while True:

        print("\n")
        print("=" * 45)
        print("       LIBRARY MANAGEMENT SYSTEM")
        print("=" * 45)
        print()
        print("1. GUI Interface")
        print("2. CLI Interface")
        print("3. Exit")
        print()
        print("=" * 45)

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            # Open GUI
            root = tk.Tk()

            app = LibraryGUI(root)

            root.mainloop()

            # After closing GUI, return to interface selection

        elif choice == "2":

            # Start CLI
            cli = LibraryCLI()

            cli.run()

            # After exiting CLI, return to interface selection

        elif choice == "3":

            print(
                "\nThank you for using "
                "the Library Management System."
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please enter 1, 2, or 3."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()

