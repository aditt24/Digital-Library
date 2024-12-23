# Digital-Library

## Description
This project is a web-based digital library system designed to facilitate students in accessing book collections, borrowing, returning, and donating books online. This application uses Streamlit as its interface framework.

## Key Features
- **Login and Sign Up**: Authentication system with password encryption using BCrypt.
- **Book Management**:
  - **Book List**: Displays collections by genre.
  - **Borrow Books**: Validates book stock availability and records borrowing details.
  - **Return Books**: Handles book returns and calculates late return fines.
  - **Donate Books**: Adds new books to the library collection.
- **Interactive Dashboard**: Easy navigation via sidebar.

## Technologies Used
- **Programming Language**: Python
- **Framework**: Streamlit
- **Data Storage**: CSV
- **Encryption**: BCrypt for password security

## Folder Structure
```
Digital-Library/
├── data/
│   ├── daftar_buku.csv
│   ├── data_pengguna.csv
│   ├── peminjaman.csv
│   └── pengembalian.csv
├── src/
│   └── library_project.py
├── README.md
└── requirements.txt
```

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/Digital-Library.git
   cd Digital-Library
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   streamlit run src/library_project.py
   ```

## Usage
1. **Login or Sign Up**:
   - New users must register with their name, student ID, and password.
   - Log in with a registered account.
2. **Access Features**:
   - View the book list by genre.
   - Borrow books by specifying a return date.
   - Return books and pay fines if overdue.
   - Add new books to the library collection.

## Contributor
- Aditya Saputra
