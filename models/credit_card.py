from database import Database
import sqlite3

class CreditCard:
    def __init__(self):
        self.db = Database()

    def create_credit_card(self, amount, employee_id):
        """Add a new credit card record."""
        self.db.execute("INSERT INTO credit_card (amount, employee_id) VALUES (?, ?)", (amount, employee_id))
        print("Credit card record added successfully!")

    def read_credit_cards(self):
        """Fetch and display credit cards."""
        # return self.db.fetchall("SELECT cc.id, cc.amount, e.name FROM credit_card cc JOIN employees e ON cc.employee_id = e.id")
        return self.db.fetchall("SELECT * FROM aylyk")
    # def sum_credit_card(self):
    #     """Calculate total credit card amounts."""
    #     result = self.db.fetchone("SELECT SUM(amount) FROM credit_card")
    #     return result[0] if result else 0

    def update_credit_card(self, card_id, amount, employee_id):
        """Update a credit card record."""
        self.db.execute("UPDATE credit_card SET amount = ?, employee_id = ? WHERE id = ?", (amount, employee_id, card_id))
        print("Credit card record updated successfully!")

    def delete_credit_card(self, card_id):
        """Delete a credit card record."""
        try:
            self.db.execute("DELETE FROM credit_card WHERE id = ?", (card_id,))
            print(f"✅ Credit card ID {card_id} deleted successfully.")
        except sqlite3.IntegrityError:
            print(f"❌ Cannot delete Credit card ID {card_id} because it is referenced elsewhere.")

    def sum_credit_card(self):
        amount = self.db.fetchall("SELECT sum(amount) FROM credit_card")

        count = self.db.fetchall("SELECT count(id) FROM credit_card")

        if amount and count:
            print(f"Jemi: {amount[0][0]}, Isgar: {count[0][0]}")
        else:
            print("No salary records found.")