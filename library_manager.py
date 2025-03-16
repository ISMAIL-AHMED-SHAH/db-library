import sqlite3
import streamlit as st
import matplotlib.pyplot as plt


# Database Setup
conn = sqlite3.connect("library.db", check_same_thread=False)
cursor = conn.cursor()

# Create books table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    year TEXT,
    genre TEXT,
    read_status TEXT
)
''')
conn.commit()

# Page title
st.title("📚 Personal Library Manager")

# Sidebar for navigation
menu = ["Add Book", "Remove Book", "Search Books", "View All Books", "Statistics"]
choice = st.sidebar.selectbox("📌 Choose an option", menu)

# Function to add a book
def add_book():
    st.subheader("📖 Add a New Book")
    title = st.text_input("📖 Book Title")
    author = st.text_input("✍️ Author Name")
    year = st.text_input("📅 Publication Year")
    genre = st.text_input("📚 Genre")
    read_status = st.radio("✅ Have you read this book?", ["Yes", "No"])
    
    if st.button("➕ Add Book"):
        cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)",
                       (title, author, year, genre, read_status))
        conn.commit()
        st.success(f"✅ '{title}' by {author} added successfully!")

# Function to remove a book
def remove_book():
    st.subheader("❌ Remove a Book")
    title = st.text_input("📖 Enter the title of the book to remove")
    
    if st.button("🗑️ Remove Book"):
        cursor.execute("DELETE FROM books WHERE LOWER(title) = LOWER(?)", (title,))
        conn.commit()
        st.success(f"✅ '{title}' removed successfully!")

# Function to search books
def search_books():
    st.subheader("🔍 Search Books")
    search_query = st.text_input("🔎 Enter book title or author")
    
    if st.button("🔍 Search"):
        cursor.execute("SELECT * FROM books WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ?", 
                       (f"%{search_query.lower()}%", f"%{search_query.lower()}%"))
        results = cursor.fetchall()
        
        if results:
            st.write("📚 Matching Books:")
            st.table(results)
        else:
            st.warning("⚠️ No matching books found.")

# Function to display all books
def display_books():
    st.subheader("📖 Your Library")
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    if books:
        st.table(books)
    else:
        st.info("📚 Your library is empty!")

# Function to show statistics
def display_statistics():
    st.subheader("📊 Library Statistics")

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 'Yes'")
    read_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 'No'")
    unread_books = cursor.fetchone()[0]

    if total_books > 0:
        read_percentage = (read_books / total_books) * 100
        unread_percentage = (unread_books / total_books) * 100

        # Display statistics
        st.write(f"📚 **Total Books:** {total_books}")
        st.write(f"✅ **Books Read:** {read_books} ({read_percentage:.1f}%)")
        st.write(f"❌ **Books Unread:** {unread_books} ({unread_percentage:.1f}%)")

        # 📊 Bar Chart
        st.subheader("📊 Read vs Unread Books")
        data = {"Read": read_books, "Unread": unread_books}
        st.bar_chart(data)

        # 📊 Pie Chart
        st.subheader("📊 Reading Progress")
        fig, ax = plt.subplots()
        ax.pie([read_books, unread_books], labels=["Read", "Unread"], autopct="%1.1f%%", colors=["#4CAF50", "#FF4B4B"])
        ax.axis("equal")
        st.pyplot(fig)

    else:
        st.info("📊 No books in the library yet.")

# Execute functions based on user choice
if choice == "Add Book":
    add_book()
elif choice == "Remove Book":
    remove_book()
elif choice == "Search Books":
    search_books()
elif choice == "View All Books":
    display_books()
elif choice == "Statistics":
    display_statistics()


# --- SIDEBAR TIPS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4359/4359808.png", width=100)
st.sidebar.header("📖 Library Management Tips")
st.sidebar.info("""
- Keep your book collection organized by genre.
- Use clear and consistent book titles for easy searching.
- Regularly update book status (read/unread).
- Backup your library database periodically.
- Explore different genres to broaden your knowledge.
""")

st.sidebar.markdown("---")

# Footer
st.sidebar.markdown("<p style='text-align: center; color: grey;'>Build with ❤️ By Ismail Ahmed Shah</p>", unsafe_allow_html=True)

# Add a 'Contact Us' section
st.sidebar.markdown("---")
st.sidebar.markdown("### 📬 Contact")

# Email Link
st.sidebar.write("📧 [Email Us](mailto:ismailahmedshahpk@gmail.com)")

# LinkedIn Link
st.sidebar.write("🔗 [Connect on LinkedIn](https://www.linkedin.com/in/ismail-ahmed-shah-2455b01ba/)")

# WhatsApp Link
st.sidebar.write("💬 [Chat on WhatsApp](https://wa.me/923322241405)")

