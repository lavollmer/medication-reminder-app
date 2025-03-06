import sqlite3

# Create database
conn = sqlite3.connect('medication_reminders.db')

# Create tables
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
);
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medication_name TEXT,
    dosage TEXT,
    time TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

# commits the current transaction - commiting changes
conn.commit()

# closing the connection to the database
conn.close()
