import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class PuzzleCaptcha:
    def __init__(self, parent, on_success):
        self.parent = parent
        self.on_success = on_success
        self.correct_order = [0, 3, 1, 2]  # Правильный порядок фрагментов
        self.current_order = []
        self.selected_idx = None
        self.piece_images = []
        self.piece_labels = []
        
        # Пути к изображениям фрагментов
        self.piece_paths = [
            "/Users/annapislegina/Desktop/ПРАКТИКА/практика 3 неделя/captcha/1.jpg",
            "/Users/annapislegina/Desktop/ПРАКТИКА/практика 3 неделя/captcha/2.jpg",
            "/Users/annapislegina/Desktop/ПРАКТИКА/практика 3 неделя/captcha/3.jpg",
            "/Users/annapislegina/Desktop/ПРАКТИКА/практика 3 неделя/captcha/4.jpg"
        ]
        
        self.create_captcha()
    
    def create_captcha(self):
        """Создание пазла из 4 фрагментов с изображениями в сетке 2x2"""
        frame = tk.Frame(self.parent, bd=2, relief=tk.GROOVE, bg="#f5f5f5")
        frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(frame, text="Соберите пазл (кликните на два фрагмента для обмена):", 
                 font=("Arial", 10), bg="#f5f5f5", fg="black").pack(pady=5)
        
        self.puzzle_frame = tk.Frame(frame, bg="#f5f5f5")
        self.puzzle_frame.pack(pady=10)
        
        self.current_order = self.correct_order.copy()
        random.shuffle(self.current_order)
        
        self.load_and_display_pieces()
        
        button_frame = tk.Frame(frame, bg="#f5f5f5")
        button_frame.pack(pady=10)
        
        self.check_button = tk.Button(button_frame, text="Проверить пазл", 
                                      command=self.check_puzzle,
                                      bg="#4CAF50", fg="black", font=("Arial", 10, "bold"),
                                      cursor="hand2")
        self.check_button.pack(side="left", padx=5)
        
        self.reset_button = tk.Button(button_frame, text="Перемешать", 
                                      command=self.reset_puzzle,
                                      bg="#FF9800", fg="black", font=("Arial", 10, "bold"),
                                      cursor="hand2")
        self.reset_button.pack(side="left", padx=5)
        
        self.status_label = tk.Label(frame, text="", fg="blue", bg="#f5f5f5", font=("Arial", 9))
        self.status_label.pack(pady=5)
    
    def load_and_display_pieces(self):
        """Загрузка и отображение фрагментов изображения в сетке 2x2"""
        # Очищаем старые виджеты
        for widget in self.puzzle_frame.winfo_children():
            widget.destroy()
        self.piece_labels = []
        self.piece_images = []
        
        # Размер фрагмента (подстройте под ваши изображения)
        piece_width = 150
        piece_height = 150
        
        # Создаем сетку 2x2 (2 строки, 2 столбца)
        for i in range(4):
            row = i // 2  # 0, 0, 1, 1
            col = i % 2   # 0, 1, 0, 1
            
            piece_idx = self.current_order[i]
            
            try:
                # Загружаем изображение
                img_path = self.piece_paths[piece_idx]
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img = img.resize((piece_width, piece_height), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                else:
                    # Если файл не найден, создаем заглушку
                    photo = self.create_placeholder_piece(piece_idx, piece_width, piece_height)
                
                # Создаем Label для отображения фрагмента
                label = tk.Label(self.puzzle_frame, image=photo, 
                                bg="white", relief=tk.RAISED, bd=2,
                                width=piece_width, height=piece_height)
                label.grid(row=row, column=col, padx=2, pady=2)
                label.bind("<Button-1>", lambda e, idx=i: self.on_piece_click(idx))
                
                self.piece_labels.append(label)
                self.piece_images.append(photo)  # Сохраняем ссылку!
                
            except Exception as e:
                print(f"Ошибка загрузки изображения {piece_idx}: {e}")
                # Создаем заглушку при ошибке
                photo = self.create_placeholder_piece(piece_idx, piece_width, piece_height)
                label = tk.Label(self.puzzle_frame, image=photo,
                                bg="white", relief=tk.RAISED, bd=2,
                                width=piece_width, height=piece_height)
                label.grid(row=row, column=col, padx=2, pady=2)
                label.bind("<Button-1>", lambda e, idx=i: self.on_piece_click(idx))
                
                self.piece_labels.append(label)
                self.piece_images.append(photo)
    
    def create_placeholder_piece(self, piece_idx, width, height):
        """Создание заглушки, если изображение не найдено"""
        img = Image.new('RGB', (width, height), color=self.get_piece_color(piece_idx))
        draw = ImageDraw.Draw(img)
        draw.text((width//2-40, height//2-10), f"Piece {piece_idx+1}", fill="black")
        return ImageTk.PhotoImage(img)
    
    def get_piece_color(self, idx):
        """Цвета для заглушек"""
        colors = ['#FFE0B5', '#C8E6E0', '#FFD966', '#B0D9B1']
        return colors[idx] if idx < len(colors) else '#FFFFFF'
    
    def on_piece_click(self, idx):
        """Обработка клика по фрагменту"""
        if self.selected_idx is None:
            # Первый клик - выбираем фрагмент
            self.selected_idx = idx
            self.piece_labels[idx].config(relief=tk.SUNKEN, bd=4)
            self.status_label.config(text=f"Выбран фрагмент {idx+1}")
        else:
            # Второй клик - меняем местами
            if self.selected_idx != idx:
                # Меняем местами в массиве
                self.current_order[self.selected_idx], self.current_order[idx] = \
                    self.current_order[idx], self.current_order[self.selected_idx]
                
                # Обновляем отображение
                self.load_and_display_pieces()
            
            self.selected_idx = None
            self.status_label.config(text="")
    
    def check_puzzle(self):
        """Проверка правильности сборки пазла"""
        if self.current_order == self.correct_order:
            self.status_label.config(text="Пазл собран верно! Вы можете войти.", fg="green")
            self.check_button.config(bg="#8BC34A")
            self.on_success(True)
        else:
            self.status_label.config(text="Пазл собран неверно! Попробуйте еще раз.", fg="red")
            self.on_success(False)
    
    def reset_puzzle(self):
        """Перемешивание фрагментов"""
        random.shuffle(self.current_order)
        self.load_and_display_pieces()
        self.selected_idx = None
        self.status_label.config(text="Пазл перемешан. Соберите его заново.", fg="blue")
        self.on_success(False)

# Добавляем импорт для создания заглушек
from PIL import ImageDraw