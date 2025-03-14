import json
import os
import streamlit as st

# File where library data will be stored
data_file = "library.txt"

def load_library():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, "w") as file:
        json.dump(library, file)

def add_book(library):
    st.subheader("Add a New Book")
    book_title = st.text_input("Enter the title of the book:")
    book_author = st.text_input("Enter the name of the author:")
    publishing_year = st.text_input("Enter the year of publication:")
    book_genre = st.text_input("Enter the genre of the book:")
    read = st.checkbox("Have you read this book before?")
    
    if st.button("Add Book"):
        new_book = {
            "title": book_title,
            "author": book_author,
            "year": publishing_year,
            "genre": book_genre,
            "read": read
        }
        library.append(new_book)
        save_library(library)
        st.success(f"Book '{book_title}' added successfully!")

def remove_book(library):
    st.subheader("Remove a Book")
    book_titles = [book["title"] for book in library]
    selected_book = st.selectbox("Select a book to remove:", book_titles)
    
    if st.button("Remove Book"):
        library = [book for book in library if book['title'] != selected_book]
        save_library(library)
        st.success(f"Book '{selected_book}' removed successfully!")

def search_library(library):
    st.subheader("Search for a Book")
    search_by = st.selectbox("Search by:", ["title", "author"])
    search_term = st.text_input(f"Enter {search_by}:")
    
    if st.button("Search"):
        results = [book for book in library if search_term.lower() in book.get(search_by, '').lower()]
        if results:
            for book in results:
                st.write(f"{book['title']} by {book['author']} - {book['year']} - {book['genre']} - {'Read' if book['read'] else 'Not Read'}")
        else:
            st.warning("No results found.")

def all_books(library):
    st.subheader("All Books in the Library")
    if library:
        for book in library:
            st.write(f"{book['title']} by {book['author']} - {book['year']} - {book['genre']} - {'Read' if book['read'] else 'Not Read'}")
    else:
        st.info("No books found in the library.")

def display_statistics(library):
    st.subheader("Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    
    st.write(f"Total books: {total_books}")
    st.write(f"Books read: {read_books}")
    st.write(f"Percentage read: {percentage_read:.2f}%")

def main():
    st.set_page_config(page_title="Library Management System", layout="wide")
    st.sidebar.title("Library Management")
    choice = st.sidebar.radio("Select an option:", ["Add Book", "Remove Book", "Search Book", "View All Books", "View Statistics"])
    
    library = load_library()
    
    if choice == "Add Book":
        add_book(library)
    elif choice == "Remove Book":
        remove_book(library)
    elif choice == "Search Book":
        search_library(library)
    elif choice == "View All Books":
        all_books(library)
    elif choice == "View Statistics":
        display_statistics(library)

if __name__ == "__main__":
    main()
