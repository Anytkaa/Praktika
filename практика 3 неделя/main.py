import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database
from auth import AuthWindow

def main():
    try:
        db = Database()
        AuthWindow(db)
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        print("Проверьте настройки подключения в database.py")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()