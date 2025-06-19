from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QDoubleSpinBox,
    QSpinBox, QDialogButtonBox, QMessageBox
)
from PyQt5.QtCore import Qt


class AddEditMaterialDialog(QDialog):
    def __init__(self, model, material_id=None, parent=None):
        super().__init__(parent)
        self.model = model
        self.material_id = material_id
        self.setWindowTitle("Добавить материал" if not material_id else "Редактировать материал")
        self.setWindowModality(Qt.ApplicationModal)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        form_layout = QFormLayout()

        # Тип материала
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Дерево", "Металл", "Пластик", "Ткань", "Стекло"])
        form_layout.addRow("Тип материала:", self.type_combo)

        # Наименование
        self.name_edit = QLineEdit()
        form_layout.addRow("Наименование:", self.name_edit)

        # Цена
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0, 999999.99)
        self.price_spin.setDecimals(2)
        self.price_spin.setPrefix("₽ ")
        form_layout.addRow("Цена за единицу:", self.price_spin)



        # Единица измерения
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["кг", "м", "м²", "л", "шт"])
        form_layout.addRow("Единица измерения:", self.unit_combo)

        # Количество в упаковке
        self.package_spin = QSpinBox()
        self.package_spin.setRange(1, 9999)
        form_layout.addRow("Количество в упаковке:", self.package_spin)

        # Количество на складе
        self.stock_spin = QDoubleSpinBox()
        self.stock_spin.setRange(0, 999999.99)
        self.stock_spin.setDecimals(2)
        form_layout.addRow("Количество на складе:", self.stock_spin)

        # Минимальное количество
        self.min_spin = QDoubleSpinBox()
        self.min_spin.setRange(0, 999999.99)
        self.min_spin.setDecimals(2)
        form_layout.addRow("Минимальное количество:", self.min_spin)

        layout.addLayout(form_layout)

        # Кнопки
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def load_data(self):
        if self.material_id:
            material = self.model.get_material(self.material_id)
            if material:
                self.type_combo.setCurrentText(material['type'])
                self.name_edit.setText(material['name'])
                self.price_spin.setValue(material['price'])
                self.unit_combo.setCurrentText(material['unit'])
                self.package_spin.setValue(material['package_amount'])
                self.stock_spin.setValue(material['stock_amount'])
                self.min_spin.setValue(material['min_amount'])

    def accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите наименование материала")
            return

        material_data = {
            'type': self.type_combo.currentText(),
            'name': self.name_edit.text().strip(),
            'price': self.price_spin.value(),
            'unit': self.unit_combo.currentText(),
            'package_amount': self.package_spin.value(),
            'stock_amount': self.stock_spin.value(),
            'min_amount': self.min_spin.value()
        }

        if self.material_id:
            success = self.model.update_material(self.material_id, material_data)
            msg = "Материал успешно обновлен" if success else "Не удалось обновить материал"
        else:
            material_id = self.model.add_material(material_data)
            msg = "Материал успешно добавлен" if material_id else "Не удалось добавить материал"

        QMessageBox.information(self, "Результат", msg)
        super().accept()