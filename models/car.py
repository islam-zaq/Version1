from database import Database
import sqlite3

class Car:
    def __init__(self):
        self.db = Database()

    def create_car(self, model, car_idnum, employee_id1, employee_id2=None):
        """Add a new car record."""
        self.db.execute("INSERT INTO cars (model, car_idnum, employee_id1, employee_id2) VALUES (?, ?, ?, ?)", 
                        (model, car_idnum, employee_id1, employee_id2))
        print("Car record added successfully!")

    def read_cars(self):
        """Fetch and display cars."""
        return self.db.fetchall('''SELECT c.id, c.model, c.car_idnum, e1.name AS owner1, e2.name AS owner2
                                   FROM cars c
                                   JOIN employees e1 ON c.employee_id1 = e1.id
                                   LEFT JOIN employees e2 ON c.employee_id2 = e2.id''')

    def update_car(self, car_id, model, car_idnum, employee_id1, employee_id2=None):
        """Update a car record."""
        self.db.execute("UPDATE cars SET model = ?, car_idnum = ?, employee_id1 = ?, employee_id2 = ? WHERE id = ?", 
                        (model, car_idnum, employee_id1, employee_id2, car_id))
        print("Car record updated successfully!")

    def delete_car(self, car_id):
        """Delete a car record."""
        try:
            self.db.execute("DELETE FROM cars WHERE id = ?", (car_id,))
            print(f"✅ Cars ID {car_id} deleted successfully.")
        except sqlite3.IntegrityError:
            print(f"❌ Cannot delete Cars ID {car_id} because it is referenced elsewhere.")
