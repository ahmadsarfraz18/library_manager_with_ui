import json
import os
import streamlit as st

# File jahan library ka data store hoga
data_file = "library.txt"

def load_library():
    # Agar file mojood hai to data load karo
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    # Agar file mojood nahi hai to khali list return karo
    return []

def save_library(library):
    # Library ka data file mein save karo
    with open(data_file, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library):
    st.subheader("📚 Naya Kitaab Shamil Karein")
    st.markdown("---")
    # User se kitaab ka title, author, saal, aur genre lene ke liye input fields
    book_title = st.text_input("**Kitaab ka Naam**", placeholder="Kitaab ka naam likhein")
    book_author = st.text_input("**Musannif ka Naam**", placeholder="Musannif ka naam likhein")
    publishing_year = st.text_input("**Nashar ka Saal**", placeholder="Nashar ka saal likhein")
    book_genre = st.text_input("**Genre**", placeholder="Kitaab ka genre likhein")
    read = st.checkbox("Kya aap ne yeh kitaab parh li hai?")
    
    # Agar user "Add Book" ka button dabata hai to kitaab shamil karein
    if st.button("➕ Kitaab Shamil Karein", use_container_width=True):
        # Sab fields bharna zaroori hai
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
            st.success(f"✅ Kitaab '{book_title}' kamiyabi se shamil kar di gayi hai!")
        else:
            st.error("⚠️ Bara-e-karam sab fields bharain.")

def remove_book(library):
    st.subheader("🗑️ Kitaab Hatayein")
    st.markdown("---")
    # Library se tamaam kitaabon ke naam lein
    book_titles = [book["title"] for book in library]
    # User ko ek kitaab select karne dein jo delete karni hai
    selected_book = st.selectbox("Woh kitaab chunein jo hatani hai:", book_titles, index=0)
    
    # Agar user "Remove Book" ka button dabata hai to kitaab hata dein
    if st.button("❌ Kitaab Hatayein", use_container_width=True):
        library = [book for book in library if book['title'] != selected_book]
        save_library(library)
        st.success(f"🚮 Kitaab '{selected_book}' kamiyabi se hata di gayi hai!")

def search_library(library):
    st.subheader("🔍 Kitaab Talash Karein")
    st.markdown("---")
    # User ko talash ka option dein (title ya author)
    search_by = st.radio("Talash kis par karni hai:", ["title", "author"], horizontal=True)
    search_term = st.text_input(f"{search_by} likhein:", placeholder=f"{search_by} ke mutabiq talash karein")
    
    # Agar user "Search" ka button dabata hai to natayij dikhayein
    if st.button("🔎 Talash Karein", use_container_width=True):
        results = [book for book in library if search_term.lower() in book.get(search_by, '').lower()]
        if results:
            for book in results:
                st.markdown(f"**📖 {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Parhi hui' if book['read'] else '❌ Abhi nahi parhi'}")
        else:
            st.warning("⚠️ Koi natija nahi mila.")

def all_books(library):
    st.subheader("📚 Library ki Tamaam Kitaabein")
    st.markdown("---")
    # Agar library mein kitaabein mojood hain to dikhayein
    if library:
        for book in library:
            st.markdown(f"**📖 {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Parhi hui' if book['read'] else '❌ Abhi nahi parhi'}")
    else:
        st.info("ℹ️ Library mein koi kitaab mojood nahi hai.")

def display_statistics(library):
    st.subheader("📊 Library ki Maloomat")
    st.markdown("---")
    total_books = len(library)  # Library mein total kitaabein kitni hain
    read_books = sum(1 for book in library if book['read'])  # Kitni kitaabein parhi gae hain
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0  # Kitni kitaabein parhi gae hain (percentage)
    
    st.metric(label="📚 Total Kitaabein", value=total_books)
    st.metric(label="✅ Parhi gayi Kitaabein", value=read_books)
    st.metric(label="📈 Parhi gayi kitaabon ka ratio", value=f"{percentage_read:.2f}%")

def main():
    st.set_page_config(page_title="📖 Library Management System", layout="centered", page_icon="📚")
    st.sidebar.title("📚 Library Management")
    # Navigation menu jo user ko mukhtalif functions par lay jaye
    choice = st.sidebar.radio("Navigate", ["Add Book", "Remove Book", "Search Book", "View All Books", "View Statistics"], index=0)
    
    library = load_library()  # Library ka data load karein
    
    with st.sidebar:
        st.markdown("---")
        st.write("✨ Streamlit se banaya gaya by Mahar Ahmad Sarfraz ✨")
    
    # User ki choice k mutabiq function call karein
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
