from database import Database
import sqlite3
import csv

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

    def export_cars_to_csv(self, filename="cars.csv"):
        """
        Export all cars to a CSV file.
        Columns: id, model, car_idnum, employee_id1, employee_id2, is_active
        """
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, model, car_idnum, employee_id1, employee_id2, is_active FROM cars")
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"✅ Exported {len(rows)} cars to {filename}")

    def import_cars_from_csv(self, filename="cars.csv"):
        """
        Import cars from CSV.
        - If ID is blank → insert new car (auto id).
        - If ID exists → update that car.
        - If ID does not exist → insert with that ID.
        """
        cursor = self.db.conn.cursor()
        inserted, updated = 0, 0

        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            expected_headers = ["id", "model", "car_idnum", "employee_id1", "employee_id2", "is_active"]
            if reader.fieldnames != expected_headers:
                print(f"❌ Error: CSV headers must be {expected_headers}, got {reader.fieldnames}")
                return

            for row in reader:
                car_id = row["id"].strip()
                model = row["model"].strip()
                car_idnum = row["car_idnum"].strip()
                employee_id1 = row["employee_id1"].strip() or None
                employee_id2 = row["employee_id2"].strip() or None
                is_active = row["is_active"].strip() or "1"

                if car_id == "":
                    cursor.execute("""
                        INSERT INTO cars (model, car_idnum, employee_id1, employee_id2, is_active)
                        VALUES (?, ?, ?, ?, ?)
                    """, (model, car_idnum, employee_id1, employee_id2, is_active))
                    inserted += 1
                else:
                    cursor.execute("""
                        UPDATE cars
                        SET model=?, car_idnum=?, employee_id1=?, employee_id2=?, is_active=?
                        WHERE id=?
                    """, (model, car_idnum, employee_id1, employee_id2, is_active, car_id))

                    if cursor.rowcount == 0:
                        cursor.execute("""
                            INSERT INTO cars (id, model, car_idnum, employee_id1, employee_id2, is_active)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (car_id, model, car_idnum, employee_id1, employee_id2, is_active))
                    updated += 1

        self.db.conn.commit()
        print(f"✅ Imported: {inserted} new, {updated} updated cars from {filename}")