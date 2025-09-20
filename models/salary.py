from database import Database
import sqlite3
import csv

class Salary:
    def __init__(self):
        self.db = Database()

    def create_salary(self, amount, employee_id):
        """Add a new salary record."""
        self.db.execute("INSERT INTO salary (amount, employees_id) VALUES (?, ?)", (amount, employee_id))
        print("Salary record added successfully!")

    def read_salaries(self):
        """Fetch and display salaries."""
        return self.db.fetchall(
            "SELECT s.id, e.id, e.name, s.amount, p.title as Position FROM salary s " \
            "JOIN employees e ON s.employees_id = e.id " \
            "JOIN positions p ON e.position_id = p.id")

    def sum_salary(self):
        """Calculate total salaries."""
        result = self.db.fetchone("SELECT SUM(amount) FROM salary")
        return result[0] if result else 0

    def update_salary(self, sal_id, amount, employee_id):
        """Update a salary record."""
        self.db.execute("UPDATE salary SET amount = ?, employees_id = ? WHERE id = ?", (amount, employee_id, sal_id))
        print("Salary record updated successfully!")

    def delete_salary(self, sal_id):
        """Delete a salary record."""
        try:
            self.db.execute("DELETE FROM salary WHERE id = ?", (sal_id,))
            print(f"✅ Salary ID {sal_id} deleted successfully.")
        except sqlite3.IntegrityError:
            print(f"❌ Cannot delete Salary ID {sal_id} because it is referenced elsewhere.")

    def sum_salary(self):
        amount = self.db.fetchall("SELECT sum(amount) FROM salary")

        if amount:
            print(f"Jemi: {amount[0][0]}")
        else:
            print("No salary records found.")
    
    def export_salaries_to_csv(self, filename):
        """
        Export all salaries to a CSV file.
        """
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM salary")

        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)   # column names
            writer.writerows(rows)

        print(f"✅ Exported {len(rows)} positions to {filename}")
    
    def import_salaries_from_csv(self, filename):
        """
        Import salaries from CSV.
        - If ID is blank → insert new salary (auto id).
        - If ID exists → update that salary.
        - If ID does not exist → insert with that ID.
        """
        cursor = self.db.conn.cursor()
        inserted, updated = 0, 0

        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                id = row.get("id", "").strip()
                amount = row.get("amount", "").strip()
                employees_id = row.get("employees_id", "").strip()
                is_active = row.get("is_active", "1").strip()  # default active=1

                if id == "":
                    # New employee → let DB generate ID
                    cursor.execute("""
                        INSERT INTO salary (amount, employees_id, is_active)
                        VALUES (?, ?, ?)
                    """, (amount, employees_id, is_active))
                    inserted += 1
                else:
                    # Try update existing
                    cursor.execute("""
                        UPDATE salary
                        SET amount=?, employees_id=?, is_active=?
                        WHERE id=?
                    """, (amount, employees_id, is_active, id))

                    if cursor.rowcount == 0:
                        # If no row updated → insert with given id
                        cursor.execute("""
                            INSERT INTO salary (id, amount, emoloyees_id, is_active)
                            VALUES (?, ?, ?, ?)
                        """, (id, amount, employees_id, is_active))
                    updated += 1

        self.db.conn.commit()
        print(f"✅ Imported: {inserted} new, {updated} updated salaries from {filename}")    