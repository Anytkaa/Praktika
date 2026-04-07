import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="ManufacturingEnterpriseDB",
                user="postgres",
                password="00343kvn"  
            )
            self.cursor = self.conn.cursor()
            print("Подключение к базе данных успешно!")
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            raise
    
    def get_user(self, username):
        """Получение пользователя по логину"""
        self.cursor.execute(
            "SELECT id, username, password, role, is_blocked, failed_attempts FROM users WHERE username = %s",
            (username,)
        )
        result = self.cursor.fetchone()
        if result:
            return (result[0], result[1], result[2], result[3], result[4], result[5])
        return None
    
    def update_failed_attempts(self, user_id, attempts):
        """Обновление счетчика неудачных попыток (администратор не блокируется)"""
        # Проверяем, не администратор ли это
        self.cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
        result = self.cursor.fetchone()
        
        if result and result[0] == 'admin':
            self.cursor.execute(
                "UPDATE users SET failed_attempts = 0 WHERE id = %s",
                (user_id,)
            )
            self.conn.commit()
            return
        
        self.cursor.execute(
            "UPDATE users SET failed_attempts = %s WHERE id = %s",
            (attempts, user_id)
        )
        self.conn.commit()
    
    def block_user(self, user_id):
        """Блокировка пользователя (администратор не блокируется)"""
        self.cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
        result = self.cursor.fetchone()
        
        if result and result[0] == 'admin':
            print("Попытка блокировки администратора - отклонено")
            return
        
        self.cursor.execute(
            "UPDATE users SET is_blocked = TRUE WHERE id = %s",
            (user_id,)
        )
        self.conn.commit()
        print(f"Пользователь с ID {user_id} заблокирован")
    
    def reset_failed_attempts(self, user_id):
        """Сброс счетчика неудачных попыток"""
        self.cursor.execute(
            "UPDATE users SET failed_attempts = 0 WHERE id = %s",
            (user_id,)
        )
        self.conn.commit()
    
    def get_all_users(self):
        """Получение всех пользователей"""
        self.cursor.execute(
            "SELECT id, username, role, is_blocked, failed_attempts FROM users ORDER BY id"
        )
        return self.cursor.fetchall()
    
    def add_user(self, username, password, role):
        """Добавление нового пользователя"""
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, password, role)
            )
            self.conn.commit()
            return True, "Пользователь добавлен"
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False, "Пользователь с таким логином уже существует"
    
    def update_user(self, user_id, username=None, password=None, role=None, is_blocked=None):
        """Обновление данных пользователя"""
        updates = []
        params = []
        
        if username is not None:
            updates.append("username = %s")
            params.append(username)
        
        if password is not None and password != "":
            updates.append("password = %s")
            params.append(password)
        
        if role is not None:
            updates.append("role = %s")
            params.append(role)
        
        if is_blocked is not None:
            # Проверяем, не администратор ли это
            self.cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            result = self.cursor.fetchone()
            
            if result and result[0] == 'admin' and is_blocked:
                # Нельзя блокировать администратора
                print("Попытка блокировки администратора - отклонено")
                return
            
            updates.append("is_blocked = %s")
            params.append(is_blocked)
            if not is_blocked:
                updates.append("failed_attempts = 0")
        
        if updates:
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            self.cursor.execute(query, params)
            self.conn.commit()
    
    def delete_user(self, user_id):
        """Удаление пользователя (администратора нельзя удалить)"""
        self.cursor.execute(
            "DELETE FROM users WHERE id = %s AND role != 'admin'",
            (user_id,)
        )
        self.conn.commit()
    
    def close(self):
        self.cursor.close()
        self.conn.close()