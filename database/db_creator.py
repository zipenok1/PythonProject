import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "furniture.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Создание таблицы Материалы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL CHECK(price >= 0),
        unit TEXT NOT NULL,
        package_amount INTEGER NOT NULL CHECK(package_amount > 0),
        stock_amount REAL NOT NULL CHECK(stock_amount >= 0),
        min_amount REAL NOT NULL CHECK(min_amount >= 0)
    )
    """)

    # Создание таблицы Продукция
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        param1 REAL NOT NULL CHECK(param1 > 0),
        param2 REAL NOT NULL CHECK(param2 > 0),
        type_coef REAL NOT NULL CHECK(type_coef > 0)
    )
    """)

    # Создание таблицы связи Материал-Продукция
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS MaterialProduct (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        amount REAL NOT NULL CHECK(amount > 0),
        FOREIGN KEY (material_id) REFERENCES Materials(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Products(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
       INSERT INTO Materials (type, name, price, unit, package_amount, stock_amount, min_amount)
            VALUES ('Дерево', 'Доска', 123.00, 'кг', 2, 1.00, 1.00)
      """)

    cursor.execute("""
           INSERT INTO Products (name, param1, param2, type_coef)
                VALUES ('Стол', 133.00, 123.00, 321.00)
          """)

    cursor.execute("""
               INSERT INTO MaterialProduct (material_id, product_id, amount)
                    VALUES ( 1, 1, 2.00)
              """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()