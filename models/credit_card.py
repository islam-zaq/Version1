from database import Database
import sqlite3
import csv

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
    
    def export_credit_cards_to_csv(self, filename):
        """
        Export all credit cards to a CSV file.
        Columns: id, amount, employee_id, is_active
        """
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, amount, employee_id, is_active FROM credit_card")
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"✅ Exported {len(rows)} credit cards to {filename}")

    def import_credit_cards_from_csv(self, filename):
        """
        Import credit cards from CSV.
        - If ID is blank → insert new card (auto id).
        - If ID exists → update that card.
        - If ID does not exist → insert with that ID.
        """
        cursor = self.db.conn.cursor()
        inserted, updated = 0, 0

        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            expected_headers = ["id", "amount", "employee_id", "is_active"]
            if reader.fieldnames != expected_headers:
                print(f"❌ Error: CSV headers must be {expected_headers}, got {reader.fieldnames}")
                return

            for row in reader:
                card_id = row["id"].strip()
                amount = row["amount"].strip()
                employee_id = row["employee_id"].strip()
                is_active = row["is_active"].strip() or "1"

                if card_id == "":
                    cursor.execute("""
                        INSERT INTO credit_card (amount, employee_id, is_active)
                        VALUES (?, ?, ?)
                    """, (amount, employee_id, is_active))
                    inserted += 1
                else:
                    cursor.execute("""
                        UPDATE credit_card
                        SET amount=?, employee_id=?, is_active=?
                        WHERE id=?
                    """, (amount, employee_id, is_active, card_id))

                    if cursor.rowcount == 0:
                        cursor.execute("""
                            INSERT INTO credit_card (id, amount, employee_id, is_active)
                            VALUES (?, ?, ?, ?)
                        """, (card_id, amount, employee_id, is_active))
                    updated += 1

        self.db.conn.commit()
        print(f"✅ Imported: {inserted} new, {updated} updated credit cards from {filename}")