from database import Database
import sqlite3
import csv

class Cash:
    def __init__(self):
        self.db = Database()
    
    def create_cash_document(self, doc_date, comment):
        """Add a new cash doc record."""
        self.db.execute("INSERT INTO cash_document (doc_date, comment) VALUES (?, ?)", (doc_date, comment))
        print("Cash document record added successfully!")

    def read_cash_documents(self, show_non_active=False):
        """Fetch and display cash documents."""
        if show_non_active == False:
            return self.db.fetchall("SELECT * FROM cash_document WHERE is_active != 0")
        else:
            return self.db.fetchall("SELECT * FROM cash_document WHERE is_active = 0")
        
    def delete_document(self, doc_id):
        self.db.execute("UPDATE cash_document SET is_active = 0 WHERE id = ?", (doc_id))
    
    def activate_document(self, doc_id):
        self.db.execute("UPDATE cash_document SET is_active = 1 WHERE id = ?", (doc_id))
    
    # def read_cash(self):
    #     self.db.fetchall("")
