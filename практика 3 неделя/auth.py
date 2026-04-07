import tkinter as tk
from tkinter import messagebox
from captcha import PuzzleCaptcha

class AuthWindow:
    def __init__(self, db):
        self.db = db
        self.captcha_failures = {}
        self.captcha_success = False
        self.current_username = None
        self.create_window()
    
    def create_window(self):
        self.window = tk.Tk()
        self.window.title("Авторизация - Система управления производством")
        self.window.geometry("600x900")
        self.window.resizable(True, True)
        self.window.minsize(550, 800)
        self.window.configure(bg="#f0f0f0")

        self.center_window()
        
        header_frame = tk.Frame(self.window, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Управление производственным предприятием", 
                 font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=20)
        
        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=30)
        
        tk.Label(form_frame, text="Вход в систему", 
                 font=("Arial", 14, "bold"), bg="#f0f0f0", fg="black").grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(form_frame, text="Логин:", font=("Arial", 11), bg="#f0f0f0", fg="black").grid(row=1, column=0, sticky="e", pady=10, padx=5)
        self.entry_username = tk.Entry(form_frame, width=25, font=("Arial", 11), relief=tk.GROOVE, bd=2)
        self.entry_username.grid(row=1, column=1, pady=10, padx=5)
        
        tk.Label(form_frame, text="Пароль:", font=("Arial", 11), bg="#f0f0f0", fg="black").grid(row=2, column=0, sticky="e", pady=10, padx=5)
        self.entry_password = tk.Entry(form_frame, show="*", width=25, font=("Arial", 11), relief=tk.GROOVE, bd=2)
        self.entry_password.grid(row=2, column=1, pady=10, padx=5)
        
        self.captcha = PuzzleCaptcha(self.window, self.on_captcha_result)
        
        btn_frame = tk.Frame(self.window, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        
        self.login_btn = tk.Button(btn_frame, text="Войти", command=self.login,
                                   width=20, height=2, bg="#2196F3", fg="black", 
                                   font=("Arial", 11, "bold"), cursor="hand2",
                                   relief=tk.RAISED)
        self.login_btn.pack()
        
        self.entry_username.bind("<KeyRelease>", self.on_username_change)
        
        self.window.mainloop()
    
    def center_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        window_width = 600
        window_height = 900
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def on_username_change(self, event):
        """При изменении логина сбрасываем состояние для нового пользователя"""
        username = self.entry_username.get().strip()
        
        if username != self.current_username:
            self.current_username = username
            self.captcha_success = False
            self.login_btn.config(state="normal", bg="#2196F3")
            
            # Проверяем, не заблокирован ли пользователь в БД
            if username:
                user = self.db.get_user(username)
                if user and user[4]:  # is_blocked
                    messagebox.showwarning("Доступ запрещен", 
                                          f"Пользователь '{username}' заблокирован.\n"
                                          "Обратитесь к администратору для разблокировки.")
                    self.login_btn.config(state="disabled", bg="#cccccc")
    
    def on_captcha_result(self, success):
        self.captcha_success = success
        username = self.entry_username.get().strip()
        
        if not success:
            if username not in self.captcha_failures:
                self.captcha_failures[username] = 0
            
            self.captcha_failures[username] += 1
            
            user = self.db.get_user(username) if username else None
            
            if user and self.captcha_failures[username] >= 3:
                user_id, db_username, db_password, role, is_blocked, failed_attempts = user
                
                if role != 'admin':
                    self.db.block_user(user_id)
                    messagebox.showerror("Доступ запрещен", 
                                        f"Пользователь '{username}' заблокирован.\n"
                                        "Вы превысили количество попыток сборки пазла.\n"
                                        "Обратитесь к администратору для разблокировки.\n\n"
                                        "Введите другой логин для входа в систему.")
                    self.login_btn.config(state="disabled", bg="#cccccc")
                    # Не блокируем поля, чтобы можно было ввести другой логин
                else:
                    messagebox.showwarning("Внимание", 
                                          f"Администратор, вы превысили количество попыток сборки пазла.\n"
                                          f"Учетная запись администратора не блокируется.\n"
                                          "Нажмите кнопку 'Перемешать' для продолжения.")
                    self.captcha_failures[username] = 0
            elif not username and self.captcha_failures.get("", 0) >= 3:
                self.login_btn.config(state="disabled", bg="#cccccc")
                messagebox.showerror("Доступ запрещен", 
                                    "Вы превысили количество попыток сборки пазла.\n"
                                    "Введите логин и нажмите кнопку 'Перемешать'.")
        else:
            self.login_btn.config(state="normal", bg="#2196F3")
            if username:
                self.captcha_failures[username] = 0
    
    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Ошибка ввода", 
                                "Пожалуйста, заполните все поля!\n"
                                "Логин и пароль обязательны для заполнения.")
            return
        
        if not self.captcha_success:
            messagebox.showwarning("Ошибка капчи", 
                                "Пожалуйста, соберите пазл правильно!\n"
                                "Для успешной авторизации необходимо собрать изображение.")
            return
        
        user = self.db.get_user(username)
        
        if not user:
            messagebox.showerror("Ошибка авторизации", 
                                "Вы ввели неверный логин или пароль.\n"
                                "Пожалуйста, проверьте введенные данные и попробуйте снова.")
            return
        
        user_id, db_username, db_password, role, is_blocked, failed_attempts = user
        
        if is_blocked:
            messagebox.showerror("Доступ запрещен", 
                                f"Учетная запись '{username}' заблокирована.\n"
                                "Обратитесь к администратору для разблокировки.")
            return
        
        if password == db_password:
            self.db.reset_failed_attempts(user_id)
            messagebox.showinfo("Успешная авторизация", 
                            f"Добро пожаловать, {username}!\n"
                            "Вы успешно вошли в систему.")
            self.window.destroy()
            
            if role == 'admin':
                from admin_panel import AdminPanel
                AdminPanel(self.db)
            else:
                from user_panel import UserPanel
                UserPanel(self.db, username)
        else:
            if role == 'admin':
                messagebox.showwarning("Ошибка авторизации", 
                                    f"Неверный логин или пароль для администратора.\n"
                                    f"Учетная запись администратора не блокируется.\n"
                                    f"Попробуйте снова.")
                return
            
            new_attempts = failed_attempts + 1
            self.db.update_failed_attempts(user_id, new_attempts)
            
            if new_attempts >= 3:
                self.db.block_user(user_id)
                messagebox.showerror("Доступ запрещен", 
                                    f"Пользователь '{username}' заблокирован.\n"
                                    "Вы превысили количество допустимых попыток входа.\n"
                                    "Обратитесь к администратору для разблокировки.\n\n"
                                    "Введите другой логин для входа в систему.")
            else:
                remaining = 3 - new_attempts
                messagebox.showwarning("Ошибка авторизации", 
                                    f"Неверный логин или пароль.\n"
                                    f"Осталось попыток: {remaining}\n"
                                    f"После 3 неудачных попыток учетная запись будет заблокирована.")