import sqlite3

class Database:
    def __init__(self, db_name="employees.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.enable_foreign_keys()
        self.setup_tables()

    def enable_foreign_keys(self):
        """Enable foreign key constraints."""
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()

    def setup_tables(self):
        """Create tables if they do not exist."""
        queries = [
            '''CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE)''',
                
            '''CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position_id INTEGER NOT NULL,
                FOREIGN KEY (position_id) REFERENCES positions (id))''',
                
            '''CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL)''',
                
            '''CREATE TABLE IF NOT EXISTS salary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                employee_id INTEGER NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES employees (id))''',
                
            '''CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                car_idnum TEXT NOT NULL UNIQUE,
                employee_id1 INTEGER NOT NULL,
                employee_id2 INTEGER,
                FOREIGN KEY (employee_id1) REFERENCES employees (id) ,
                FOREIGN KEY (employee_id2) REFERENCES employees (id))''',
                
            '''CREATE TABLE IF NOT EXISTS credit_card (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                employee_id INTEGER NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES employees (id))''',
                
            '''CREATE TABLE IF NOT EXISTS salary_calculate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                total_money REAL NOT NULL,
                km REAL)''',
                
            '''CREATE TABLE IF NOT EXISTS revision (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                employee_id INTEGER NOT NULL,
                total_income REAL NOT NULL,
                left_days INTEGER NOT NULL,
                credit_card REAL NOT NULL,
                km1 REAL NOT NULL,
                km2 REAL NOT NULL,
                total_expanse_sum REAL NOT NULL,
                expanse_comment TEXT,
                total_credit REAL NOT NULL,
                left_loan REAL NOT NULL,
                left_credit REAL NOT NULL,
                fund REAL NOT NULL,
                other_credit1_sum REAL NOT NULL,
                other_credit1_comment TEXT,
                other_credit2_sum REAL NOT NULL,
                other_credit2_comment TEXT,
                salary_calculate_id INTEGER NOT NULL,
                FOREIGN KEY (document_id) REFERENCES documents (id),
                FOREIGN KEY (employee_id) REFERENCES employees (id),
                FOREIGN KEY (salary_calculate_id) REFERENCES salary_calculate (id))'''
        ]
        for query in queries:
            self.execute(query)

    def execute(self, query, params=()):
        """Execute a query."""
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetchall(self, query, params=()):
        """Fetch all results from a query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=()):
        """Fetch one result from a query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        """Close the database connection."""
        self.conn.close()
