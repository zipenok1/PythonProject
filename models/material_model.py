from typing import List, Dict, Optional  # Добавили импорт Optional
from database.database import Database


class MaterialModel:
    def __init__(self):
        self.db = Database()

    def get_all_materials(self) -> List[Dict]:
        materials = self.db.get_materials()
        for material in materials:
            material['required_amount'] = self.db.get_required_amount(material['id'])
        return materials

    def get_material(self, material_id: int) -> Optional[Dict]:
        material = self.db.get_material(material_id)
        if material:
            material['required_amount'] = self.db.get_required_amount(material_id)
            material['products'] = self.db.get_products_for_material(material_id)
        return material

    def add_material(self, material_data: Dict) -> int:
        return self.db.add_material(material_data)

    def update_material(self, material_id: int, material_data: Dict) -> bool:
        return self.db.update_material(material_id, material_data)

    def delete_material(self, material_id: int) -> bool:
        return self.db.delete_material(material_id)

    def close(self):
        self.db.close()