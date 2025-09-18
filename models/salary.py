from database import Database
import sqlite3

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
