from database import Database
import sqlite3
import csv

class Employee:
    def __init__(self):
        self.db = Database()

    def create_employee(self, name, position_id):
        """Add a new employee."""
        self.db.execute("INSERT INTO employees (name, position_id) VALUES (?, ?)", (name, position_id))
        print("Employee added successfully!")

    def read_employees(self):
        """Fetch and display employees."""
        employees = self.db.fetchall('''SELECT e.id, e.name, p.title 
                                        FROM employees e 
                                        JOIN positions p ON e.position_id = p.id WHERE e.is_active = 1''')
        return employees

    def update_employee(self, emp_id, name, position_id):
        """Update an employee."""
        self.db.execute("UPDATE employees SET name = ?, position_id = ? WHERE id = ?", (name, position_id, emp_id))
        print("Employee updated successfully!")

    def delete_employee(self, emp_id):
        """Delete an employee."""
        try:
            self.db.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
            print(f"✅ Employee ID {emp_id} deleted successfully.")
        except sqlite3.IntegrityError:
            print(f"❌ Cannot delete Employee ID {emp_id} because it is referenced elsewhere.")

    def fire_employee(self, emp_id):
        """Mark an employee as fired instead of deleting."""
        self.db.execute("UPDATE employees SET is_active = 0 WHERE id = ?", (emp_id,))
        print(f"✅ Employee ID {emp_id} has been fired.")

    def read_fired_employees(self):
        """Fetch and display fired employees."""
        employees = self.db.fetchall('''SELECT e.id, e.name, p.title 
                                        FROM employees e 
                                        JOIN positions p ON e.position_id = p.id WHERE e.is_active = 0''')
        return employees

    def unfire_employee(self, emp_id):
        """Restore a fired employee to active status."""
        self.db.execute("UPDATE employees SET is_active = 1 WHERE id = ?", (emp_id,))
        print(f"✅ Employee ID {emp_id} has been reactivated.")

    def export_employees_to_csv(self, filename):
        """
        Export all employees to a CSV file.
        """
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM employees")

        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)   # column names
            writer.writerows(rows)

        print(f"✅ Exported {len(rows)} employees to {filename}")
    
    def import_employees_from_csv(self, filename):
        """
        Import employees from CSV.
        - If ID is blank → insert new employee (auto id).
        - If ID exists → update that employee.
        - If ID does not exist → insert with that ID.
        """
        cursor = self.db.conn.cursor()
        inserted, updated = 0, 0

        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                emp_id = row.get("id", "").strip()
                name = row.get("name", "").strip()
                position_id = row.get("position_id", "").strip() or None
                is_active = row.get("is_active", "1").strip()  # default active=1

                if emp_id == "":
                    # New employee → let DB generate ID
                    cursor.execute("""
                        INSERT INTO employees (name, position_id, is_active)
                        VALUES (?, ?, ?)
                    """, (name, position_id, is_active))
                    inserted += 1
                else:
                    # Try update existing
                    cursor.execute("""
                        UPDATE employees
                        SET name=?, position_id=?, is_active=?
                        WHERE id=?
                    """, (name, position_id, is_active, emp_id))

                    if cursor.rowcount == 0:
                        # If no row updated → insert with given id
                        cursor.execute("""
                            INSERT INTO employees (id, name, position_id, is_active)
                            VALUES (?, ?, ?, ?)
                        """, (emp_id, name, position_id, is_active))
                    updated += 1

        self.db.conn.commit()
        print(f"✅ Imported: {inserted} new, {updated} updated employees from {filename}")    