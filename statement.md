## 📌Program Statement
Libraries whether in a school , college or a small community often struggle with keeping track of books using registers or spreadsheets . This manual approach is slow , prone to human error and makes it hard to quickly answer simple questions like "is this book available right now?" or "who currently has this book and is it overdue?"

## 📌Scope of the Project
This project aims to develop a Library Management System , a client-side desktop application that replaces the manual register with a simple , reliable digital tool. It bridges the gap between paper-based record keeping and easy-to-use software solution.

The scope includes:
* **Book Management:** Adding and removing books , along with tracking how many copies exist and how many are currently available .
* **Member Management:** Maintaining simple list of registered members who are allowed to borrow books .
* **Loan Tracking:** Issuing a book to a member , recording the due date and marking it as returned once it comes back , including calculating late fines automatically .
* **Data Persistence:** All records are stored locally so the librarian's data is safe even after closing the program .

## 📌Target Users
* **School/College Librarians:** Staff who need a lightweight way to track book issues and returns without expensive software .
* **Small Community Libraries:** Volunteer-run libraries that don't have the budget for a commercial library system .
* **Students Learning Programming:** A practical example of combining a GUI with a database for an introductory programming course .

## 📌High-Level Features
* **Book Catalog:** Add and remove books , each tracked with a title and copy count .
* **Member Directory:** Add and remove members by name .
* **Issue & Return Workflow:** Select a book and a member together to issue a loan and select an active loan to return it .
* **Automatic Due Dates & Fines:** Every loan gets a 14-day due date and returning a book late automatically calculates a fine .
* **Reliable Local Storage:** Uses an SQLite database so no data is lost between runs of the program .
