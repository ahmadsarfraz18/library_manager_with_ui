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
        json.dump(library, file, indent=4)

def add_book(library):
    st.subheader("📚 Add a New Book")
    st.markdown("---")
    book_title = st.text_input("**Book Title**", placeholder="Enter the book title")
    book_author = st.text_input("**Author Name**", placeholder="Enter the author's name")
    publishing_year = st.text_input("**Year of Publication**", placeholder="Enter publication year")
    book_genre = st.text_input("**Genre**", placeholder="Enter book genre")
    read = st.checkbox("Have you read this book?")
    
    if st.button("➕ Add Book", use_container_width=True):
        if book_title and book_author and publishing_year and book_genre:
            new_book = {
                "title": book_title,
                "author": book_author,
                "year": publishing_year,
                "genre": book_genre,
                "read": read
            }
            library.append(new_book)
            save_library(library)
            st.success(f"✅ Book '{book_title}' added successfully!")
        else:
            st.error("⚠️ Please fill in all fields.")

def remove_book(library):
    st.subheader("🗑️ Remove a Book")
    st.markdown("---")
    book_titles = [book["title"] for book in library]
    selected_book = st.selectbox("Select a book to remove:", book_titles, index=0)
    
    if st.button("❌ Remove Book", use_container_width=True):
        library = [book for book in library if book['title'] != selected_book]
        save_library(library)
        st.success(f"🚮 Book '{selected_book}' removed successfully!")

def search_library(library):
    st.subheader("🔍 Search for a Book")
    st.markdown("---")
    search_by = st.radio("Search by:", ["title", "author"], horizontal=True)
    search_term = st.text_input(f"Enter {search_by}:", placeholder=f"Search by {search_by}")
    
    if st.button("🔎 Search", use_container_width=True):
        results = [book for book in library if search_term.lower() in book.get(search_by, '').lower()]
        if results:
            for book in results:
                st.markdown(f"**📖 {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Not Read'}")
        else:
            st.warning("⚠️ No results found.")

def all_books(library):
    st.subheader("📚 All Books in the Library")
    st.markdown("---")
    if library:
        for book in library:
            st.markdown(f"**📖 {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Not Read'}")
    else:
        st.info("ℹ️ No books found in the library.")

def display_statistics(library):
    st.subheader("📊 Library Statistics")
    st.markdown("---")
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    
    st.metric(label="📚 Total Books", value=total_books)
    st.metric(label="✅ Books Read", value=read_books)
    st.metric(label="📈 Percentage Read", value=f"{percentage_read:.2f}%")

def main():
    st.set_page_config(page_title="📖 Library Management System", layout="centered", page_icon="📚")
    st.sidebar.title("📚 Library Management")
    choice = st.sidebar.radio("Navigate", ["Add Book", "Remove Book", "Search Book", "View All Books", "View Statistics"], index=0)
    
    library = load_library()
    
    with st.sidebar:
        st.markdown("---")
        st.write("✨ Designed with Streamlit by Mahar Ahmad Sarfraz ✨")
    
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
