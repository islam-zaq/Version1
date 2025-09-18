from database import Database
import sqlite3

class Document:
    def __init__(self):
        self.db = Database()

    def create_document(self, title, description, date, worked_date):
        """Add a new document."""
        self.db.execute("INSERT INTO documents (title, description, date, worked_date) VALUES (?, ?, ?, ?)",
                        (title, description, date, worked_date))
        print("Document added successfully!")

    def read_documents(self):
        """Fetch and display documents."""
        return self.db.fetchall("SELECT * FROM documents")

    def update_document(self, doc_id, title, description, date):
        """Update a document."""
        self.db.execute("UPDATE documents SET title = ?, description = ?, date = ? WHERE id = ?", (title, description, date, doc_id))
        print("Document updated successfully!")

    def delete_document(self, doc_id):
        """Delete a document."""
        try:
            self.db.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
            print(f"✅ Document ID {doc_id} deleted successfully.")
        except sqlite3.IntegrityError:
            print(f"❌ Cannot delete Document ID {doc_id} because it is referenced elsewhere.")
