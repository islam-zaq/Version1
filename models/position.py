from database import Database
import sqlite3
import csv

class Position:
    def __init__(self):
        self.db = Database()

    def create_position(self, title):
        """Add a new position."""
        self.db.execute("INSERT INTO positions (title) VALUES (?)", (title,))
        print("Position added successfully!")

    def read_positions(self):
        """Fetch all positions."""
        return self.db.fetchall("SELECT id, title FROM positions where is_active = 1")

    def update_position(self, pos_id, new_title):
        """Update a position."""
        self.db.execute("UPDATE positions SET title = ? WHERE id = ?", (new_title, pos_id))
        print("Position updated successfully!")

    def delete_position(self, pos_id):
        """Delete a position."""
        try:
            self.db.execute("DELETE FROM positions WHERE id = ?", (pos_id,))
            print(f"✅ Positions ID {pos_id} deleted successfully.")
        except sqlite3.IntegrityError:
            print(f"❌ Cannot delete Positions ID {pos_id} because it is referenced elsewhere.")

    def deactivate_position(self, pos_id):
        """Mark a position as inactive instead of deleting."""
        self.db.execute("UPDATE positions SET is_active = 0 WHERE id = ?", (pos_id,))
        print(f"✅ Position ID {pos_id} has been deactivated.")

    def reactivate_position(self, pos_id):
        """Restore a deactivated position to active status."""
        self.db.execute("UPDATE positions SET is_active = 1 WHERE id = ?", (pos_id,))
        print(f"✅ Position ID {pos_id} has been reactivated.")

    def read_inactive_positions(self):
        """Fetch only inactive positions."""
        return self.db.fetchall("SELECT id, title FROM positions WHERE is_active = 0")

    def export_positions_to_csv(self, filename):
        """
        Export all positons to a CSV file.
        """
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM positions")

        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)   # column names
            writer.writerows(rows)

        print(f"✅ Exported {len(rows)} positions to {filename}")
    
    def import_positions_from_csv(self, filename):
        """
        Import positions from CSV.
        - If ID is blank → insert new position (auto id).
        - If ID exists → update that position.
        - If ID does not exist → insert with that ID.
        """
        cursor = self.db.conn.cursor()
        inserted, updated = 0, 0

        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                id = row.get("id", "").strip()
                title = row.get("title", "").strip()
                is_active = row.get("is_active", "1").strip()  # default active=1

                if id == "":
                    # New employee → let DB generate ID
                    cursor.execute("""
                        INSERT INTO positions (title, is_active)
                        VALUES (?, ?)
                    """, (title, is_active))
                    inserted += 1
                else:
                    # Try update existing
                    cursor.execute("""
                        UPDATE positions
                        SET title=?, is_active=?
                        WHERE id=?
                    """, (title, is_active, id))

                    if cursor.rowcount == 0:
                        # If no row updated → insert with given id
                        cursor.execute("""
                            INSERT INTO positions (id, title, is_active)
                            VALUES (?, ?, ?)
                        """, (id, title, is_active))
                    updated += 1

        self.db.conn.commit()
        print(f"✅ Imported: {inserted} new, {updated} updated positions from {filename}")    