import streamlit as st
import pandas as pd
import csv
from datetime import datetime
import bcrypt

class Book:
    def __init__(self, title="", date=""):
        self.title = title
        self.date = date

def login():
    st.title("Login Page")

    st.write("Nama (Login):")
    nama_login = st.text_input(" ", key="nama_login")

    st.write("NIM (Login):")
    nim_login = st.text_input(" ", key="nim_login")

    st.write("Password (Login):")
    password_login = st.text_input(" ", type="password", key="password_login")

    if st.button("Login"):
        try:
            # Baca data pengguna dari file CSV (atau database)
            with open('data_pengguna.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and len(row) == 3 and row[0] == nama_login and row[1] == nim_login and bcrypt.checkpw(password_login.encode('utf-8'), row[2].encode('utf-8')):
                        # Initialize session_state attributes
                        st.session_state.logged_in = True
                        st.session_state.nama = nama_login
                        st.session_state.nim = nim_login

                        st.success("Login berhasil.")
                        app = LibraryApp()
                        app.display_menu()
                        return

            st.error("Nama, NIM, atau password salah. Silakan coba lagi.")
            st.get_option("Belum punya akun? Daftar sekarang!")
        except Exception as e:
            st.error(f"Error during login: {e}")

def signup():
    st.title("Signup Page")
    st.write("Nama (Register):")
    nama_regis = st.text_input(" ", key="nama_regis")

    # NIM (Register)
    st.write("NIM (Register):")
    nim_regis = st.text_input(" ", key="nim_regis")

    # Password (Register)
    st.write("Password (Register):")
    password_regis = st.text_input(" ", type="password", key="password_regis")

    if st.button("Sign Up"):
        try:
            # Simpan data pengguna ke file CSV (atau database)
            with open('data_pengguna.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                hashed_password = bcrypt.hashpw(password_regis.encode('utf-8'), bcrypt.gensalt())
                writer.writerow([nama_regis, nim_regis, hashed_password.decode('utf-8')])

            st.success("Pendaftaran berhasil. Silakan login.")
        except Exception as e:
            st.error(f"Error during registration: {e}")



class LibraryApp:
    def __init__(self):
        self.df_books = pd.DataFrame(columns=['Book Name', 'Author', 'Genre', 'Quantity'])
        self.df_borrowed = pd.DataFrame(columns=['nama', 'nim', 'book name', 'borrow date', 'return date'])

        try:
            self.df_books = pd.read_csv('daftar_buku.csv')
        except pd.errors.ParserError as e:
            st.error(f"Error parsing CSV file: {e}")
            st.stop()

    def display_book_list(self):
        st.subheader("Daftar Buku")
        label_genre = st.selectbox('Pilih Genre:', ['Semua'] + self.df_books['Genre'].unique().tolist())
        filtered_df = self.df_books if label_genre == 'Semua' else self.df_books[self.df_books['Genre'] == label_genre]

        with st.expander("Daftar Buku"):
            st.dataframe(filtered_df)

    def borrow_book(self):
        st.subheader("Pinjam Buku")

        try:
            self.df_borrowed = pd.read_csv('peminjaman.csv')
        
        except pd.errors.ParserError as e:
            st.error(f"Error parsing borrowing CSV file: {e}")
            self.df_borrowed = pd.DataFrame(columns=['nama', 'nim', 'book name', 'borrow date', 'return date', 'keterangan'])
           
        book_names = self.df_books['Book Name'].tolist()

        # Create a Combobox for book selection
        book_name = st.selectbox("Pilih Buku:", [""] + book_names)

        if book_name:
            # Check if the selected book is available
            if book_name in self.df_books['Book Name'].values:
                # Get the index of the selected book in df_books
                book_index = self.df_books[self.df_books['Book Name'] == book_name].index[0]

                borrow_date = st.date_input("Tanggal Peminjaman", min_value=datetime.now().date())

            # Simpan informasi pengguna
            nama = st.session_state.nama
            nim = st.session_state.nim

            # Check if the user has already borrowed the selected book and not returned it
            already_borrowed = self.df_borrowed[(self.df_borrowed['nama'] == nama) & (self.df_borrowed['book name'] == book_name) & (self.df_borrowed['keterangan'] == 'Belum dikembalikan')]

            if not already_borrowed.empty:
                st.warning(f"Anda belum mengembalikan buku '{book_name}'. Silakan kembalikan buku sebelum meminjam yang lain.")
                return

            # Add a date picker for return date
            return_date = st.date_input("Pilih Tanggal Pengembalian:", min_value=datetime.now())

            # Check if the selected book is available (quantity > 0) before borrowing
            selected_book = self.df_books[self.df_books['Book Name'] == book_name]
            if selected_book['Quantity'].values[0] <= 0:
                st.warning(f"Maaf, stok buku '{book_name}' sudah habis.")
                return

            # Button to perform borrowing action
            if st.button("Pinjam Buku"):
                # Perform borrowing action
                st.success(f"Buku '{book_name}' berhasil dipinjam oleh {nama} ({nim}). Tanggal peminjaman: {borrow_date}, Tanggal pengembalian: {return_date.strftime('%Y-%m-%d')}")

                # Update the DataFrame with the new borrowing details
                new_borrowing = {'nama': [nama], 'nim': [nim], 'book name': [book_name], 'borrow date': [borrow_date], 'return date': [return_date.strftime('%Y-%m-%d')], 'keterangan': 'Belum dikembalikan'}
                self.df_borrowed = pd.concat([self.df_borrowed, pd.DataFrame(new_borrowing)], ignore_index=True)

                # Update the quantity of the borrowed book in df_books
                self.df_books.at[book_index, 'Quantity'] -= 1
                # Save the updated DataFrames to their respective files
                self.df_borrowed.to_csv('peminjaman.csv', index=False)
                self.df_books.to_csv('daftar_buku.csv', index=False)

                # Optionally, you can update the displayed book list after borrowing
                self.display_book_list()

    def return_book(self):
        st.subheader("Kembalikan Buku")

        try:
            self.df_borrowed = pd.read_csv('peminjaman.csv', parse_dates=['return date'])
            self.df_books = pd.read_csv('daftar_buku.csv')
        except pd.errors.ParserError as e:
            st.error(f"Error parsing borrowing or book CSV file: {e}")
            self.df_borrowed = pd.DataFrame(columns=['nama', 'nim', 'book name', 'borrow date', 'return date', 'keterangan'])
            self.df_books = pd.DataFrame(columns=['Book Name', 'Quantity', 'borrow date'])

        nama = st.session_state.nama

        # Filter borrowed books for the current user
        filtered = self.df_borrowed[(self.df_borrowed['nama'] == nama) & (self.df_borrowed['keterangan'] == 'Belum dikembalikan')]

        if filtered.empty:
            st.warning("Anda belum meminjam buku.")
            return
        else:
            book_names = filtered['book name'].tolist()
            book_name = st.selectbox("Pilih Buku yang Akan Dikembalikan:", book_names)

            if filtered.empty:
                st.warning("Semua buku sudah dikembalikan")
            else:
                return_date = st.date_input("Pilih Tanggal Pengembalian", min_value=datetime.now().date())
                borrowed_date = filtered.loc[filtered['book name'] == book_name, 'borrow date'].iloc[0]

                # Ensure 'borrow date' and 'return date' are datetime objects
                borrowed_date = pd.to_datetime(borrowed_date)
                return_date = pd.to_datetime(return_date)

                # Calculate late return penalty
                days_late = (return_date - borrowed_date).days
                late_penalty = max(0, days_late) * 1000

                if st.button("Kembalikan Buku"):
                    if days_late > 0:
                        st.success(f"Buku '{book_name}' berhasil dikembalikan oleh {nama}. "
                                f"Tanggal pengembalian: {return_date.strftime('%Y-%m-%d')}. "
                                f"Denda terlambat: Rp {late_penalty:,.0f}")
                    else:
                        st.success(f"Buku '{book_name}' berhasil dikembalikan oleh {nama}. "
                                f"Tanggal pengembalian: {return_date.strftime('%Y-%m-%d')}. "
                                f"Tidak ada denda terlambat.")

                    # Update the 'keterangan' column to 'Sudah dikembalikan'
                    filter = (self.df_borrowed['nama'] == nama) & (self.df_borrowed['book name'] == book_name)
                    self.df_borrowed.loc[filter, 'keterangan'] = 'Sudah dikembalikan'

                    # Increase the quantity of the returned book in the book list
                    book_index = self.df_books[self.df_books['Book Name'] == book_name].index[0]
                    self.df_books.at[book_index, 'Quantity'] += 1

                    # Save the updated DataFrames to the respective CSV files
                    self.df_borrowed.to_csv('peminjaman.csv', index=False)
                    self.df_books.to_csv('daftar_buku.csv', index=False)

                    # Optionally, you can update the displayed book list after returning
                    self.display_book_list()

               
    def add_book(self):
        st.subheader("Sumbang Buku")

        book_name = st.text_input("Nama Buku:")
        author = st.text_input("Penulis:")
        genre = st.text_input("Genre:")
        quantity = st.number_input("Jumlah Buku:", min_value=1, value=1)

        if st.button("Sumbangkan Buku"):
            st.success("Terimakasih sudah menyumbang buku.")
            # Ensure 'Quantity' column is present
            if 'Quantity' not in self.df_books.columns:
                self.df_books['Quantity'] = 0

            # Check if the book already exists in the DataFrame
            if book_name in self.df_books['Book Name'].tolist():
                # If it exists, update the quantity
                book_index = self.df_books[self.df_books['Book Name'] == book_name].index[0]
                self.df_books.at[book_index, 'Quantity'] += quantity
            else:
                # If it doesn't exist, append a new row
                new_book = {'Book Name': book_name, 'Author': author, 'Genre': genre, 'Quantity': quantity}
                self.df_books = pd.concat([self.df_books, pd.DataFrame(new_book, index=[0])], ignore_index=True)

            # Save the updated DataFrame to the CSV file
            self.df_books.to_csv('daftar_buku.csv', index=False)

    def display_menu(self):
        st.title("Perpustakaan Digital")
        st.subheader("Universitas Negeri Surabaya")
        tabs = ["Daftar Buku", "Pinjam Buku", "Kembalikan Buku", "Sumbang Buku"]
        selected_tab = st.sidebar.radio("Menu", tabs)

        if selected_tab == "Daftar Buku":
            self.display_book_list()
        elif selected_tab == "Pinjam Buku":
            self.borrow_book()
        elif selected_tab == "Kembalikan Buku":
            self.return_book()
        elif selected_tab == "Sumbang Buku":
            self.add_book()
    
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()

def main():
    if not getattr(st.session_state, 'logged_in', False):
        st.title("Welcome!")
        choice = st.radio("Choose an action:", ["**Login**", "**Sign Up**"], key="action_choice")

        if choice == "**Login**":
            login()
        elif choice == "**Sign Up**":
            signup()
    else:
        app = LibraryApp()
        app.display_menu()

if __name__ == "__main__":
    main()
