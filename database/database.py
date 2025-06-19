import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Tuple

DB_PATH = Path(__file__).parent / "furniture.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

    def get_materials(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Materials")
        return [dict(row) for row in cursor.fetchall()]

    def get_material(self, material_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Materials WHERE id = ?", (material_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def add_material(self, material_data: Dict) -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO Materials (type, name, price, unit, package_amount, stock_amount, min_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            material_data['type'],
            material_data['name'],
            material_data['price'],
            material_data['unit'],
            material_data['package_amount'],
            material_data['stock_amount'],
            material_data['min_amount']
        ))
        self.conn.commit()
        return cursor.lastrowid

    def update_material(self, material_id: int, material_data: Dict) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE Materials 
            SET type = ?, name = ?, price = ?, unit = ?, package_amount = ?, stock_amount = ?, min_amount = ?
            WHERE id = ?
        """, (
            material_data['type'],
            material_data['name'],
            material_data['price'],
            material_data['unit'],
            material_data['package_amount'],
            material_data['stock_amount'],
            material_data['min_amount'],
            material_id
        ))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_material(self, material_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Materials WHERE id = ?", (material_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_products_for_material(self, material_id: int) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.id, p.name, mp.amount
            FROM Products p
            JOIN MaterialProduct mp ON p.id = mp.product_id
            WHERE mp.material_id = ?
        """, (material_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_required_amount(self, material_id: int) -> float:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT SUM(mp.amount) as total
            FROM MaterialProduct mp
            WHERE mp.material_id = ?
        """, (material_id,))
        result = cursor.fetchone()
        return result['total'] if result['total'] else 0.0

    def close(self):
        self.conn.close()


# Убедитесь, что класс экспортируется
__all__ = ['Database']