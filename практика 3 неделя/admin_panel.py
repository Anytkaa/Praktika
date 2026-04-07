import tkinter as tk
from tkinter import ttk, messagebox

class AdminPanel:
    def __init__(self, db):
        self.db = db
        self.window = tk.Tk()
        self.window.title("Панель администратора - Система управления производством")
        self.window.geometry("800x600")
        self.window.minsize(700, 500)
        self.window.configure(bg="#f0f0f0")
        
        # Заголовок
        header_frame = tk.Frame(self.window, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Панель администратора", 
                 font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack(pady=20)
        
        # Основной контейнер
        main_frame = tk.Frame(self.window, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Фрейм для списка пользователей
        list_frame = tk.LabelFrame(main_frame, text="Список пользователей", 
                                   font=("Arial", 12, "bold"), bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, side="left", padx=(0, 10))
        
        # Таблица пользователей
        columns = ("ID", "Логин", "Роль", "Заблокирован", "Попытки")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.column("Логин", width=150)
        self.tree.column("Роль", width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<ButtonRelease-1>", self.on_user_select)
        
        # Фрейм для кнопок управления
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(side="right", fill="y", padx=(10, 0))
        
        # Кнопки
        self.add_btn = tk.Button(buttons_frame, text="Добавить пользователя", 
                                 command=self.add_user_window,
                                 bg="#4CAF50", fg="black", font=("Arial", 10, "bold"),
                                 width=20, height=2, cursor="hand2")
        self.add_btn.pack(pady=5)
        
        self.edit_btn = tk.Button(buttons_frame, text="Редактировать", 
                                  command=self.edit_user_window,
                                  bg="#2196F3", fg="black", font=("Arial", 10, "bold"),
                                  width=20, height=2, cursor="hand2", state="disabled")
        self.edit_btn.pack(pady=5)
        
        self.unblock_btn = tk.Button(buttons_frame, text="Снять блокировку", 
                                     command=self.unblock_user,
                                     bg="#FF9800", fg="black", font=("Arial", 10, "bold"),
                                     width=20, height=2, cursor="hand2", state="disabled")
        self.unblock_btn.pack(pady=5)
        
        self.delete_btn = tk.Button(buttons_frame, text="Удалить", 
                                    command=self.delete_user,
                                    bg="#f44336", fg="black", font=("Arial", 10, "bold"),
                                    width=20, height=2, cursor="hand2", state="disabled")
        self.delete_btn.pack(pady=5)
        
        self.logout_btn = tk.Button(buttons_frame, text="Выйти", 
                                    command=self.logout,
                                    bg="#e74c3c", fg="black", font=("Arial", 10, "bold"),
                                    width=20, height=2, cursor="hand2")
        self.logout_btn.pack(pady=(20, 5))
        
        # Статусная строка
        self.status_label = tk.Label(self.window, text="Готов", 
                                     bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                     bg="#f0f0f0", font=("Arial", 9))
        self.status_label.pack(side="bottom", fill="x")
        
        self.selected_user_id = None
        self.load_users()
        self.window.mainloop()
    
    def load_users(self):
        """Загрузка списка пользователей"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        users = self.db.get_all_users()
        for user in users:
            user_id, username, role, is_blocked, failed_attempts = user
            blocked_status = "Да" if is_blocked else "Нет"
            self.tree.insert("", "end", values=(user_id, username, role, blocked_status, failed_attempts))
    
    def on_user_select(self, event):
        """Обработка выбора пользователя с защитой администратора"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.selected_user_id = item['values'][0]
            user_role = item['values'][2]  # Роль пользователя
            
            # Для администратора ограничиваем возможности
            if user_role == 'admin':
                self.edit_btn.config(state="normal")  
                self.delete_btn.config(state="disabled")  
                self.unblock_btn.config(state="disabled")  
                self.status_label.config(text="Администратор: удаление и блокировка недоступны")
            else:
                self.edit_btn.config(state="normal")
                self.delete_btn.config(state="normal")
                
               
                if item['values'][3] == "Да":
                    self.unblock_btn.config(state="normal")
                else:
                    self.unblock_btn.config(state="disabled")
                self.status_label.config(text="Готов")
        else:
            self.selected_user_id = None
            self.edit_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")
            self.unblock_btn.config(state="disabled")
    
    def add_user_window(self):
        """Окно добавления пользователя"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Добавление пользователя")
        dialog.geometry("500x450")
        dialog.configure(bg="#f0f0f0")
        dialog.resizable(False, False)
        
        # Центрирование
        dialog.transient(self.window)
        dialog.grab_set()
        
        tk.Label(dialog, text="Добавление нового пользователя", 
                 font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=20)
        
        form_frame = tk.Frame(dialog, bg="#f0f0f0", relief=tk.GROOVE, bd=2)
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        tk.Label(form_frame, text="Логин:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=0, column=0, sticky="e", pady=15, padx=10)
        entry_login = tk.Entry(form_frame, width=30, font=("Arial", 11), relief=tk.GROOVE, bd=2)
        entry_login.grid(row=0, column=1, pady=15, padx=10)
        
        tk.Label(form_frame, text="Пароль:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=1, column=0, sticky="e", pady=15, padx=10)
        entry_password = tk.Entry(form_frame, show="*", width=30, font=("Arial", 11), relief=tk.GROOVE, bd=2)
        entry_password.grid(row=1, column=1, pady=15, padx=10)
        
        tk.Label(form_frame, text="Подтверждение:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=2, column=0, sticky="e", pady=15, padx=10)
        entry_confirm = tk.Entry(form_frame, show="*", width=30, font=("Arial", 11), relief=tk.GROOVE, bd=2)
        entry_confirm.grid(row=2, column=1, pady=15, padx=10)
        
        tk.Label(form_frame, text="Роль:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=3, column=0, sticky="e", pady=15, padx=10)
        role_var = tk.StringVar(value="user")
        role_menu = ttk.Combobox(form_frame, textvariable=role_var, values=["user", "admin"], 
                                 width=27, font=("Arial", 11), state="readonly")
        role_menu.grid(row=3, column=1, pady=15, padx=10)
        
        error_label = tk.Label(dialog, text="", fg="red", bg="#f0f0f0", font=("Arial", 10, "bold"))
        error_label.pack(pady=10)
        
        def save_user():
            login = entry_login.get().strip()
            password = entry_password.get()
            confirm = entry_confirm.get()
            role = role_var.get()
            
            if not login:
                error_label.config(text="Ошибка: Введите логин!")
                return
            
            if not password:
                error_label.config(text="Ошибка: Введите пароль!")
                return
            
            if password != confirm:
                error_label.config(text="Ошибка: Пароли не совпадают!")
                return
            
            if len(password) < 3:
                error_label.config(text="Ошибка: Пароль должен содержать минимум 3 символа!")
                return
            
            success, message = self.db.add_user(login, password, role)
            if success:
                messagebox.showinfo("Успех", message)
                dialog.destroy()
                self.load_users()
                self.status_label.config(text=f"Пользователь {login} добавлен")
            else:
                error_label.config(text=message)
        
        btn_frame = tk.Frame(dialog, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Сохранить", command=save_user,
                  bg="#4CAF50", fg="black", font=("Arial", 11, "bold"),
                  width=15, height=1, cursor="hand2", relief=tk.RAISED).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Отмена", command=dialog.destroy,
                  bg="#9E9E9E", fg="black", font=("Arial", 11, "bold"),
                  width=15, height=1, cursor="hand2", relief=tk.RAISED).pack(side="left", padx=10)
        
        entry_login.focus()
    
    def edit_user_window(self):
        """Окно редактирования пользователя"""
        if not self.selected_user_id:
            return
        
        users = self.db.get_all_users()
        user_data = None
        for user in users:
            if user[0] == self.selected_user_id:
                user_data = user
                break
        
        if not user_data:
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Редактирование пользователя")
        dialog.geometry("500x450")
        dialog.configure(bg="#f0f0f0")
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        
        tk.Label(dialog, text="Редактирование пользователя", 
                 font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=20)
        
        form_frame = tk.Frame(dialog, bg="#f0f0f0", relief=tk.GROOVE, bd=2)
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        tk.Label(form_frame, text="Логин:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=0, column=0, sticky="e", pady=15, padx=10)
        entry_login = tk.Entry(form_frame, width=30, font=("Arial", 11), relief=tk.GROOVE, bd=2)
        entry_login.insert(0, user_data[1])
        entry_login.grid(row=0, column=1, pady=15, padx=10)
        
        tk.Label(form_frame, text="Новый пароль:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=1, column=0, sticky="e", pady=15, padx=10)
        entry_password = tk.Entry(form_frame, show="*", width=30, font=("Arial", 11), relief=tk.GROOVE, bd=2)
        entry_password.grid(row=1, column=1, pady=15, padx=10)
        
        tk.Label(form_frame, text="Роль:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=2, column=0, sticky="e", pady=15, padx=10)
        role_var = tk.StringVar(value=user_data[2])
        role_menu = ttk.Combobox(form_frame, textvariable=role_var, values=["user", "admin"], 
                                 width=27, font=("Arial", 11), state="readonly")
        role_menu.grid(row=2, column=1, pady=15, padx=10)
        
        info_label = tk.Label(dialog, text="Оставьте пароль пустым, если не хотите менять", 
                               fg="gray", bg="#f0f0f0", font=("Arial", 9))
        info_label.pack(pady=5)
        
        def save_user():
            login = entry_login.get().strip()
            password = entry_password.get()
            role = role_var.get()
            
            if not login:
                messagebox.showwarning("Ошибка", "Логин не может быть пустым!")
                return
            
            self.db.update_user(self.selected_user_id, username=login, 
                                password=password if password else None, role=role)
            messagebox.showinfo("Успех", "Данные пользователя обновлены")
            dialog.destroy()
            self.load_users()
            self.status_label.config(text=f"Пользователь {login} обновлен")
        
        btn_frame = tk.Frame(dialog, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Сохранить", command=save_user,
                  bg="#4CAF50", fg="black", font=("Arial", 11, "bold"),
                  width=15, height=1, cursor="hand2", relief=tk.RAISED).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Отмена", command=dialog.destroy,
                  bg="#9E9E9E", fg="black", font=("Arial", 11, "bold"),
                  width=15, height=1, cursor="hand2", relief=tk.RAISED).pack(side="left", padx=10)
    
    def unblock_user(self):
        """Снятие блокировки пользователя (администратор не блокируется)"""
        if self.selected_user_id:
            # Проверяем, не администратор ли это
            users = self.db.get_all_users()
            username = None
            role = None
            for user in users:
                if user[0] == self.selected_user_id:
                    username = user[1]
                    role = user[2]
                    break
            
            if role == 'admin':
                messagebox.showinfo("Информация", 
                                   "Учетная запись администратора не может быть заблокирована.\n"
                                   "Снятие блокировки не требуется.")
                return
            
            self.db.update_user(self.selected_user_id, is_blocked=False)
            messagebox.showinfo("Успех", f"Блокировка снята с пользователя '{username}'")
            self.load_users()
            self.status_label.config(text=f"Блокировка снята с {username}")
    
    def delete_user(self):
        """Удаление пользователя (администратора нельзя удалить)"""
        if self.selected_user_id:
            # Проверяем, не администратор ли это
            users = self.db.get_all_users()
            username = None
            role = None
            for user in users:
                if user[0] == self.selected_user_id:
                    username = user[1]
                    role = user[2]
                    break
            
            if role == 'admin':
                messagebox.showwarning("Ошибка", 
                                      "Невозможно удалить учетную запись администратора!")
                return
            
            if messagebox.askyesno("Подтверждение", 
                                   f"Вы уверены, что хотите удалить пользователя '{username}'?\n"
                                   "Это действие нельзя отменить."):
                self.db.delete_user(self.selected_user_id)
                self.load_users()
                self.selected_user_id = None
                self.edit_btn.config(state="disabled")
                self.delete_btn.config(state="disabled")
                self.unblock_btn.config(state="disabled")
                self.status_label.config(text=f"Пользователь {username} удален")
                messagebox.showinfo("Успех", f"Пользователь {username} удален")
    
    def logout(self):
        """Выход из системы"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите выйти из системы?"):
            self.window.destroy()
            from auth import AuthWindow
            AuthWindow(self.db)