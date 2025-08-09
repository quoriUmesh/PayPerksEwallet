import hashlib
from datetime import datetime
from db_connector import create_connection, close_connection



class DatabaseManager:
    def __init__(self):
        try:
            self.conn = create_connection()
            self.cursor = self.conn.cursor()
            self.create_tables()
        except Exception as e:
            print("Failed to initialize database connection:", e)
            self.conn = None
            self.cursor = None

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print('db closed')
        except Exception as e:
            print("Error closing connection:", e)

    def create_tables(self):
        """Create all necessary tables"""
        self.create_user_table()
        self.create_transactions_table()
        self.create_rewards_table()
        self.create_login_session_table()

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users_table (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash  VARCHAR(255) NOT NULL,
            dob DATE DEFAULT NULL,
            address VARCHAR(255) DEFAULT NULL,
            phone_number VARCHAR(10) DEFAULT NULL,
            type_of_id VARCHAR(50) DEFAULT NULL,
            id_number  VARCHAR(50) DEFAULT NULL,
            balance DECIMAL(10,2) DEFAULT 0.00,
            reward_points DECIMAL(10,2) DEFAULT 0.00,
            income DECIMAL(10,2) DEFAULT 0.00,
            expenses DECIMAL(10,2) DEFAULT 0.00,
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print("Error creating users_table:", e)

    def create_transactions_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS transactions_table (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            sender_id INT NOT NULL,
            receiver_id INT,
            amount DECIMAL(10,2) NOT NULL,
            transaction_type VARCHAR(50) NOT NULL,
            description TEXT DEFAULT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users_table(user_id)
        );
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print("Error creating transactions_table:", e)

    def create_rewards_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS rewards_table (
            reward_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            points INT NOT NULL,
            source_transaction_id INT DEFAULT NULL,
            reward_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users_table(user_id),
            FOREIGN KEY (source_transaction_id) REFERENCES transactions_table(transaction_id)
        );
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print("Error creating rewards_table:", e)

    def create_login_session_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS login_session_table (
            user_id INT NOT NULL,
            session_id VARCHAR(64) UNIQUE NOT NULL,
            login_time TIMESTAMP NULL,
            logout_time TIMESTAMP NULL,
            expiry_time TIMESTAMP NOT NULL,
            PRIMARY KEY (session_id),
            FOREIGN KEY (user_id) REFERENCES users_table(user_id)
        );
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print("Error creating logging session table:", e)


    def hash_password(self, password):
        try:
            return hashlib.sha256(password.encode()).hexdigest()
        except Exception as e:
            print("Password hashing failed:", e)
            return None

    def register_user(self, full_name, email, password):
        try:
            hashed_pw = self.hash_password(password)
            if not hashed_pw:
                raise ValueError("Hashing failed")
            query = 'INSERT INTO users_table (full_name, password_hash, email) VALUES (%s, %s, %s)'
            self.cursor.execute(query, (full_name, hashed_pw, email))
            self.conn.commit()
            return True
        except Exception as e:
            print("User registration failed:", e)
            return False

    def authenticate_user(self, email, password):
        try:
            query = 'SELECT password_hash FROM users_table WHERE email = %s'
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
            print('authing')
            if result:
                stored_hash = result[0]
                input_hash = self.hash_password(password)
                success= input_hash == stored_hash
                if success:
                    print('pass match')
                    return True
            print('pass miss match')
            return False
        except Exception as e:
            print("Authentication error:", e)

            return False

    def get_user_by_email(self, email):
        try:
            query = 'SELECT full_name, balance, reward_points, income, expenses, user_id FROM users_table WHERE email = %s'
            self.cursor.execute(query, (email,))
            print('data recieved')
            return self.cursor.fetchone()
        except Exception as e:
            print("Error fetching user by email:", e)
            return None
        
    def email_exists(self, email):
        try:
            query = 'SELECT 1 FROM users_table WHERE email = %s'
            self.cursor.execute(query, (email,))
            return self.cursor.fetchone() is not None
        except Exception as e:
            print("Email check failed:", e)
            return False

    def update_password(self, email, new_password):
        try:
            hashed_pw = self.hash_password(new_password)
            if not hashed_pw:
                return False
            query = 'UPDATE users_table SET password_hash = %s WHERE email = %s'
            self.cursor.execute(query, (hashed_pw, email))
            self.conn.commit()
            return True
        except Exception as e:
            print("Password update failed:", e)
            return False

    def process_send_money(self, sender_email, recipient_email, amount):
        try:
            amount = int(amount)
            # Get sender and recipient IDs
            sender_query = 'SELECT user_id, balance FROM users_table WHERE email = %s'
            self.cursor.execute(sender_query, (sender_email,))
            sender_data = self.cursor.fetchone()
            
            recipient_query = 'SELECT user_id FROM users_table WHERE email = %s'
            self.cursor.execute(recipient_query, (recipient_email,))
            recipient_data = self.cursor.fetchone()
            
            if not sender_data or not recipient_data:
                return False
            
            sender_id, sender_balance = sender_data
            recipient_id = recipient_data[0]
            
            if sender_balance < amount:
                return False
            
            # Update balances
            new_sender_balance = sender_balance - amount
            self.cursor.execute('UPDATE users_table SET balance = %s, expenses = expenses + %s WHERE user_id = %s', 
                              (new_sender_balance, amount, sender_id))
            
            self.cursor.execute('UPDATE users_table SET balance = balance + %s, income = income + %s WHERE user_id = %s', 
                              (amount, amount, recipient_id))
            
            # Record transaction
            self.cursor.execute('''INSERT INTO transactions_table 
                              (sender_id, receiver_id, amount, transaction_type, description) 
                              VALUES (%s, %s, %s, %s, %s)''', 
                              (sender_id, recipient_id, amount, 'send', f'Sent to {recipient_email}'))
            
            transaction_id = self.cursor.lastrowid
            
            # Add reward points (2% of transaction)
            print('begin reward calculating')
            reward_points = int(amount * 0.02)
            print('reward calculated begining of insert')
            if reward_points > 0:
                self.cursor.execute('UPDATE users_table SET reward_points = reward_points + %s WHERE user_id = %s', 
                                  (reward_points, sender_id))
                self.cursor.execute('''INSERT INTO rewards_table (user_id, points, source_transaction_id) 
                                  VALUES (%s, %s, %s)''', (sender_id, reward_points, transaction_id))
            
            self.conn.commit()
            return True
        except Exception as e:
            print("Send money failed:", e)
            self.conn.rollback()
            return False

    def process_load_money(self, email, amount, method):
        try:
            user_query = 'SELECT user_id FROM users_table WHERE email = %s'
            self.cursor.execute(user_query, (email,))
            user_data = self.cursor.fetchone()
            
            if not user_data:
                return False
            
            user_id = user_data[0]
            
            # Update balance and income
            self.cursor.execute('UPDATE users_table SET balance = balance + %s, income = income + %s WHERE user_id = %s', 
                              (amount, amount, user_id))
            
            # Record transaction
            self.cursor.execute('''INSERT INTO transactions_table 
                              (sender_id, amount, transaction_type, description) 
                              VALUES (%s, %s, %s, %s)''', 
                              (user_id, amount, 'load', f'Loaded via {method}'))
            
            transaction_id = self.cursor.lastrowid
            
            # Add reward points (2% of transaction)
            reward_points = int(amount * 0.02)
            if reward_points > 0:
                self.cursor.execute('UPDATE users_table SET reward_points = reward_points + %s WHERE user_id = %s', 
                                  (reward_points, user_id))
                self.cursor.execute('''INSERT INTO rewards_table (user_id, points, source_transaction_id) 
                                  VALUES (%s, %s, %s)''', (user_id, reward_points, transaction_id))
            
            self.conn.commit()
            return True
        except Exception as e:
            print("Load money failed:", e)
            self.conn.rollback()
            return False
        
    def process_redeem_points(self, email, points):
        try:
            amount = float(points)  # 1 point = $1
            self.cursor.execute('''
                SELECT user_id FROM users_table WHERE email = %s''',(email,))
            id = self.cursor.fetchone()

            # Update user data directly via email
            self.cursor.execute('''
                UPDATE users_table
                SET balance = balance + %s, 
                    reward_points = reward_points - %s, 
                    income = income + %s
                WHERE email = %s
            ''', (amount, amount, amount, email))
            # Log the transaction (assuming sender_email is a valid column)
            self.cursor.execute('''
                INSERT INTO transactions_table 
                (sender_id,receiver_id, amount, transaction_type, description) 
                VALUES (%s, %s,%s, 'redeem', %s)
            ''', (id[0],id[0], amount, f"Redeemed {amount} points"))
            self.conn.commit()
            return True

        except Exception as e:
            print("Redeem points failed:", e)
            self.conn.rollback()
            return False


    def process_utility_payment(self, email, amount, payment_type):
        try:
            user_query = 'SELECT user_id, balance FROM users_table WHERE email = %s'
            self.cursor.execute(user_query, (email,))
            user_data = self.cursor.fetchone()
            
            if not user_data:
                return False
            
            user_id, balance = user_data
            
            if balance < amount:
                return False
            
            # Update balance and expenses
            self.cursor.execute('UPDATE users_table SET balance = balance - %s, expenses = expenses + %s WHERE user_id = %s', 
                              (amount, amount, user_id))
            
            # Record transaction
            self.cursor.execute('''INSERT INTO transactions_table 
                              (sender_id, amount, transaction_type, description) 
                              VALUES (%s, %s, %s, %s)''', 
                              (user_id, amount, 'payment', payment_type))
            
            transaction_id = self.cursor.lastrowid
            
            # Add reward points (2% of transaction)
            reward_points = int(amount * 0.02)
            if reward_points > 0:
                self.cursor.execute('UPDATE users_table SET reward_points = reward_points + %s WHERE user_id = %s', 
                                  (reward_points, user_id))
                self.cursor.execute('''INSERT INTO rewards_table (user_id, points, source_transaction_id) 
                                  VALUES (%s, %s, %s)''', (user_id, reward_points, transaction_id))
            
            self.conn.commit()
            return True
        except Exception as e:
            print("Utility payment failed:", e)
            self.conn.rollback()
            return False

    def get_user_transactions(self, user_id):
        try:
            query = '''SELECT transaction_date, transaction_type, amount, description,sender_id
                      FROM transactions_table WHERE sender_id = %s OR receiver_id =%s 
                      ORDER BY transaction_date DESC LIMIT 20'''
            self.cursor.execute(query, (user_id,user_id))
            return self.cursor.fetchall()
        except Exception as e:
            print("Error fetching transactions:", e)
            return []

    def get_transaction_chart_data(self, user_id,current_balance):
        try:
            if not user_id:
                return []
            
            query = '''SELECT transaction_type, amount,sender_id
                      FROM transactions_table WHERE sender_id = %s OR receiver_id =%s 
                      ORDER BY transaction_date DESC LIMIT 5'''
            self.cursor.execute(query, (user_id,user_id))
            results = self.cursor.fetchall()
            data = []
            data.append(current_balance)
            if results:
                for transaction_type, amount,sender_id in results:
                    if transaction_type in ['load','redeem']:
                        current_balance = current_balance - amount

                    elif transaction_type == 'send':
                        if sender_id == user_id:
                            current_balance = current_balance + amount
                        else:
                            current_balance = current_balance - amount

                    else:
                        current_balance = current_balance + amount
                    data.append(current_balance)
                print('chart data :',data)
                return data[::-1]
            else:
                print('chart else')
                return [0,0,0,0,0]
        except Exception as e:
            print("Error fetching chart data:", e)
            return [0,0,0,0,0]
        
    def insert_session(self, user_id, session_id, login_time, expiry_time):
        try:
            query = 'INSERT INTO login_session_table (user_id, session_id, login_time, expiry_time) VALUES (%s, %s, %s, %s)'
            self.cursor.execute(query, (user_id, session_id, login_time, expiry_time))
            self.conn.commit()
            print('session inserted')
            return True
        except Exception as e:
            print("Login Session failed:", e)
            return False
   

    def update_session(self, session_id, expiry):
        try:
            query = '''
                UPDATE login_session_table 
                SET expiry_time = %s 
                WHERE session_id = %s AND logout_time IS NULL
            '''
            self.cursor.execute(query, (expiry, session_id))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                print(f"No active session found with ID: {session_id}")
                return False
            return True
        except Exception as e:
            print(f"Session refresh error: {e}")
            return False

    
    def invalidate_session(self, session_id):
        try:
            now = datetime.now()
            query = 'UPDATE login_session_table SET logout_time = %s WHERE session_id = %s'
            self.cursor.execute(query,(now,session_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Session invalidation error: {e}")
            return False