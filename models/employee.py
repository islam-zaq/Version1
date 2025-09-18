from database import Database
import sqlite3

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
