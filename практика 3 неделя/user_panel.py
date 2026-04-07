import tkinter as tk
from tkinter import messagebox

class UserPanel:
    def __init__(self, db, username):
        self.db = db
        self.username = username
        self.window = tk.Tk()
        self.window.title("Панель пользователя")
        self.window.geometry("500x450")
        self.window.configure(bg="#f0f0f0")
        
        # Заголовок
        header_frame = tk.Frame(self.window, bg="#2c3e50", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Панель пользователя", 
                 font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack(pady=20)
        
        # Основное содержимое
        content_frame = tk.Frame(self.window, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True, padx=20, pady=30)
        
        tk.Label(content_frame, text=f"Добро пожаловать, {username}!", 
                 font=("Arial", 16), bg="#f0f0f0", fg="black").pack(pady=20)
        
        tk.Label(content_frame, text="Ваша роль: Пользователь", 
                 font=("Arial", 12), bg="#f0f0f0", fg="black").pack()
        
        tk.Label(content_frame, text="Доступные функции:", 
                 font=("Arial", 11, "bold"), bg="#f0f0f0", fg="black").pack(pady=(30, 10))
        
        functions_frame = tk.Frame(content_frame, bg="#f0f0f0")
        functions_frame.pack()
        
        tk.Label(functions_frame, text="• Просмотр отчетов", font=("Arial", 10), bg="#f0f0f0", fg="black").pack(anchor="w")
        tk.Label(functions_frame, text="• Работа с заказами", font=("Arial", 10), bg="#f0f0f0", fg="black").pack(anchor="w")
        tk.Label(functions_frame, text="• Просмотр спецификаций", font=("Arial", 10), bg="#f0f0f0", fg="black").pack(anchor="w")
        
        # Кнопка выхода
        btn_frame = tk.Frame(self.window, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        
        self.logout_btn = tk.Button(btn_frame, text="Выйти из системы", command=self.logout,
                                    bg="#e74c3c", fg="black", font=("Arial", 11, "bold"), 
                                    cursor="hand2", width=20, height=2, relief=tk.RAISED)
        self.logout_btn.pack()
        
        self.window.mainloop()
    
    def logout(self):
        """Выход из системы и возврат в окно авторизации"""
        if messagebox.askyesno("Подтверждение", "Выйти из системы?"):
            self.window.destroy()
            from auth import AuthWindow
            AuthWindow(self.db)