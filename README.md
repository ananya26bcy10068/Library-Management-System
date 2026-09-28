# Library Management System (Python & SQLite Desktop Project)

📌 What is this?
This is a lightweight Python desktop app designed to help small local libraries or reading rooms drop paper registers and messy spreadsheets. Built using Tkinter for the front end and SQLite for the back end, it gives a librarian a single workspace to keep tabs on books, track student profiles, and log active checkouts without losing data when the application closes.

📌 What it does?
1. Inventory Logging: Quick fields to add or remove books from the library list along with their total copy counts.
2. Student/Member Profiles: Basic registration system to log readers by name.
3. Check-out System: Allows the librarian to highlight a book and a student simultaneously to issue the item on the spot.
4. Automated Deadlines: The app automatically sets a 14-day return window from the exact day a book is checked out.
5. Return & Fine Handler: Clears active loans upon book return and calculates late fees if the students misses their due date.
6. Local Database Storage: Saves everything to a local library.db file file using SQLite, so all records stay intact between runs.
7. Simple Tabbed Layout: Organised into three clean, dedicated tabs (Books, Members, and Issue-Return) using consistent Times New Roman typography.

📌 Built With
1. Language: Python 3.7+ 
2. Interface: Tkinter (Python's built-in GUI library) 
3. Database: SQLite (via standard sqlite3 module) 
4. Date Calculations: Python's native datetime 

📌 Getting Started
### 1. Check Python installation
Make sure Python is ready on your machine by opening a terminal and typing:
bash
python --version

### 2. Grab the project files
Download or clone this repository folder to your local drive.
### 3. Setup dependencies
You do not need to run any pip install commands. Both Tkinter and SQLite come packaged with standard Python installations.
### 4. Run the script
Navigate inside the project folder and launch the app using:
bash
python library_management.py

📌 Testing Checklist
Run through these basic checks to verify the program behaves correctly:
### 1. Adding New Inventory
* Open the app, head to the **Books** tab, type `Python Basics` under title, set copies to `2`, and hit **Add Book**.
* Verification: The book should drop into the list display showing `Python Basics (2/2 available)`.

### 2. Creating a Student Record
* Go over to the Members tab, enter a name like "Ananya", and click **Add Member**.
* Verification: The name should instantly update inside the member directory list.

### 3. Book Allocation Window
* Under the **Issue / Return** tab, select your book and the student name from the parallel lists, then click **Issue Book**. 
* Verification: A popup dialogue should flash confirming the return deadline, and the transaction will move into the active loans display.

### 4. Processing Returns
* Select an active record from the "Books currently on loan" box and click **Return Selected Book**.
* Verification: A confirmation window should appear. If the return date is past the 14-day mark, it will print out the penalty fee.

### 5. Crash Prevention (Input Validation)
* Try hitting the add book button with characters typed into the copies box or leaving it completely blank.
* Verification: Instead of crashing or throwing terminal errors, the app should intercept the bad input and show an alert popup.

📌 Folder Layout
library management system
  ├── library_management.py
  ├── README.md
  ├── statement.md
  ├── library.db          (Generated automatically on the first launch)
  └── /recordings


## 📌 Interface Previews
1. **Inventory Setup:** Registering titles and defining available stock counts.
<img width="687" height="843" alt="image" src="https://github.com" />

2. **Issuing Workflow:** Selecting a borrower profile alongside a target book item.
<img width="1022" height="851" alt="image-1" src="https://github.com" />

3. **Return Settlement:** Closing active loans and checking time-stamps for fine evaluation.
<img width="1042" height="852" alt="image-2" src="https://github.com" />
