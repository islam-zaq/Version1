from database import Database
import sqlite3

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
