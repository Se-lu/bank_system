import sqlite3
import os

class Database:
    def __init__(self, db_name='banking_system.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client(
                c_id INTEGER PRIMARY KEY AUTOINCREMENT,
                c_name VARCHAR(100) NOT NULL,
                c_mail CHAR(30) UNIQUE,
                c_id_card CHAR(20) UNIQUE NOT NULL,
                c_phone CHAR(20) UNIQUE NOT NULL,
                c_password CHAR(20) NOT NULL,
                c_address VARCHAR(25)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bank_card (
                b_number VARCHAR(30) PRIMARY KEY,
                b_type VARCHAR(20),
                b_c_id INTEGER NOT NULL,
                b_expiry_date DATE,
                FOREIGN KEY (b_c_id) REFERENCES client (c_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insurance (
                i_name VARCHAR(100) NOT NULL,
                i_id INTEGER PRIMARY KEY AUTOINCREMENT,
                i_amount INTEGER,
                i_person CHAR(20),
                i_year INTEGER,
                i_project VARCHAR(200),
                i_provider VARCHAR(100)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS finance (
                p_name VARCHAR(100) NOT NULL,
                p_id INTEGER PRIMARY KEY AUTOINCREMENT,
                p_description VARCHAR(4000),
                p_amount INTEGER,
                p_year INTEGER,
                p_risk_assessment VARCHAR(100)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fund (
                f_name VARCHAR(100) NOT NULL,
                f_id INTEGER PRIMARY KEY AUTOINCREMENT,
                f_type CHAR(20),
                f_amount INTEGER,
                risk_level CHAR(20) NOT NULL,
                f_manager INTEGER NOT NULL,
                f_benchmark VARCHAR(100)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS property (
                pro_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pro_type CHAR(10) NOT NULL,
                pro_status CHAR(20),
                pro_quantity INTEGER,
                pro_income INTEGER,
                pro_location VARCHAR(100)
            )
        ''')
        
        # Create client_insurance junction table for purchases
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_insurance (
                purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                insurance_id INTEGER,
                purchase_date DATE,
                premium_amount DECIMAL(10,2),
                coverage_period INTEGER,
                FOREIGN KEY (client_id) REFERENCES client(c_id),
                FOREIGN KEY (insurance_id) REFERENCES insurance(i_id)
            )
        ''')
        
        # Create client_fund junction table for investments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_fund (
                investment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                fund_id INTEGER,
                investment_amount DECIMAL(10,2),
                investment_date DATE,
                FOREIGN KEY (client_id) REFERENCES client(c_id),
                FOREIGN KEY (fund_id) REFERENCES fund(f_id)
            )
        ''')
        
        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_card VARCHAR(30),
                to_card VARCHAR(30),
                amount DECIMAL(10,2),
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                description TEXT,
                FOREIGN KEY (from_card) REFERENCES bank_card(b_number),
                FOREIGN KEY (to_card) REFERENCES bank_card(b_number)
            )
        ''')
        
        conn.commit()
        conn.close()

db = Database()
